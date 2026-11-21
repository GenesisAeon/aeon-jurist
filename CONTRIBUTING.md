# Contributing to aeon-jurist

aeon-jurist is **a map, not a verdict**. Contributions are welcome if they keep it that way: every record must be traceable to a primary source, and its limits must be visible.

## Adding a case or a building block

Open an issue or pull request with one record per item, using this template:

```yaml
id: XX-SHORTNAME-YYYY          # jurisdiction code, short name, year
kind: case | context           # case = a decision/statute on legal status; context = building block (see J3b §6)
title: "Court/statute, number, date"
jurisdiction: ""
year: 0000
entity_type: fluss | oekosystem | natur_allgemein | tier | ki | software_rolle   # cases only
outcome: gewaehrt | abgelehnt | vorgeschlagen | aufgehoben | offen               # cases only
status_today: in_kraft | ausgesetzt | aufgehoben | nicht_umgesetzt | unbekannt
criteria: {K-INT: ja|nein|strittig|nicht_geprueft, K-REP: …, K-STA: …, K-DUT: …, K-CUL: …, K-AGN: …}
quote: "verbatim passage in the original language"
primary_source: {url: "", type: "judgment / statute / official copy", retrieved: YYYY-MM-DD}
check_depth: volltext | volltext_kopie | volltext_uebersetzung | auszug | sekundaer
checked_by: "who read the source (person or agent)"
note: "appeals, stays, later amendments; anything that limits the record"
```

## Rules

1. **Primary source or candidate.** Without a primary source that someone actually read, an item goes to `kandidaten`, not into the collection. Press reports and secondary summaries are fine as pointers, never as the only basis.
2. **Verbatim quote.** The quote must be findable in the linked source. Paraphrases go into `note`.
3. **Check depth is honest.** Say how the source was read. A blocked page is not `volltext`.
4. **Later history matters.** Check for appeals, stays and repeals. A first-instance grant that was overturned is recorded as `aufgehoben` (see AR-SANDRA-2015).
5. **Law and argument stay separate.** Records describe what a court or legislature decided. Interpretations belong in the docs, marked as argument.
6. **No unauthorised copies.** No shadow libraries or pirated mirrors, also not for "just checking".
7. **Disclosure.** Say if you or your organisation have a stake in the question (for example, an AI developer contributing on AI status). The project's own analyses disclose that they were written with an AI.
8. **Tests.** New records must pass the contract tests (`pytest`). If a rule needs a new test, add it.

## What we will not merge

- Similarity scoring that invents analogies for entities without sourced cases (`landscape()` returns an empty map on purpose).
- A protection "level" or prediction derived from the map.
- Records whose only source is a summary, a model output or memory.

Not legal advice.
