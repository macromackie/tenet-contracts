# Tenet contracts

Shared contracts and agent skills for [Tenet](https://github.com/macromackie/tenet), which checks code against
Markdown contracts. A contract becomes a requirement only when a project installs it.

## Contracts

| Contract | Requirement |
| --- | --- |
| `contract-maintenance` | Keep adopted contracts scoped, reviewable, and consistent with their implementation. |
| `data-and-apis` | Keep authoritative facts and explicit outcomes behind small, usable APIs. |
| `execution-lifecycle` | Bound work and preserve authoritative results through failure and interruption. |
| `ownership-and-boundaries` | Give decisions and state one owner, with explicit dependency direction. |

Install a contract into the scope it governs with Tenet 0.7.0 or later:

```sh
tenet contracts add tenet/data-and-apis --scope packages/api
tenet check --contract data-and-apis
```

Tenet copies it to the next numbered folder, such as `packages/api/.contracts/003-data-and-apis/CONTRACT.md`, and
records the release in `.tenet.lock`. Edit the copy freely; put local exceptions under `## Local adaptations`.
`tenet contracts update` takes later releases: unedited copies are replaced and edited copies merge three ways.

## Skills

Start with `tenet` for CLI usage, `tenet-adoption` for adoption and updates, or one of the curation skills. Ask an agent
to adopt them with `tenet-adoption`, or use a skill installer such as
`npx skills add macromackie/tenet-contracts --skill tenet-adoption`.

## Releases

Releases are `vX.Y.Z` tags. [CHANGELOG.md](CHANGELOG.md) classifies each change. A tightened or removed requirement is a
major release, so review the changelog before updating across one.

See https://tenet-contracts.com/docs/guidance for the full workflow.
