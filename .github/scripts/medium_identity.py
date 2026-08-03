"""Shared, stdlib-only identity helper for the Medium importer and the
source-side canonical-uniqueness gate (Importer dedupe P1).

Identity model
--------------
- A Medium ID is the trailing 12-hex suffix of the last path segment of a
  URL on medium.com or one of its subdomains — NEVER derived from any
  other host.
- normalize_canonical() strips the fragment and tracking parameters
  (`source`, `utm_*`); every other query parameter is MEANINGFUL and kept.
- entry_identity() reads both the feed link and the GUID/entry id; if both
  carry a Medium ID and they disagree, it FAILS CLOSED (IdentityError) —
  an inconsistent entry is never imported on a guess.
- Dedup priority downstream: Medium ID -> normalized canonical -> output
  path / conservative slug fallback. Two DIFFERENT stable identities must
  never be merged just because titles or slugs collide.

Ledger
------
imported_medium.json is versioned, sorted, unique:
  {"version": 1, "identities": [{"canonical": "...", "medium_id": "..."}]}
Loading accepts the legacy plain-URL-list format and migrates it in
memory. A missing file, corrupt JSON, or unknown schema NEVER degrades to
an empty ledger — that silent reset is exactly what re-imported an
existing article on 2026-08-03 (fe85f9e, reverted). Writing is atomic
(tmp + os.replace), deterministic (sorted keys, fixed separators), and is
only performed by the caller when a whole batch finished with zero
failures; writing twice yields byte-identical files.
"""
import json
import os
import re
import tempfile
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

MEDIUM_ID_RE = re.compile(r"(?:^|-)([0-9a-f]{12})$")
MEDIUM_ID_EXACT_RE = re.compile(r"^[0-9a-f]{12}$")
TRACKING_KEYS = ("source",)
TRACKING_PREFIXES = ("utm_",)
LEDGER_VERSION = 1


class IdentityError(ValueError):
    """Inconsistent or unusable identity — fail closed, never guess."""


class LedgerError(ValueError):
    """Missing, corrupt, or unknown-schema ledger — never default to empty."""


def _host_of(url_parts):
    return url_parts.netloc.lower().split("@")[-1].split(":")[0]


def is_medium_host(host):
    return host == "medium.com" or host.endswith(".medium.com")


def medium_id_from_url(url):
    """Trailing 12-hex id of the last path segment, medium.com hosts only."""
    if not url:
        return None
    parts = urlsplit(url.strip())
    if not is_medium_host(_host_of(parts)):
        return None
    segments = [s for s in parts.path.split("/") if s]
    if not segments:
        return None
    match = MEDIUM_ID_RE.search(segments[-1])
    return match.group(1) if match else None


def normalize_canonical(url):
    """Lower-cased scheme/host, fragment dropped, tracking params dropped,
    meaningful query kept in original order."""
    parts = urlsplit(url.strip())
    kept = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in TRACKING_KEYS
        and not key.lower().startswith(TRACKING_PREFIXES)
    ]
    return urlunsplit(
        (parts.scheme.lower(), _host_of(parts), parts.path, urlencode(kept), "")
    )


class Identity:
    __slots__ = ("medium_id", "canonical")

    def __init__(self, medium_id, canonical):
        self.medium_id = medium_id
        self.canonical = canonical

    def as_dict(self):
        entry = {"canonical": self.canonical}
        if self.medium_id:
            entry["medium_id"] = self.medium_id
        return entry


def entry_identity(link, guid=None):
    """Identity of a feed entry. Link and GUID must agree on the Medium ID;
    a mismatch is an IdentityError (fail closed)."""
    if not link:
        raise IdentityError("entry has no link")
    id_from_link = medium_id_from_url(link)
    id_from_guid = medium_id_from_url(guid) if guid else None
    if id_from_link and id_from_guid and id_from_link != id_from_guid:
        raise IdentityError(
            f"medium id mismatch between link ({id_from_link}) and guid ({id_from_guid})"
        )
    return Identity(id_from_link or id_from_guid, normalize_canonical(link))


