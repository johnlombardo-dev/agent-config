# Persistence, migration, and recovery

## Select when

The target changes durable schemas, migrations, transactions, indexes, caches backed by source rows, checkpoints, files, backups, restore, deduplication, or crash/restart behavior.

## Review

- State atomicity, consistency, identity, retention, and recovery invariants.
- Enumerate the durable artifact set; backup and restore must round-trip every retained artifact needed for observable reads.
- Inject failure between every multi-write step and verify rollback or resumable state.
- Exercise fresh creation, populated upgrade, downgrade/newer-version refusal, reopen, restart, duplicate application, and corrupted or partial artifacts.
- Compare source rows with derived indexes or caches after insert, update, delete, reclassify, rebuild, and rollback.
- Check atomic promotion, fsync/rename assumptions, private modes, backup overwrite policy, and restoration fidelity.

## Evidence

Use transactional failure injection, reopen tests, integrity queries, source/index differentials, and crash-shaped fixtures. Escalate to concurrency for multiple writers or operations for filesystem and deployment assumptions.
