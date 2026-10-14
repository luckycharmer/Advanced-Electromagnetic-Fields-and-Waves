---
name: lecturekit
description: Build, verify, resume and deliver reproducible lecture kits for any course. Use for /lecturekit, $lecturekit, or complete lecture-kit production. Retrieve current course context, author one master, generate student and instructor outputs, and block unverified releases.
---

# Lecture Kit

Interpret `/lecturekit COURSE DATE-OR-NUMBER "TOPIC" MINUTES` as an agent workflow invocation. Parse relative dates in Asia/Karachi. Retrieve missing session identifiers; never infer a held class from an existing folder. Read [production.md](references/production.md) and [content-model.md](references/content-model.md). Run `python scripts/lecturekit.py doctor`.

## Defaults

English, precise academic language, SI unless the topic requires another convention, A4 dark high-contrast PDFs, 16:9 editable PPTX. Separate handwritten-style derivation prose with legible typeset mathematics. No ZIP, Google Docs, unsolicited model branding/signatures or promotional links. Preserve attribution, licences and required disclosure. Instructor files/source master private. Preserve sharing; never silently broaden access. GitHub-ready means staging, not published. Require actual duration; never borrow another course's duration. Reserve 5% contingency and account for every minute. Use measurable derived lecture outcomes without claiming they are official CLOs. Preserve instructional worked examples; control active assessment answers.

## Execute in dependency order

1. **Retrieve:** read current course profile, official syllabus, prerequisites, textbook editions, actual previous teaching, next plan, assessment coverage and destination metadata. Record source IDs, versions/modification dates, access times, snapshots and hashes. Use profile seeds only as locators. Find `LectureKit Production System` in Course Control if local resources are missing; restore individual files. Discover a new course rather than guessing. Search missing inputs, continue independent work and request only essential unresolved information once.
2. **Initialize:** run `init --course COURSE --session SESSION --topic TOPIC --duration MINUTES --out WORKDIR`. Fill `master.json` completely. Use stable outcome, equation, constant, source, claim, question and slide IDs. Never edit generated copies.
3. **Author:** map outcomes to teaching and assessment. Supply concepts, geometry, assumptions, full derivations, readings, distinct worked examples, diagnostic, worksheet, exit, follow-up/assignment, reflection, instructor solutions/marking, logistics and a minute-by-minute run sheet. Verify science independently. Add tools only for identified instructional value and provide static fallbacks.
4. **Validate/build:** run `validate` then `build`. Use active PDF/Presentations skills and the supported runtime. The generator exports role-filtered PDFs, editable equations, classroom/student decks, private source register and a hash manifest. A missing dependency is a blocker, not permission to fabricate an export. Resolve handwriting-font availability; record limitations before rendering gate passes.
5. **Review:** execute thirteen distinct gates listed in production.md. Save actual evidence under evidence/ and use `record-gate`. Receipts must reference inspected evidence, reviewer, current master and manifest hashes. Scripts cannot prove physics or visual correctness. Correct the master, rebuild and recheck affected dependencies; stale receipts are rejected.
6. **Content release:** run `release --phase content`. Then `stage-public` applies an allowlist and regenerates safe exports. Inspect notes, hidden slides, metadata, comments, embedded assets and HTML for leakage. Preserve required disclosure; do not delete it to satisfy a scanner.
7. **Deliver:** run `delivery-plan`, discover current connected tool schemas, verify destination access, upload/update individual files, preserve tracked IDs and record readback/hash/opening/permission evidence using `record-delivery`. Use a separate private destination outside any broadly shared ancestor. Reconcile ambiguous or interrupted uploads before creating again.
8. **Finalize:** pass gate 13 and run `release --phase delivered`. Report content, delivery and GitHub publication separately. Update teaching history only with evidence the class occurred. Record post-class outcome evidence for the next kit.

Use `status` to resume. Changed content/artifacts invalidates receipts. Retry transient operations twice, preserve checkpoints and mark persistent failures blocked. Never label unchecked components Done or promise zero errors. Keep private course profiles outside public git. Do not claim native Skills-page registration unless the supported save mechanism succeeds.