CANONICAL_FM_RE = re.compile(
    r'^canonical:\s*["\']?(https?://[^"\']+)["\']?\s*$', re.IGNORECASE
)


def is_http_url(value):
    """A non-empty string whose scheme is http/https (case-insensitive)
    and that has a host — the only shape a canonical may take."""
    if not isinstance(value, str) or not value.strip():
        return False
    parts = urlsplit(value.strip())
    return parts.scheme.lower() in ("http", "https") and bool(_host_of(parts))


def canonical_from_markdown(text):
    """The canonical: front-matter value of a source file, or None.
    Front matter is delimited by FULL '---' lines — never split on the
    substring '---' (Medium canonicals contain six-dash runs). The scheme
    match is case-insensitive: HTTPS://MEDIUM.COM/... must not slip past
    this reader (and therefore past the uniqueness gate)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            return None
        match = CANONICAL_FM_RE.match(line)
        if match:
            return match.group(1)
    return None


def file_identity(path):
    """Identity of an existing content file via its canonical, or None."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        canonical = canonical_from_markdown(fh.read())
    if not canonical:
        return None
    return Identity(medium_id_from_url(canonical), normalize_canonical(canonical))


class Ledger:
    """Persistent identity ledger with fail-closed loading."""

    def __init__(self, identities):
        self._by_id = {}
        self._by_canonical = {}
        for identity in identities:
            self._remember(identity)

    def _remember(self, identity):
        if identity.medium_id:
            self._by_id[identity.medium_id] = identity
        self._by_canonical[identity.canonical] = identity

    def has_medium_id(self, medium_id):
        return bool(medium_id) and medium_id in self._by_id

    def has_canonical(self, canonical):
        return canonical in self._by_canonical

    def knows(self, identity):
        return self.has_medium_id(identity.medium_id) or self.has_canonical(identity.canonical)

    def add(self, identity):
        """Merge one identity, VALIDATING FIRST and mutating only after the
        outcome is decided — so a rejected add leaves the ledger byte-identical
        and `parse(serialize())` always round-trips.

        idempotent no-op   same canonical, same id
        keep existing      same canonical, existing has id, incoming has none
        promotion          same canonical, existing has no id, incoming id free
        alias              same id, different canonical -> keep the first
                           canonical, never write a second row
        new row            unseen canonical and unseen id
        LedgerError        same canonical with a different id, an ambiguous
                           bridge between two existing rows, malformed input,
                           or an id contradicting its own canonical
        """
        canonical = identity.canonical
        medium_id = identity.medium_id
        if not is_http_url(canonical):
            raise LedgerError(f"ledger canonical is not a usable http(s) URL: {canonical!r}")
        canonical = normalize_canonical(canonical)
        from_url = medium_id_from_url(canonical)
        if medium_id is not None:
            if not isinstance(medium_id, str) or not MEDIUM_ID_EXACT_RE.match(medium_id):
                raise LedgerError(f"ledger medium_id is not a 12-hex id: {medium_id!r}")
            if from_url and from_url != medium_id:
                raise LedgerError(
                    f"ledger medium_id {medium_id} contradicts its canonical "
                    f"({from_url} in {canonical})"
                )
        medium_id = medium_id or from_url

        by_canonical = self._by_canonical.get(canonical)
        by_id = self._by_id.get(medium_id) if medium_id else None

        if by_canonical is not None:
            if by_canonical.medium_id == medium_id or medium_id is None:
                return  # identical, or incoming carries no new information
            if by_canonical.medium_id is not None:
                raise LedgerError(
                    f"canonical {canonical} already has medium_id "
                    f"{by_canonical.medium_id}, refusing to rewrite it to {medium_id}"
                )
            if by_id is not None and by_id.canonical != canonical:
                raise LedgerError(
                    f"ambiguous bridge: medium_id {medium_id} already belongs to "
                    f"{by_id.canonical}, cannot also claim {canonical}"
                )
            promoted = Identity(medium_id, canonical)   # atomic promotion
            self._by_canonical[canonical] = promoted
            self._by_id[medium_id] = promoted
            return

        if by_id is not None:
            return  # URL alias of a known article: keep the original canonical

        entry = Identity(medium_id, canonical)
        self._by_canonical[canonical] = entry
        if medium_id:
            self._by_id[medium_id] = entry

    def identities(self):
        return sorted(
            (Identity(i.medium_id, i.canonical) for i in self._by_canonical.values()),
            key=lambda i: (i.medium_id or "", i.canonical),
        )

    @staticmethod
    def _checked_identity(canonical, medium_id, seen_canonicals, seen_ids):
        """Validate one ledger row and fail closed on anything ambiguous:
        an unusable canonical, a malformed id, an id that contradicts the
        canonical's own id, or a duplicate/conflicting row."""
        if not is_http_url(canonical):
            raise LedgerError(f"ledger canonical is not a usable http(s) URL: {canonical!r}")
        normalized = normalize_canonical(canonical)
        from_url = medium_id_from_url(canonical)
        if medium_id is not None:
            if not isinstance(medium_id, str) or not MEDIUM_ID_EXACT_RE.match(medium_id):
                raise LedgerError(f"ledger medium_id is not a 12-hex id: {medium_id!r}")
            if from_url and from_url != medium_id:
                raise LedgerError(
                    f"ledger medium_id {medium_id} contradicts its canonical "
                    f"({from_url} in {normalized})"
                )
        resolved = medium_id or from_url
        if normalized in seen_canonicals:
            raise LedgerError(f"duplicate ledger canonical: {normalized}")
        if resolved and resolved in seen_ids:
            if seen_ids[resolved] != normalized:
                raise LedgerError(
                    f"conflicting ledger medium_id {resolved}: "
                    f"{seen_ids[resolved]} vs {normalized}"
                )
            raise LedgerError(f"duplicate ledger medium_id: {resolved}")
        seen_canonicals.add(normalized)
        if resolved:
            seen_ids[resolved] = normalized
        return Identity(resolved, normalized)

    @classmethod
    def parse(cls, raw):
        data = json.loads(raw)
        seen_canonicals, seen_ids = set(), {}
        if isinstance(data, list):
            # legacy format: plain list of URL strings — migrate
            if not all(isinstance(u, str) for u in data):
                raise LedgerError("legacy ledger list contains non-string entries")
            return cls(
                cls._checked_identity(u, None, seen_canonicals, seen_ids) for u in data
            )
        if isinstance(data, dict):
            if data.get("version") != LEDGER_VERSION:
                raise LedgerError(f"unknown ledger schema version {data.get('version')!r}")
            if "identities" not in data or not isinstance(data["identities"], list):
                raise LedgerError(
                    "version 1 ledger must carry an 'identities' list — refusing to "
                    "treat a missing or malformed key as an empty ledger"
                )
            identities = []
            for entry in data["identities"]:
                if not isinstance(entry, dict) or "canonical" not in entry:
                    raise LedgerError(f"malformed ledger identity entry: {entry!r}")
                identities.append(
                    cls._checked_identity(
                        entry["canonical"], entry.get("medium_id"), seen_canonicals, seen_ids
                    )
                )
            return cls(identities)
        raise LedgerError(f"unknown ledger schema: {type(data).__name__}")

    @classmethod
    def load(cls, path):
        if not os.path.isfile(path):
            raise LedgerError(
                f"ledger missing: {path} — refusing to default to empty "
                "(a silent reset is how the 2026-08-03 duplicate import happened)"
            )
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        try:
            return cls.parse(raw)
        except json.JSONDecodeError as exc:
            raise LedgerError(f"ledger corrupt: {path}: {exc}") from exc

    def serialize(self):
        payload = {
            "version": LEDGER_VERSION,
            "identities": [i.as_dict() for i in self.identities()],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    def save_atomic(self, path):
        """Deterministic bytes, tmp + os.replace. Callers must invoke this
        ONLY after a batch with zero failures."""
        directory = os.path.dirname(os.path.abspath(path))
        fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".ledger-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(self.serialize())
            os.replace(tmp_path, path)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
