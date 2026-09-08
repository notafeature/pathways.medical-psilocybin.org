# pathways.medical-psilocybin.org

One pathway per role under New Mexico's medical psilocybin rules (producers, testing laboratories, certifying clinicians, practitioners, facilitators, healing centers, educational programs, patients), and a browser-side drafter for the two documents 7.35.2.8 NMAC describes. The rules site (`NMMPAB_Rules-Draft-Analysis`) states what the rule requires; this site states where each item comes from, agency by agency. Its `ARCHITECTURE.md`, `OPERATIONS.md`, and `WRITING-STANDARD.md` govern this project too.

| Path | What it is |
|---|---|
| `public/index.html` | The pathways, one door per role, each with its status |
| `public/<role>/` | One folder per role: `producers/` (six guide pages and the drafter), `testing/`, `clinicians/`, `practitioners/`, `facilitators/`, `healing-centers/`, `educational-programs/`, `patients/` (one page each). Each page carries marker pairs (header, footer, counter, and in `producers/` a subnav) that `tools/build.py` fills |
| `public/_chrome.html` | The shared header and footer, edited once |
| `public/producers/_subnav.html` | The producer pathway's second navigation line, stamped into every page in that folder |
| `public/_redirects` | The first day's addresses (`/zoning` and the rest), 301 to their `/producers/` homes; read by the asset host |
| `public/style.css` | A copy of the rules site's stylesheet plus a short block of pathways-only rules at the end; refresh the copy from `docs/style.css` there when it changes and keep the block |
| `public/producers/attestation.html` | The drafter. Plain JavaScript in the page; nothing typed leaves the browser |
| `tools/build.py` | Stamps the chrome, a folder's subnav, and the counter beacon; fails on an em dash or on a root-absolute link that resolves to no file; `--check` fails if a page is out of date |
| `wrangler.jsonc` | Deploy config: Worker `medical-psilocybin-pathways`, custom domain `pathways.medical-psilocybin.org` |

Every requirement is cited to the rule, to the subsection and page of the published text; a proposed rule is cited as proposed and marked not in effect. Committee outlines, minutes, and other documents that predate a rule never support a requirement; they appear only in a labeled block that checks each item against the adopted text. Local steps are cited to the page of the agency that administers them, with the date read. Jurisdictions are added one at a time, each with the same rows as Santa Fe; a facility-address selector is planned once a third exists. Nothing here names who compiles it. No em dashes.

```
python3 tools/build.py && npx wrangler@4 deploy --config ./wrangler.jsonc
```
