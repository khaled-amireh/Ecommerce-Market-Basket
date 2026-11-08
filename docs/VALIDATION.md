# Documentation validation and integrity record

Review date: 2026-11-08. Starting HEAD:
`ad13f98afac5c646bb38cd3521d69352c2d86e0c`, branch `main`, initially clean.
This record accompanies the final documentation/contribution-guidance commit.
It intentionally does not embed its own commit hash. To list all 15 local
commits, use `git log --reverse --oneline ad13f98..HEAD`.

## Preservation results

SHA-256 was checked before each commit and again at completion against the
[full byte/hash baseline](EVIDENCE_BASELINE.md). The editable README is excluded
from the protected set. All original tracked paths remain present.

| Protected artifact | Initial bytes | Final comparison |
| --- | ---: | --- |
| `LICENSE` | 1091 | SHA-256 identical |
| `ecommerce_market_basket.ipynb` | 125761 | SHA-256 identical, including Markdown and saved outputs |
| `ecommerce_market_basket.py` | 1915 | SHA-256 identical, including existing syntax defects |
| `images/association_rules_plot.png` | 143151 | SHA-256 identical |
| `requirements.txt` | 45 | SHA-256 identical |

No data file existed in the initial workspace; none was acquired or created.
No mining, notebook execution, output regeneration, code formatting, dependency
installation, history rewrite, or push was performed. Temporary rendering files
were kept outside the repository. Existing user changes were absent at baseline.

## Documentation and evidence checks

| Check | Method and result |
| --- | --- |
| README composition | Exactly 18 numbered second-level case-study sections |
| Markdown | Parsed with installed Mistune and table plugin; consistent table columns, valid separator rows, Python snippets parse |
| Local links | Relative file targets, image paths, README anchors, and script line references checked |
| Tracked structure | README tree compared with `git ls-files`; includes only actual project paths |
| Banner | XML valid; 1200 × 400 viewBox; no scripts, image embeds, remote references, or external fonts; all five requested palette colors |
| Banner appearance | Rendered in headless Chrome and visually inspected; original retail-node/basket composition, legible labels, no fabricated metric |
| Mermaid | README flowchart rendered successfully with Mermaid 11.4.1 in a temporary browser preview; one SVG, no parse error; stage order checked against notebook |
| README appearance | Local HTML preview visually inspected for hero, navigation, and tables; GitHub's own renderer may differ |
| Original visuals | Tracked PNG and embedded notebook PNG both viewed; resolution/provenance distinction recorded |
| Saved values | All ten itemset supports and thirty rule metric values matched to notebook HTML; fully readable pair names checked |
| Arithmetic | Metric example and rounded reciprocal teacup-rule consistency checked; no source-data recomputation claimed |
| Source syntax | In-memory parse confirms script failure at line 34; all seven notebook code cells parse |
| Audit coverage | Fourteen distinct findings; 0 Critical, 2 High, 9 Medium, 3 Low; eight Confirmed, five Potential, one Unverified |
| Git scope | Only README, 13 new documentation files, CONTRIBUTING, and one SVG differ from starting HEAD |
| Git whitespace | `git diff --check ad13f98..HEAD` and staged-diff checks pass |
| Git history | Fifteen nonempty local Conventional Commits; protected-file hashes checked before each |

The final commit records contribution standards, this validation evidence,
the exact final tree, and rendering/wording corrections found during review.
The banner is tracked in its own earlier commit; its final palette includes
Obsidian Navy, Deep Indigo, Electric Cyan, Refined Violet, and Soft White.

## External references and remaining uncertainties

Web-tool checks reached the repository, author GitHub, UCI source page, pandas
API, mlxtend guides, and mlxtend source. Kaggle resolved but provided no readable
metadata, so its attribution remains a repository claim. The DOI redirected to
the expected UCI path, but the tool failed on the redirect. The requested
[portfolio URL](https://portfolio-1kpn.onrender.com) was inaccessible via that
tool and is retained as supplied. Local shell HTTP requests were blocked by
the environment; they are not evidence that these websites are down.

No full input identity, local row count/date coverage, cleaning counts, basket
shape, total itemsets/rules, complete clipped rule names, historical dependency
versions, or commercial effects could be established. See the
[audit](CODE_AUDIT.md), [provenance record](DATA_PROVENANCE.md), and
[saved-output ledger](VERIFIED_RESULTS.md). No independent reproduction was
claimed. The repository is ready for documentation review and owner-controlled
publishing, with the implementation limitations explicitly disclosed.
