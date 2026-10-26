---
name: library-skill-portability
message: Keep library skills self-contained and usable without private tooling or companion skills.
---

## Rules

Store each skill at `skills/<name>/SKILL.md` with `name` and `description` frontmatter, and keep the folder name equal to `name`.
Use only the Agent Skills frontmatter fields `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`.
Write `name` in lowercase letters, digits, and single hyphens, at most 64 characters, keep `description` to one line of at most 1024 characters, and keep any `compatibility` to one line of at most 500 characters.
Give each skill folder a copy of the library license as `LICENSE.txt`, and name that license in the `license` field.
Put every resource a skill needs inside its own folder, and keep its links relative.
Keep documents an agent reads when needed under `references/`, executable code under `scripts/`, and templates and data files under `assets/`.
Make each skill work without a sibling checkout, personal configuration, or private command.
A skill may suggest a companion skill but must complete its task without it.
Skills describe how to work; contracts state requirements, so a skill must not restate a contract's rules as its own.
Never name a company, internal product, person, or private repository in a skill, except the copyright holder in its `LICENSE.txt`.
Name the minimum Tenet version a skill's commands need.

## Checks

Run `python3 scripts/lint-contracts.py` from the repository root.
Follow every link in changed skills; does each resolve inside the library?
Walk through a changed skill's main workflow in a fresh repository with only Tenet installed.
Search changed skills for internal names, private commands, and absolute paths.
