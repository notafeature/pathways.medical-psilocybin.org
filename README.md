# pathways.medical-psilocybin.org

Practical guides for applicants under New Mexico's medical psilocybin rules, and a browser-side drafter for the two documents 7.35.2.8 NMAC describes. The rules site (`NMMPAB_Rules-Draft-Analysis`) states what the rule requires; this site states where each item comes from, agency by agency. Its `ARCHITECTURE.md`, `OPERATIONS.md`, and `WRITING-STANDARD.md` govern this project too.

| Path | What it is |
|---|---|
| `public/*.html` | The pages. Each carries three marker pairs (header, footer, counter) that `tools/build.py` fills from `public/_chrome.html` |
| `public/_chrome.html` | The shared header and footer, edited once |
| `public/style.css` | A copy of the rules site's stylesheet; refresh from `docs/style.css` there when it changes |
| `public/attestation.html` | The drafter. Plain JavaScript in the page; nothing typed leaves the browser |
| `tools/build.py` | Stamps the chrome and the counter beacon; `--check` fails if a page is out of date or carries an em dash |
| `wrangler.jsonc` | Deploy config: Worker `medical-psilocybin-pathways`, custom domain `pathways.medical-psilocybin.org` |

Every claim on a guide page is cited to the rule or to the page of the agency that administers the item, with the date it was read stated on the page. Jurisdictions are added one at a time, each with the same rows as Santa Fe. Nothing here names who compiles it. No em dashes.

```
python3 tools/build.py && npx wrangler@4 deploy --config ./wrangler.jsonc
```
