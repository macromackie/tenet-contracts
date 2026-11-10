---
name: code-tool-configuration-folder
message: Keep every tool's settings that a path flag can point at in the workspace's one configuration folder, and pass that path on every call of the tool.
requires-tenet: 0.11.0
---

## Rules

Apply these rules to each workspace, which is a folder that a package manager or a task runner treats as a root.
Keep the settings file of every tool that accepts a settings path, as a flag or as an environment variable, in one folder named `.config/` directly inside the workspace root.
Keep a file at the workspace root only when its tool finds it nowhere else, such as the package manager's manifest, workspace file, and lock file, the version control system's ignore and attributes files, and the folders that hold the source.
Declare the allowed entries of the workspace root once, in the policy that the repository's check reads, and add an entry only for a tool that cannot be pointed elsewhere.
Declare each entry that a tool generates at the root, such as an installed dependency folder, in that policy with its reason, and keep it out of version control.
Never keep two settings files for one tool in one workspace, such as one at the root and one in the configuration folder.

Declare each tool that reads a settings file from the configuration folder in the policy, with the flags that pass the path.
Pass the settings path explicitly on every call of a declared tool in a task, a hook script, and a continuous integration workflow, because a tool that finds no settings can run on its defaults and pass.
Write the path so that it names the configuration folder, never a copy elsewhere.
A call that only prints the tool's version or usage reads no settings and needs no path.
Call a declared tool only from the files that the policy lists as holding commands, so that the check reads every call.

Keep one settings file for a compiler or a type checker at the folder that groups the packages it serves, and write none in a package below a folder that already holds one.
Give a package its own compiler settings only when no folder above it holds one, and state in the package's README what differs.
A folder's settings file that a tool finds by walking up from a source file stays at that folder, since no flag points the walk elsewhere.

Violation: a lint task runs the lint with no settings flag after its settings moved to `.config/`, so the lint passes on its default rules.
Allowed: the task passes `--config .config/lint.json`, and the policy lists the lint with `--config`.
Violation: `packages/orders/` and `packages/invoices/` each hold compiler settings that only extend the file in `packages/`.
Allowed: `packages/` holds the one compiler settings file, and neither package holds another.

## Checks

Run the checker in this contract's `assets/` folder from the repository root with the workspace's policy, where its runtime can run.
For each entry a change adds to the allowed root entries, can its tool be pointed at the configuration folder instead?
For each declared tool, does a planted file that only the workspace's settings reject fail the task that runs the tool?
For each file a change adds that runs commands, does the policy list it among the files that hold commands?
For each package settings file a change adds, does no folder above the package hold settings for the same tool?
