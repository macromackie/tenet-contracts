---
name: cargo-dist-release
description: Regenerate the release workflow that cargo-dist writes for a Cargo workspace published from a subfolder of its repository, after its dist configuration changes.
license: MIT
compatibility: Needs uv, Git, and the cargo-dist version the workspace pins in its dist configuration.
---

# Regenerate a cargo-dist release workflow

Use this skill after a change to a workspace's dist configuration, such as its `[workspace.metadata.dist]` table or
`dist-workspace.toml`, when the workspace sits in a subfolder of a larger repository and ships from its own repository.
`dist generate` writes `.github/workflows/release.yml` at the root of the Git repository that holds the workspace, so
running it in place writes the workflow to the wrong folder. Install the skill with Tenet 0.11.0 or later:

```sh
tenet skills add tenet/cargo-dist-release
```

## Generate the workflow

Run the script from the repository root, with the pinned `dist` on the path:

```sh
uv run --script .agents/skills/cargo-dist-release/scripts/generate-release.py --workspace workspaces/release-tool
```

It copies the workspace, without its `target` folder, to a new temporary Git repository, runs `dist generate` there,
and copies the generated `.github/workflows/release.yml` back into the workspace. `--prefix` names the start of the
temporary folder's name, such as `release-tool-release-`, and `--dist` names another cargo-dist command. A failed
command stops the script with its own error, and the workspace keeps its previous workflow.

Never edit the generated workflow by hand: change the dist configuration and run the script again. Review the
workflow's diff before committing it, and run the repository's workflow checks on it.

Keep action pins in `github-action-commits`. When an audit requires version comments, include each comment inside
its reference string so cargo-dist generates the audited text. With cargo-dist 0.33.0, the value
`d23441a48e516b6c34aea4fa41551a30e30af803 # v6.1.0` generates the pinned checkout action and its version comment.
Run `dist plan --output-format=json` in the standalone release checkout before publication. It detects drift between
the workflow and the configuration before a release tag exists.
