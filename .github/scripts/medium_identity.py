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


def canonical_from_markdown(text):
    """The canonical: front-matter value of a source file, or None.
    Front matter is delimited by FULL '---' lines — never split on the
    substring '---' (Medium canonicals contain six-dash runs)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            return None
        match = re.match(r'^canonical:\s*["\']?(https?://[^"\']+)["\']?\s*$', line)
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
        self._remember(identity)

    def identities(self):
        return sorted(
            (Identity(i.medium_id, i.canonical) for i in self._by_canonical.values()),
            key=lambda i: (i.medium_id or "", i.canonical),
        )

    @classmethod
    def parse(cls, raw):
        data = json.loads(raw)
        if isinstance(data, list):
            # legacy format: plain list of URL strings — migrate
            if not all(isinstance(u, str) for u in data):
                raise LedgerError("legacy ledger list contains non-string entries")
            return cls(
                Identity(medium_id_from_url(u), normalize_canonical(u)) for u in data
            )
        if isinstance(data, dict):
            if data.get("version") != LEDGER_VERSION:
                raise LedgerError(f"unknown ledger schema version {data.get('version')!r}")
            identities = []
            for entry in data.get("identities", []):
                if not isinstance(entry, dict) or "canonical" not in entry:
                    raise LedgerError(f"malformed ledger identity entry: {entry!r}")
                identities.append(Identity(entry.get("medium_id"), entry["canonical"]))
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
