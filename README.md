# Bogdan-Adrian Enache — academic and research website

Public academic website, with bibliographic data compiled on 29 September 2026.

Website: https://enacheba.github.io/academic-website/ A dependency-free, responsive static website with 20 pages, 12 detailed project appointments, 99 bibliography records, career and teaching profiles, a portrait, and a printable professional CV.

## Build and preview

Requires Python 3. No package installation or external font/CDN is required.

```sh
python3 scripts/build.py --public --output docs
python3 scripts/check.py --public --output docs
python3 -m http.server 4173 --bind 127.0.0.1 --directory docs
```

Open http://127.0.0.1:4173. The JSON files in `data/` are the editable content; `scripts/build.py` renders HTML and BibTeX. `styles.css` and `app.js` supply layout, mobile navigation and bibliography filtering. All records remain readable with JavaScript disabled.

## Sources and reconciliation

- Supplied four-page Europass CV and supplied portrait.
- Google Scholar: https://scholar.google.com/citations?user=MZdHJ7MAAAAJ&hl=en — 100 records collected; metrics observed on 29 September 2026.
- ResearchGate: https://www.researchgate.net/profile/Bogdan-Adrian-Enache — 91 entries from the accessible indexed profile snapshot. Direct ResearchGate browsing was restricted.
- ORCID: https://orcid.org/0000-0001-9979-3837 and Crossref/publisher metadata.
- Official CORDIS factsheets for the European projects, and institutional publication lists for unresolved bibliography fields.

The catalogue reconciles profile duplicates, includes two ResearchGate-only records and an additional institutional bibliography record. A generic ResearchGate “Chapter” upload is retained as supplementary material. Every collected Scholar record has a preserved source link. 83 records have DOIs. A few sources abbreviate authors or omit bibliographic fields; these are labelled, not invented. `research/` holds public bibliographic provenance only. `scripts/prepare_publications.py` reconciles source data and applies `scripts/curated_metadata.py`; rerunning it overwrites manual edits in `data/publications.json`.

Open `sources.html` in the public site for bibliographic provenance and source discrepancies: three CV project dates, EVOSST programme naming, one battery-paper date, CAR 2026 publication status, and conflicting chapter pagination. Consortium budgets/durations are separated from personal participation.

## Public deployment

This repository and its GitHub Pages website are public, as requested by the owner. GitHub Pages publishes the generated `docs/` directory from the `main` branch. To update the live website, edit the source, run the build and checks above, then commit the source and regenerated `docs/` files and push `main`. GitHub deploys the committed static pages automatically; no custom workflow credentials are needed.

The public edition has indexable pages, canonical links, a sitemap and a public Sources page. It omits the private-review banner, owner review page and conversation link.

The original CV (with home address, personal telephone and family details) is not included. Only professional content, university email and the supplied portrait are deployed. No tracking, analytics, external fonts, embedded third-party media or contact-form data collection is used.

The earlier Sites URL remains a separate owner-only review snapshot. `.openai/hosting.json` identifies it; changing GitHub visibility does not change its audience. To build that review edition locally, run `python3 scripts/build.py` and `python3 scripts/check.py` without `--public`. Do not publish review output to GitHub Pages. Credentials must never be committed.

## Validation

`python3 scripts/check.py --public --output docs` validates all internal links and anchors, one H1 per page, image alt text, public indexing and canonical links, distinct identifiers and DOIs, complete Scholar source coverage, BibTeX record counts, and exclusion of the raw CV and private review page. Browser checks cover desktop/mobile layouts, search, year filtering, empty results/reset and disclosure records.
