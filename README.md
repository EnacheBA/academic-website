# Bogdan-Adrian Enache — academic and research website

Public academic website, with bibliographic data compiled on 29 September 2026.

Website: https://enacheba.github.io/academic-website/ A dependency-free, responsive static website with 19 pages, 12 detailed project appointments, 99 bibliography records, career and teaching profiles, a portrait, and a printable professional CV.

## Build and preview

Requires Python 3. No package installation or external font/CDN is required.

```sh
python3 scripts/build.py --public --output docs
python3 scripts/check.py --public --output docs
python3 -m http.server 4173 --bind 127.0.0.1 --directory docs
```

Open http://127.0.0.1:4173. The JSON files in `data/` are the editable content; `scripts/build.py` renders HTML and BibTeX. `styles.css` and `app.js` supply layout, mobile navigation and bibliography filtering. All records remain readable with JavaScript disabled.

## Content

The publication catalogue includes authors, titles, dates, venues, DOIs, and volume and pagination details where available. Project pages distinguish personal appointments from consortium dates and budgets. The build exports bibliographic data without editorial notes or research provenance.

`scripts/prepare_publications.py` prepares the catalogue and applies `scripts/curated_metadata.py`; rerunning it overwrites manual edits in `data/publications.json`. The `research/` directory supports this maintenance process and is not deployed to the website.

## Public deployment

This repository and its GitHub Pages website are public, as requested by the owner. GitHub Pages publishes the generated `docs/` directory from the `main` branch. To update the live website, edit the source, run the build and checks above, then commit the source and regenerated `docs/` files and push `main`. GitHub deploys the committed static pages automatically; no custom workflow credentials are needed.

The public edition has indexable pages, canonical links and a sitemap. It omits the private-review banner and conversation link.

Only professional content, university email and the portrait are deployed. No tracking, analytics, external fonts, embedded third-party media or contact-form data collection is used.

The earlier Sites URL remains a separate owner-only review snapshot. `.openai/hosting.json` identifies it; changing GitHub visibility does not change its audience. To build that review edition locally, run `python3 scripts/build.py` and `python3 scripts/check.py` without `--public`. Do not publish review output to GitHub Pages. Credentials must never be committed.

## Validation

`python3 scripts/check.py --public --output docs` validates all internal links and anchors, one H1 per page, image alt text, public indexing and canonical links, distinct identifiers and DOIs, complete Scholar source coverage, BibTeX record counts, and exclusion of the raw CV and private review page. Browser checks cover desktop/mobile layouts, search, year filtering, empty results/reset and disclosure records.
