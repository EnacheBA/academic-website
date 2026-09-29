# Bogdan-Adrian Enache — academic and research website

Private review edition, compiled 29 September 2026. A dependency-free, responsive static website with 20 pages, 12 detailed project appointments, 99 bibliography records, career and teaching profiles, a portrait, and a printable professional CV.

## Build and preview

Requires Python 3. No package installation or external font/CDN is required.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4173. The JSON files in `data/` are the editable content; `scripts/build.py` renders HTML and BibTeX. `styles.css` and `app.js` supply layout, mobile navigation and bibliography filtering. All records remain readable with JavaScript disabled.

## Sources and reconciliation

- Supplied four-page Europass CV and supplied portrait.
- Shared conversation: https://chatgpt.com/share/6abb9bd1-84b0-83ed-b1d3-cd7fbd09fa83
- Google Scholar: https://scholar.google.com/citations?user=MZdHJ7MAAAAJ&hl=en — 100 records collected; metrics observed on 29 September 2026.
- ResearchGate: https://www.researchgate.net/profile/Bogdan-Adrian-Enache — 91 entries from the accessible indexed profile snapshot. Direct ResearchGate browsing was restricted.
- ORCID: https://orcid.org/0000-0001-9979-3837 and Crossref/publisher metadata.
- Official CORDIS factsheets for the European projects, and institutional publication lists for unresolved bibliography fields.

The catalogue reconciles profile duplicates, includes two ResearchGate-only records and an additional institutional bibliography record. A generic ResearchGate “Chapter” upload is retained as supplementary material. Every collected Scholar record has a preserved source link. 83 records have DOIs. A few sources abbreviate authors or omit bibliographic fields; these are labelled, not invented. `research/` holds public bibliographic provenance only. `scripts/prepare_publications.py` reconciles source data and applies `scripts/curated_metadata.py`; rerunning it overwrites manual edits in `data/publications.json`.

Open `review.html` in the generated site for uncertainties: three CV project dates, EVOSST programme naming, one battery-paper date, CAR 2026 publication status, and conflicting chapter pagination. Consortium budgets/durations are separated from personal participation.

## Privacy and deployment

Keep this repository PRIVATE. The Sites project in `.openai/hosting.json` is configured for owner-only review. Do not enable public GitHub Pages or widen site access without the owner's request. `robots.txt` and noindex are supplementary indexing controls, not authentication.

The original CV (with home address, personal telephone and family details) is not included. Only professional content, university email and the supplied portrait are deployed. No tracking, analytics, external fonts, embedded third-party media or contact-form data collection is used.

Build from the committed source, push that exact commit to the configured Sites source repository, then package `.openai/hosting.json` and `dist/` for private deployment. Do not include source research archives or credentials in the deployment archive. Credentials must never be committed.

## Validation

`python3 scripts/check.py` validates all internal links and anchors, one H1 per page, image alt text, noindex, distinct identifiers and DOIs, complete Scholar source coverage, BibTeX record counts, and exclusion of the raw CV. Browser checks cover desktop/mobile layouts, search, year filtering, empty results/reset and disclosure records.
