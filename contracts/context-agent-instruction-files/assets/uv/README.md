# Document name check

Run from the repository root, replacing the installed contract path and naming the repository's own files:

```bash
uv run --script .contracts/009-context-agent-instruction-files/assets/uv/check-doc-identifiers.py \
  --root . --code src scripts --tasks .=mise.toml --whole AGENTS.md README.md
```

The script requires Python 3.14 or later and has no package dependencies. It reads each code span of a document after
`--whole`, and of the text under `## Local adaptations` in a contract after `--adapted`.

| A code span that holds                         | passes when                                                                  |
| ---------------------------------------------- | ---------------------------------------------------------------------------- |
| a file path with a folder                      | the file exists under the root, the document's folder, or a `--base` folder  |
| a bare file name                               | a file under the root has that name, or the code holds it as a whole name    |
| an identifier in a case style that code writes | the code holds it as a word                                                  |
| a package name such as `@scope/name`           | the code holds it as a whole name                                            |
| a kebab-case name                              | it is a declared name, a run of whole names in a path, or a name in the code |
| `mise run <task>`, with or without `-C`        | the folder's entry under `--tasks` declares the task                         |

The code is every file under `--code` except Markdown documents and files under a folder named after `--uncounted`,
such as a folder of made-up test cases.

Declared kebab-case names come from four optional sources:

- `--rules` names each folder whose structural lint rules give an `id`.
- `--lint` names a lint executable that prints its rules with `--rules -f json`.
- `--lock` names the lock that lists each installed contract and skill, and `--contracts` each contract folder.
- `--names` names each file that lists names as `` - `name` `` items.

Each `--tasks` entry is `<folder>=<source>`. The folder is the one a command names after `-C`, or `.` for the root.
The source is a task file with a `[tasks]` table, or a folder of task files, wherever the repository keeps it. Repeat
a folder to combine several sources.

The checker also reads two forms of prose. "`name` in `file`" requires the file to hold the name. A constant and its
value in parentheses, such as "`MAXIMUM_ORDER_LINES` (30)", requires the code to give that constant that one value.

The command reports every name that no longer exists and exits unsuccessfully. It changes no files.
