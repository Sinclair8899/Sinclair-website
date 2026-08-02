"""Offline transform layer for the Medium/Substack importer — stdlib ONLY.

The fetch layer (feedparser/requests) lives in import_medium.py; nothing in
this module may import third-party packages or touch the network, so the
whole layer is testable offline (.github/scripts/test_import_medium.py).

Description contract (Step 5):
- Parse feed HTML with html.parser honoring block boundaries (p, h1-h6,
  li, blockquote, figure, figcaption) so text from adjacent blocks never
  fuses into one word or sentence.
- Headings, figure/figcaption content, bylines, author names, series
  labels, and Field Note/version blocks never reach the description.
- HTML entities are decoded; U+00A0 and all whitespace runs normalize to
  a single space.
- The description is the EARLIEST run of one or two complete body
  sentences, in document order, whose joined length lands in 120-160
  Unicode code points. Nothing is cut mid-word or mid-sentence and no
  claim is invented.
- If no qualifying sentence group exists, DescriptionError is raised and
  the caller must skip the article (and must NOT record it as imported).
"""
import re
from html.parser import HTMLParser

DESCRIPTION_MIN = 120
DESCRIPTION_MAX = 160

BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote"}
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
FIGURE_TAGS = {"figure", "figcaption"}

NOISE_PATTERNS = [
    re.compile(r"^\s*by\s+\S+", re.IGNORECASE),          # "By ..."
    re.compile(r"sinclair\s*huang", re.IGNORECASE),       # author name
    re.compile(r"po-sung\s*\(\s*sinclair\s*\)", re.IGNORECASE),
    re.compile(r"notes\s*[|｜]\s*(part|article)", re.IGNORECASE),  # series label
    re.compile(r"^\s*field\s+note", re.IGNORECASE),       # version block
]

SENTENCE_END = re.compile(r'([.!?…。！？]["”』」)]?)(?=\s|$)')


class DescriptionError(ValueError):
    """No compliant 120-160 code-point sentence group exists."""


class _BlockCollector(HTMLParser):
    """Collects normalized text per block; figure/figcaption swallowed."""

    def __init__(self):
        super().__init__(convert_charrefs=True)  # entities decoded here
        self.blocks = []      # (kind, text): kind in {"text", "heading"}
        self._figure_depth = 0
        self._open = []       # stack of (tag, [chunks])

    def handle_starttag(self, tag, attrs):
        if tag in FIGURE_TAGS:
            self._figure_depth += 1
            return
        if self._figure_depth:
            return
        if tag in BLOCK_TAGS:
            self._open.append((tag, []))
        elif tag == "br" and self._open:
            self._open[-1][1].append(" ")

    def handle_endtag(self, tag):
        if tag in FIGURE_TAGS:
            self._figure_depth = max(0, self._figure_depth - 1)
            return
        if self._figure_depth:
            return
        if self._open and tag == self._open[-1][0]:
            _tag, chunks = self._open.pop()
            text = normalize_whitespace("".join(chunks))
            if text:
                kind = "heading" if tag in HEADING_TAGS else "text"
                self.blocks.append((kind, text))

    def handle_data(self, data):
        if self._figure_depth:
            return
        if self._open:
            self._open[-1][1].append(data)


def normalize_whitespace(text):
    """U+00A0 and every whitespace run become a single space."""
    return re.sub(r"\s+", " ", text.replace(" ", " ")).strip()


def blocks_from_html(html):
    collector = _BlockCollector()
    collector.feed(html)
    return collector.blocks


def is_noise(text):
    return any(p.search(text) for p in NOISE_PATTERNS)


def sentences_of(text):
    """Split a block into complete sentences; a trailing fragment without a
    terminal mark is NOT a sentence and is dropped."""
    out, last = [], 0
    for m in SENTENCE_END.finditer(text):
        out.append(text[last:m.end(1)].strip())
        last = m.end(1)
    return [s for s in out if s]


def description_from_html(html):
    """Earliest 1-2 complete body sentences landing in 120-160 code points."""
    candidates = []
    for kind, text in blocks_from_html(html):
        if kind != "text" or is_noise(text):
            continue
        candidates.extend(sentences_of(text))
    for i, sentence in enumerate(candidates):
        if DESCRIPTION_MIN <= len(sentence) <= DESCRIPTION_MAX:
            return sentence
        if i + 1 < len(candidates):
            pair = f"{sentence} {candidates[i + 1]}"
            if DESCRIPTION_MIN <= len(pair) <= DESCRIPTION_MAX:
                return pair
    raise DescriptionError(
        f"no complete 1-2 sentence group lands in "
        f"{DESCRIPTION_MIN}-{DESCRIPTION_MAX} code points "
        f"({len(candidates)} candidate sentences)"
    )


def yaml_quote(value):
    """Safe double-quoted YAML scalar (single line by construction)."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def front_matter(title, date_str, tags, description, canonical):
    """Front matter for an imported article. cta is EXPLICITLY subscribe —
    the dispatcher errorf-fails builds on missing cta, and imports must
    never silently become advisory pages. primary_cluster is deliberately
    absent: cluster assignment is an editorial decision, never guessed."""
    tags_str = ", ".join(yaml_quote(t) for t in tags) if tags else '"AI", "Research"'
    return (
        "---\n"
        f"title: {yaml_quote(title)}\n"
        f"date: {date_str}\n"
        "draft: false\n"
        f"tags: [{tags_str}]\n"
        f"description: {yaml_quote(description)}\n"
        f"canonical: {yaml_quote(canonical)}\n"
        'cta: "subscribe"\n'
        "---\n\n"
    )
