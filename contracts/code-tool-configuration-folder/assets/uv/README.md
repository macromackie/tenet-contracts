# Tool configuration check

Copy `tool-configuration.json` into the workspace as `.config/tool-configuration.json` and declare the workspace's
own entries. Run from the repository root, replacing the installed contract path and the workspace root:

```bash
uv run --script .contracts/032-code-tool-configuration-folder/assets/uv/check-tool-configuration.py \
  --root . --config .config/tool-configuration.json
```

The script requires Python 3.14 or later and has no package dependencies. `tool-configuration.schema.json` describes
the policy:

- `configurationFolder` names the one settings folder, `.config` in the example.
- `rootEntries` lists every entry allowed directly inside the root. `generatedEntries` lists the entries that a tool
  generates, each with a reason; they are allowed at the root and pruned from every walk.
- `tools` lists each command with the flags that pass its settings path. A flag
  matches as its own word or before `=`, anywhere on the same command line.
- `commandFiles` lists the patterns of the files that hold commands: task files, hook scripts, and workflows.
- `sharedSettings` lists the file names of compiler settings that one folder holds for the folders below it.

The checker reports an unlisted root entry, a call of a declared tool without one of its flags, a settings path that
does not name the configuration folder, and a `sharedSettings` file in a folder below another folder that holds one.
A call is a word of a command line whose last path segment is the command, so `node_modules/.bin/oxlint` counts. Lines
that end with a backslash join the next line. A call followed by `--version` or `--help` passes. Comment lines and
lines that start with `name:`, `- name:`, or `description` are labels and are skipped, as is a word followed by `=` or
`:`, which is a pin or a key. Declare a tool that takes its settings from an environment variable by listing the
variable's name, such as `TY_CONFIG_FILE`, as its flag.

The command reports every finding and exits unsuccessfully. It changes no files. It cannot tell whether a settings
file loads; plant a file that only the settings reject to prove that.
