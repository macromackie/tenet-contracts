---
name: code-package-shape
message: Give every package the same closed root and source root, so that a listing of either reads as a table of contents.
requires-tenet: 0.11.0
---

## Rules

Apply these rules to every package folder that the repository's shape policy declares by path pattern.
Keep exactly three entries in a package's root: `README.md`, the package manifest, and one source folder, whose name the policy declares.
Keep any other entry in a package's root only when a deploy tool reads it there, and declare it in the policy for that one package with its reason.
Declare each entry that a tool generates in a package, such as an installed dependency folder or build output, in the policy with its reason, and keep it out of version control.
Keep a tool's settings out of the package root; `code-tool-configuration-folder` says where they live.
Name a package's folder for the last segment of the name in its manifest, such as `orders` for `@acme/orders`.

Declare the entry file names of a source root, such as an index module and a main module, and its role file names, as `code-module-file-roles` defines roles.
Give a source root one of two shapes, told apart by whether it holds a folder.
A flat source root holds only files, at most a declared maximum number of them; the shipped policy sets 12, which a repository may override.
A foldered source root holds folders, entry files, and role files, and no other file.
When a change would put a flat source root over its maximum, move the modules that serve one behavior into folders in the same change, instead of raising the maximum.
Never leave a module that is neither an entry file nor a role file beside a folder in a source root.
Name and scope each folder as `code-module-structure-and-control-flow` requires for a module, and keep each folder within the limits that `code-folder-size` declares.

Violation: `packages/orders/src/` holds `index.ts`, the folder `totals/`, and `read-tax.ts`, a module that is neither an entry file nor a role file.
Allowed: `read-tax.ts` moves into `packages/orders/src/taxes/`, and the source root lists `index.ts`, `errors.ts`, `taxes/`, and `totals/`.
Violation: `packages/invoices/` holds lint settings beside its manifest, or its manifest names the package `@acme/billing`.
Allowed: `packages/invoices/` holds `README.md`, its manifest, which names `@acme/invoices`, and `src/`.

## Checks

Run the checker in this contract's `assets/` folder from the repository root with the repository's shape policy, where its runtime can run.
For each deploy entry a change adds to the policy, does the named deploy tool refuse to read the file from anywhere else?
For each role file name a change adds to the policy, does every file with that name hold only that role?
For each folder a change adds to a source root, do its modules serve one behavior that the folder's name states?
