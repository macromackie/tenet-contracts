---
name: security-server-secret-storage
message: Encrypt held secrets bound to their record, keep keys outside the database, and never log secret values.
---

## Rules

Encrypt every upstream credential and other held secret with authenticated encryption before storing it.
Never reuse a nonce under the same key, such as by drawing a fresh random nonce for every encryption.
Bind each ciphertext to its owning record through associated data, such as the record and owner IDs, so it cannot be moved to another record.
Derive the associated data from the record being read, never from values stored beside the ciphertext.
Store the key version with each ciphertext, and keep earlier versions able to decrypt until their ciphertexts are re-encrypted.
Keep encryption keys outside the database that holds the ciphertext.
Use a distinct key for each purpose and application; never reuse an encryption key for signing or across applications.

Supply production secrets through the deployment's secret store, never through source, public configuration, or built assets.
Decrypt a secret only in the component that uses it, and never return it to clients.
Keep held secrets out of public records, API responses, browser storage, server-rendered pages, logs, audit records, error messages, and release artifacts.
Refer to secret-holding records by identifier in logs and audit records.

Give the runtime database credential data access to its own schema only, with no schema-change rights.
Run migrations and data publication with a separate credential that the runtime never receives.

## Checks

Copy a ciphertext to another record and confirm decryption fails.
Inspect the runtime's database grants and confirm it cannot change schema or read other schemas or migration state.
Confirm encryption keys are absent from the database and the migration credential is absent from the runtime environment.
Search logs, audit records, error responses, rendered pages, and built artifacts for secret values and credential-bearing URLs.
Rotate the key version and confirm existing ciphertexts still decrypt until re-encrypted.
