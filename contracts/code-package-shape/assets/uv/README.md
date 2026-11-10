# Package shape check

Copy `package-shape.json` into the repository as `.config/package-shape.json` and declare the repository's own
values. Run from the repository root, replacing the installed contract path:

```bash
uv run --script .contracts/033-code-package-shape/assets/uv/check-package-shape.py \
  --root . --config .config/package-shape.json
```

The script requires Python 3.14 or later and has no package dependencies. `package-shape.schema.json` describes the
policy:

- `packagePatterns` lists the path patterns of the package folders, such as `packages/*` or `packages/*/*`. Every
  folder that matches is a package and must hold the manifest.
- `manifest` names the manifest file. A `.json` manifest states `name` at its top level; a `.toml` manifest states it
  under `[package]` or `[project]`.
- `sourceFolder` names the one source folder, `src` in the example.
- `entryFiles` and `roleFiles` list the file names that may sit beside folders in a source root.
- `maximumFlatModules` is the most files a source root without folders may hold, 12 in the example.
- `deployEntries` lists each further root entry for one package path, with a reason. `generatedEntries` lists the
  entries that a tool generates, each with a reason; they are ignored in a package root and in a source root.

The checker reports a missing or extra entry in a package root, a folder whose name is not the last segment of the
manifest's name, a file beside folders in a source root that is neither an entry file nor a role file, and a flat
source root over its maximum. It reads only the package root and the source root; the folder limits below them belong
to the layout check.

The command reports every finding and exits unsuccessfully. It changes no files.
