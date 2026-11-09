# Level 2 — Atomic Data Reconciliation & Safe Import Lab

A **real, offline SQLite + CSV reference demo**, implemented independently from ARAZVERA's private starter kits. Not a paid production integration, not a customer data migration and **not PostgreSQL**.

## Run it without external dependencies

Python 3.11+ standard library only:

~~~bash
python demo.py
python -m unittest discover -s tests -v
~~~

The demo imports bounded synthetic CSV records, previews changes without committing them, quarantines an invalid record, applies an idempotent batch, upgrades an item revision, injects a transaction failure, proves rollback and reopens the on-disk database.

## Validated behavior and contract

| API | Behavior |
| --- | --- |
| parse_inventory_csv(binary) | UTF-8, required headers, 128 KiB bound, up to 500 rows |
| DataSync.preview(tenant,source,batch_id,rows) | Real conflict analysis under a transaction followed by ROLLBACK; never changes durable rows |
| DataSync.apply(tenant,source,batch_id,rows) | Atomic SQLite BEGIN IMMEDIATE, unique scoped batch key and SHA-256 digest |
| DataSync.snapshot(tenant,source) | Tenant/source-isolated, stable-sorted current state |
| DataSync.rejections(tenant,source,batch_id) | Only item ID and reason, no customer names or raw input |
| DataSync.audit(tenant,source,batch_id) | Audit action and timestamp, no raw personal data |

For a repeated batch key with the same input digest, the engine returns the original receipt without reapplying the records. Reusing a batch key for a different payload raises BatchConflict. Newer revisions may update existing items; stale revisions and conflicting same-revision changes are rejected to a review table. Duplicate input IDs in one batch are rejected after the first valid record.

**Atomicity caveat:** SQLite is a single-node demonstration. Real integrations need customer-approved database selection, migrations, encrypted connection settings, backup, locale/format rules, transaction sizing and performance/replay tests. It does not promise reconciliation across arbitrary providers.

## Tests

**21 runnable unittest cases** include dry-run immutability, hard rollback on injected faults, 5-way concurrency, duplicate/stale revision handling, source + tenant isolation, re-open persistence, malformed CSV and safe rejection records. No paid API, no public endpoint, no GPU.

## Customer-oriented use

A bounded Level 2 paid service could include: pre-import mapping, rejected-data report, dry-run, fixed-scope migration, audit, tests and handover. The real source/target systems and any compliance requirements must be specified and authorized in each signed client project.

**Production approved:** No. **Real customer integrations tested:** None. **Synthetic transactions verified:** Yes.
