# Shared junk-name regex, sourced by build_and_check.sh and check_site.sh so
# the negative tests exercise exactly the pattern production uses.
# Catches sync-duplicate names with one-or-more digits and ANY extension
# ("name 12", "name (3)", "favicon 12.png", "update-news 12.yml") plus backup
# suffixes. Legitimate slugs/filenames in this repo never contain
# space-digit sequences.
# shellcheck disable=SC2034
JUNK_RE=' \(?[0-9]+\)?($|\.[^/]+$)|\.bak$|\.backup$|\.before-remove$|~$'
