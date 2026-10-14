# Production contract

| Stage | Inputs | Actions | Output/destination | Completion criterion |
|---|---|---|---|---|
| Retrieve | Invocation/profile/connectors | Read current sources, history, editions and folders | Private context/snapshots | Core evidence accessible; missing items explicit |
| Align | Context/duration | Define scope, sequence, outcomes and assessment | Master | No invented syllabus or held-class facts |
| Author | Alignment/references | Complete teaching, derivations, examples, tasks and marking | Master/figures/code | Stable IDs and traceable science |
| Build | Valid master/dependencies | Generate role-filtered outputs | Student/instructor exports | Required files parse; hashes recorded |
| Verify | Build/sources/checks | Review thirteen gates and repair | Private evidence/register | All critical gates pass on current hashes |
| Stage | Content approval/allowlist | Regenerate public subset | GITHUB READY | No private notes or active assessments |
| Deliver | Outputs/IDs/access policy | Upload/update/reconcile/read back | Course folders/receipts | Every required output verified |
| Learn | Actual class evidence | Record misconceptions and timing | Private teaching history | Plans distinguished from held classes |

## Thirteen gates

1. Syllabus alignment: current official evidence, topic coverage, official versus derived outcomes.
2. Continuity: actual previous teaching, next plan, sequencing rationale, exam coverage and numbering.
3. Prerequisites: diagnostic evidence or an explicit readiness/remediation plan; enrolment alone proves nothing.
4. Outcomes: measurable actions, teaching and assessment coverage at appropriate cognitive demand.
5. Physics/content: independent review of assumptions, signs, interpretation, conventions, regime and domain.
6. Derivations: notation, geometry, assumptions, intermediate steps, numbered equations, units and verified results.
7. Units/numerics: independent route/reference, dimensions, limiting cases, shared constants and tolerances.
8. Sources: actual access/edition, checked claim links and data provenance; resolve unchecked core claims.
9. Assessment: accurate keys, marking, ambiguity, difficulty, timing and delayed-solution treatment.
10. Timing: explanation, board work, attempts, discussions, transitions, break, exit and contingency fit duration; cut order protects outcomes.
11. Rendering: individually inspect every page/slide, math, figures, writing space, printing and editable sources; scan student notes, hidden slides, comments and metadata.
12. Functionality: execute calculations/tool tests, edge cases, offline/mobile/keyboard behavior and static fallback. If no tool is justified, document not_applicable with evidence.
13. Delivery/public safety: verify current hashes, parent folders, effective permissions, opening and allowlist. Distinguish staged/uploaded/published.

Evidence receipts are records, not scientific proof. The reviewer must inspect evidence. Only gate 12 may be not_applicable. Content-ready requires gates 1-12; delivered requires gate 13 and every delivery receipt. Hash or evidence changes invalidate approvals.

## Minimum structure

COURSE/SESSION/STUDENT FILES: preview-and-diagnostic.pdf; lecture-reference.pdf (key terms, readings, distinct worked examples); worksheet.pdf; exit-assessment.pdf; follow-up-and-assignment.pdf; derivations.pdf; student-deck.pptx/pdf; optional exercise.html and static-fallback.pdf.

Private INSTRUCTOR ONLY: teaching-plan.pdf (brief, alignment, clocked run sheet, cut order, checklist and feedback interpretation); solutions-and-marking.pdf; classroom-deck.pptx; source-register.csv; manifest.json; sources/ and evidence/.

GITHUB READY: README.md, lecture notes, approved reference/derivation exports and optional exercise/assets. Never publish active exit/graded assessments, instructor notes, answers or private master. Never maintain a second content master. Keep named assessments and anonymous feedback separate if required for anonymity.

## Delivery/recovery

Preserve user organization and established access. An instructor folder under a public/shared ancestor is unsafe. Verify permission inheritance and choose a separate private destination if necessary. Do not automatically share new files with everyone. Do not assume upload success means student access works.

Before replacing a file, verify tracked ID, parent and current remote version; stop for concurrent changes. A failed upload may have created a remote file: inspect destination for the exact name/hash before retrying. Record remote ID, downloaded/readback hash, parent, opening evidence and permission evidence. Plan receipts are not verified receipts. Retain the previous approved version until replacement release succeeds.

Use bounded retries, checkpoint after each success, and status to resume. Changed output hash schedules update; unchanged verified hash schedules skip. Missing/stale receipt, permission failure, ambiguous target, hash mismatch or export failure blocks delivered release. GitHub publication requires session authorization; staging is the default.

## Defaults/dependencies

No assumed duration, examination weighting, due date, institutional approval, held-class record or textbook page. Source access/correctness gates cannot be auto-passed. Runtime: Python, Pandoc, XeLaTeX, pdftoppm, pypdf, Pillow; supported Node artifact-tool for decks. Pin dependency versions for each build. Retain installed fonts and licence provenance. The bundled Caveat font (SIL OFL) provides handwriting-like prose; install it with fontconfig before building. Mathematical notation stays typeset, with its editable LaTeX retained. Handwriting prose must remain high contrast; mathematics stays typeset.

Store private profiles and executable resources in Course Control. Git-sync generic resources without private locators on an authorized feature branch. A pushed branch is neither native skill registration nor public course publication. A future agent can retrieve the individual resources from Drive if the local skill is unavailable.
