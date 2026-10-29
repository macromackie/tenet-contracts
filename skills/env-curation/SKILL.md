---
name: env-curation
description: Add, replace, or remove one value in a repository's tracked dotenv file without printing the value, and check the edit tool end to end with fake values.
license: MIT
compatibility: Needs Node 22.18 or later, which runs TypeScript without a loader, and npm; the end-to-end check also needs mise.
---

# Curate a dotenv file

Use this skill when a task adds, replaces, or removes a named value in a dotenv file that a task runner loads, such as
the `.env` file that mise reads through `_.file`. Install it with Tenet 0.11.0 or later:

```sh
tenet skills add tenet/env-curation
npm ci --ignore-scripts --prefix .agents/skills/env-curation/scripts
```

The tool's one dependency is effect, pinned in `scripts/package.json` and its lockfile. Installing with
`--ignore-scripts` runs no package code.

## Edit one key

Run each command from the repository root, with the file's path as the first argument after the command:

```sh
node .agents/skills/env-curation/scripts/env-tool.mts set .env NAME                       # Prompt with echo off, or read one piped line.
node .agents/skills/env-curation/scripts/env-tool.mts set .env NAME --from-env SOURCE_NAME # Copy a variable already set.
node .agents/skills/env-curation/scripts/env-tool.mts clear .env NAME                     # Remove one key.
```

Never pass a value as an argument: the tool refuses any argument beyond these and does not print it. `set` accepts one
nonempty line of UTF-8 of at most 64 KiB without control characters. It writes the value in double quotes, escaping
backslashes, quotes, and dollar signs so that a dotenv reader neither expands nor truncates it. It prints the key and,
for a value of 12 characters or more, its last four characters with symbols masked.

Both commands keep every other line, comment, and line ending. They refuse a symbolic link, a file that is not UTF-8, a
malformed or duplicate assignment, and a file that another writer changed during the edit. They replace the file
through a new temporary file beside it, created for the owner alone, and one rename. Editing the file does not create,
rotate, or revoke the credential at its provider, and removing a key does not remove it from version control history.

A repository may keep one-line wrappers, such as `set-env.sh NAME`, that pass its file's path to the tool.

## Check the tool

```sh
node .agents/skills/env-curation/scripts/check/check-env-tool.mts
```

The check runs the real tool on a scratch file with fake values. It sets a key from a variable and reads it back through
`mise env --json`, replaces it from piped input, clears it, and confirms that a value passed as an argument and an empty
value leave the file unchanged and unprinted. It prints one line and exits 0 when every step holds. Type-check the tool
with `.agents/skills/env-curation/scripts/node_modules/.bin/tsc -p .agents/skills/env-curation/scripts`.
