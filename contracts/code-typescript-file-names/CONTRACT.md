---
name: code-typescript-file-names
message: Use kebab-case source paths with dotted role suffixes; preserve tool-required names.
---

## Rules

Use lowercase kebab-case for TypeScript source directory and file names.
Mark a file's role with a lowercase dotted suffix before its extension, such as `invoice-total.test.ts`.
Use only the role suffixes the repository declares, and give each suffix one meaning.
Use a role suffix only when the file's contents match that role.
Do not use a catch-all role suffix such as `.utils`, `.helpers`, `.common`, or `.misc`; name the behavior in the file stem instead.

Match a file's stem to its primary export, changing only the case, so `invoice-card.ts` exports `InvoiceCard` or `invoiceCard`.
Give a test or example file the full stem of its subject, including the subject's role suffix.
Keep a subject's implementation, test, and example files side by side with matching stems.

Preserve names that tools or conventions require, such as `README.md`, `package.json`, framework entry files, and tool configuration dotfiles.
Keep the descriptive words of a framework-required path pattern, such as a parameter or private-folder marker, in kebab-case.
Do not rename generated files or provider-generated metadata.

## Checks

Compare each new or renamed path with kebab-case and the repository's declared role suffixes.
Run the repository's filename-casing lint rule where one exists.
Confirm each role suffix matches the file's contents and no catch-all suffix was introduced.
Confirm that tool-required and generated names are unchanged.
