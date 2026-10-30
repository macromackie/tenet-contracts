# Source layout check

Copy `file-layout.json` into the repository as `.config/file-layout.json`. Set `sourceRoots` to every first-party
source, test, and script folder. Add source files outside those roots to `sourceFiles`.

Run from the repository root, replacing the installed contract path:

```bash
uv run --script .contracts/029-code-folder-size/assets/uv/check-layout.py --root . --config .config/file-layout.json
```

The script requires Python 3.14 or later and has no package dependencies. `file-layout.schema.json` describes the
policy. Its example sets 20 files with the same extension directly inside a folder, four folder levels below a
source root, and 300 source lines per file. Set the repository's declared limits in its policy.

The checker counts all lines, including comments and blanks, for the configured `sourceSuffixes` and extensionless
files that start with a shebang. Other files still count toward the folder's extension total. Declare data and
generated paths in `exclusions`, each with a nonempty reason. Excluded paths are pruned before their contents are read.

The command reports every observed limit violation and exits unsuccessfully. It changes no files.
