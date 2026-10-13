---
name: library-skill-portability
message: Keep library skills self-contained and usable without private tooling or companion skills.
---

## Rules

Store each skill at `skills/<name>/SKILL.md` with `name` and `description` frontmatter, and keep the folder name equal to `name`.
Put every resource a skill needs inside its own folder, and keep its links relative.
Make each skill work without a sibling checkout, personal configuration, or private command.
A skill may suggest a companion skill but must complete its task without it.
Skills describe how to work; contracts state requirements, so a skill must not restate a contract's rules as its own.
Never name a company, internal product, person, or private repository in a skill.
Name the minimum Tenet version a skill's commands need.

## Checks

Follow every link in changed skills; does each resolve inside the library?
Walk through a changed skill's main workflow in a fresh repository with only Tenet installed.
Search changed skills for internal names, private commands, and absolute paths.
