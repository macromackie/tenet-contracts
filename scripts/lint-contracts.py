#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""
Check the library's contracts, skills, README tables, rule ids, hidden text, and upgrade notes.

Run `uv run --script scripts/lint-contracts.py`; it checks the library that holds it.
"""

import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path

import output

ROOT = Path(__file__).resolve().parent.parent
"""The library checkout that holds this script."""
CHANGELOG_FILE = "CHANGELOG.md"
CONTRACT_FILE = "CONTRACT.md"
README_FILE = "README.md"
SKILL_FILE = "SKILL.md"
SUFFIX_FORMS = {
    "boundary": "boundaries",
    "api": "apis",
    "check": "checks",
    "lifecycles": "lifecycle",
    "ownerships": "ownership",
    "curations": "curation",
}
TECHNOLOGIES = {
    r"React|JSX|use(?:Effect|State|Memo|Callback|Ref)\b": {"react"},
    r"TypeScript|tsconfig": {"typescript"},
    r"Effect Schema": {"effect"},
    r"Python|Pydantic|SQLAlchemy": {"python", "fastapi", "alembic"},
    r"FastAPI": {"fastapi"},
    r"Alembic": {"alembic"},
    r"Postgres(?:QL)?": {"postgres"},
    r"SQL": {"sql", "postgres", "alembic"},
    r"Rust|Cargo|Clippy|rustfmt|crates?": {"rust"},
    r"Storybook": {"storybook"},
    r"Terraform|OpenTofu": {"terraform"},
    r"OpenAPI": {"openapi", "fastapi"},
    r"OAuth|PKCE|OIDC": {"oauth"},
    r"Node(?:\.js)?": {"node"},
    r"mise": {"mise"},
    r"uv": {"uv"},
}
"""A technology word may appear only in a contract whose name carries one of the listed words."""
TOOLS = (
    r"ev-grep|Next\.js|TanStack|StyleX|Tailwind|Kubernetes|Docker|GitHub|GitLab|Datadog|Cloudflare|"
    r"AWS|GCP|Azure|Temporal|Bazel|pnpm|npm|Vite|Vitest|Jest|Playwright|Redis|Kafka"
)
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
FRONTMATTER = re.compile(
    r"^---\nname: (?P<name>[^\n]+)\nmessage: (?P<message>[^\n]+)\n"
    r"(?:requires-tenet: (?P<requires>[^\n]+)\n)?---\n\n"
    r"## Rules\n\n(?P<rules>.+?)\n\n## Checks\n\n(?P<checks>.+?)\n\Z",
    flags=re.DOTALL,
)
ASSET = re.compile(r"assets/[^/]+/.+")
"""A tool file under assets/<tool>/, which only Tenet 0.11.0 or later installs from a contract."""
ASSET_TENET = (0, 11, 0)
VERSION = re.compile(r"\d+\.\d+\.\d+")
TWO_SENTENCES = re.compile(r"(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)[.!?] +[A-Z`]")
LINK = re.compile(r"!?\[[^\]]*\]\([^)]*\)|<img\b[^>]*>|https?://\S+")
IMAGE = re.compile(r"!\[|<img")
WORD = re.compile(r"[A-Za-z]+")
MIN_LINKED_RULE_WORDS = 4
"""A rule that holds a link states itself in text when this many words remain without the link."""
HIDDEN_CATEGORIES = frozenset({"Cc", "Cf", "Co", "Zl", "Zp"})
"""The Unicode categories of control, format, private-use, and separator characters."""
VARIATION_SELECTOR = "VARIATION SELECTOR"
HTML_COMMENT = "<!--"
AREA_ROW = re.compile(r"^\|\s*`(?P<area>[a-z]+)`\s*\|", flags=re.MULTILINE)
"""A row of the README's naming table, whose areas form the closed list of name prefixes."""
AREA_HEADING = re.compile(r"^#### (?P<area>[a-z]+)$", flags=re.MULTILINE)
CONTRACT_ROW = re.compile(
    r"^\|\s*`(?P<name>[a-z0-9]+(?:-[a-z0-9]+)+)`\s*\|\s*(?P<requirement>.+?)\s*\|$",
)
CONTRACT_COUNT = re.compile(r"^The library has (?P<count>\d+) contracts\.$", flags=re.MULTILINE)
RELEASE_HEADING = re.compile(r"^## (?P<version>v\d+\.\d+\.\d+)$", flags=re.MULTILINE)
"""A release's changelog heading; the changelog lists releases newest first."""
MAJOR_VERSION = re.compile(r"v\d+\.0\.0")
UPGRADING_HEADING = "\n### Upgrading\n"
ROLLBACK_COMMAND = "tenet contracts update --ref"
RULE_FILES = "contracts/*/assets/ast-grep/*/*.yml"
"""The rule and utility files of each ast-grep rule set, which its sgconfig.yml loads."""
RULE_TESTS = "*/ast-grep/rule-tests/*.yml"
"""The ast-grep case files of each contract's tests/ folder."""
RULE_ID = re.compile(
    r"""^(["']?)id\1:[ \t]*(["']?)(?P<id>[^"'\s]+)\2[ \t]*$""",
    flags=re.MULTILINE,
)
"""A top-level `id` key and its value, each quoted or not; library ast-grep files quote both."""
SKILL_FIELDS = frozenset({
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
})
"""The frontmatter fields that Agent Skills allows; https://agentskills.io/specification."""
NAME_FIELD = "name"
DESCRIPTION_FIELD = "description"
COMPATIBILITY_FIELD = "compatibility"
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_NAME_CHARACTERS = 64
SKILL_DESCRIPTION_CHARACTERS = 1024
SKILL_COMPATIBILITY_CHARACTERS = 500
SKILL_FRONTMATTER = re.compile(r"^---\n(?P<fields>.*?)\n---\n", flags=re.DOTALL)
SKILL_FIELD = re.compile(r"""^([^\s#-][^:\n]*):[ \t]*(["']?)(.*?)\2[ \t]*$""", flags=re.MULTILINE)
"""A top-level key and its unquoted inline value; indented lines and list items continue the key."""
CONTINUATION_PREFIXES = (" ", "\t", "-")
BLOCK_SCALAR_PREFIXES = ("|", ">")


@dataclass(frozen=True, kw_only=True)
class Contract:
    """A contract folder that holds CONTRACT.md, with that file's text and its frontmatter match."""

    name: str
    text: str
    document: re.Match[str] | None
    has_assets: bool


@dataclass(frozen=True, kw_only=True)
class ReadmeRow:
    """A contract's row in one area's table of the README, with its line number."""

    number: int
    area: str
    name: str
    requirement: str


def is_hidden(*, character: str) -> bool:
    """Tell whether a character renders as nothing in a Markdown view."""
    category = unicodedata.category(character)

    return category in HIDDEN_CATEGORIES or VARIATION_SELECTOR in unicodedata.name(character, "")


def check_markdown_line(*, place: str, line: str) -> list[str]:
    """Check one Markdown line for hidden characters and HTML comments."""
    errors = []
    hidden = [character for character in line if is_hidden(character=character)]

    if hidden:
        name = unicodedata.name(hidden[0], "UNNAMED")
        errors.append(f"{place}: remove hidden character U+{ord(hidden[0]):04X} {name}")

    if HTML_COMMENT in line:
        errors.append(f"{place}: remove the HTML comment; rendered views hide it")

    return errors


def check_markdown_files(*, root: Path) -> list[str]:
    """Check every Markdown line, because a model reads the raw text that a rendered view hides."""
    return [
        error
        for path in sorted(root.rglob("*.md"))
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), start=1)
        for error in check_markdown_line(place=f"{path.relative_to(root)}:{number}", line=line)
    ]


def check_contract_files(*, folder: Path) -> list[str]:
    """Check that a contract folder holds CONTRACT.md and nothing else outside assets/<tool>/."""
    files = sorted(
        path.relative_to(folder).as_posix() for path in folder.rglob("*") if path.is_file()
    )

    strays = [file for file in files if file != CONTRACT_FILE and not ASSET.fullmatch(file)]
    errors = []

    if strays:
        errors.append(
            f"{folder.name}: keep only CONTRACT.md and assets/<tool>/ files in the folder, "
            f"not {', '.join(strays)}"
        )

    if CONTRACT_FILE not in files:
        errors.append(f"{folder.name}: add CONTRACT.md")

    return errors


def read_contract(*, folder: Path) -> Contract:
    """Read the CONTRACT.md of a contract folder and match its frontmatter."""
    text = (folder / CONTRACT_FILE).read_text(encoding="utf-8")

    return Contract(
        name=folder.name,
        text=text,
        document=FRONTMATTER.match(text),
        has_assets=(folder / "assets").exists(),
    )


def check_contract_name(*, name: str, areas: frozenset[str]) -> list[str]:
    """Check that a contract's name is kebab case, starts with an area, and spells its suffix."""
    words = name.split("-")
    errors = []

    if not KEBAB.match(name):
        errors.append(f"{name}: use lowercase kebab-case with at least two words")

    if words[0] not in areas:
        errors.append(f"{name}: start with an area: {', '.join(sorted(areas))}")

    if words[-1] in SUFFIX_FORMS:
        errors.append(f"{name}: end with -{SUFFIX_FORMS[words[-1]]}, not -{words[-1]}")

    return errors


def check_contract_words(*, name: str, prose: str) -> list[str]:
    """Check that the prose names each technology its contract's name carries, and no tool."""
    words = set(name.split("-"))
    errors = [
        f"{name}: {found[0]} needs one of {', '.join(sorted(name_words))} in the contract name"
        for pattern, name_words in TECHNOLOGIES.items()
        if not name_words & words and (found := re.search(rf"\b(?:{pattern})\b", prose))
    ]

    if tool := re.search(rf"\b(?:{TOOLS})\b", prose):
        errors.append(f"{name}: do not name the tool {tool[0]} in a library contract")

    return errors


def check_required_tenet(*, name: str, requires: str | None, has_assets: bool) -> list[str]:
    """Check that `requires-tenet` is a version that installs the folder's assets, if it has any."""
    if requires is not None and not VERSION.fullmatch(requires):
        return [f"{name}: requires-tenet must be a version such as 0.11.0, not {requires}"]

    if has_assets and (requires is None or tuple(map(int, requires.split("."))) < ASSET_TENET):
        version = ".".join(map(str, ASSET_TENET))

        return [f"{name}: a contract that ships assets/ needs requires-tenet: {version} or later"]

    return []


def check_contract_document(*, contract: Contract, document: re.Match[str]) -> list[str]:
    """Check the frontmatter's name and message, the required Tenet, and one sentence per line."""
    errors = []

    if document["name"] != contract.name:
        errors.append(
            f"{contract.name}: frontmatter name {document['name']} must equal the folder name"
        )

    if not document["message"].endswith(".") or TWO_SENTENCES.search(document["message"]):
        errors.append(f"{contract.name}: message must be one sentence")

    return [
        *errors,
        *check_required_tenet(
            name=contract.name,
            requires=document["requires"],
            has_assets=contract.has_assets,
        ),
        *(
            f"{contract.name}:{number}: write one sentence per line"
            for number, line in enumerate(contract.text.splitlines(), start=1)
            if line.strip()
            and not line.startswith(("#", "---"))
            and TWO_SENTENCES.search(line.rstrip())
        ),
    ]


def check_contract(
    *, contract: Contract, areas: frozenset[str], references: re.Pattern[str]
) -> list[str]:
    """Check a contract's name, the technology and tool words of its prose, and its document."""
    errors = [
        *check_contract_name(name=contract.name, areas=areas),
        # A backticked library contract name, such as `code-python-uv-scripts`, names that contract.
        *check_contract_words(name=contract.name, prose=references.sub("", contract.text)),
    ]

    if contract.document is None:
        return [
            *errors,
            (
                f"{contract.name}: expected name and message frontmatter, "
                "then ## Rules and ## Checks only"
            ),
        ]

    return [*errors, *check_contract_document(contract=contract, document=contract.document)]


def check_rule_links(*, contract: Contract) -> list[str]:
    """Warn about each rule that is an image or a bare link, because the checker reads neither."""
    if contract.document is None:
        return []

    return [
        f"warning: {contract.name}: state this rule in text; "
        f"the checker reads neither images nor linked pages: {line}"
        for line in contract.document["rules"].splitlines()
        if IMAGE.search(line)
        or (LINK.search(line) and len(WORD.findall(LINK.sub("", line))) < MIN_LINKED_RULE_WORDS)
    ]


def read_readme_rows(*, text: str) -> list[ReadmeRow]:
    """Read each contract row of the README with the area heading above it."""
    rows = []
    area = ""

    for number, line in enumerate(text.splitlines(), start=1):
        if heading := AREA_HEADING.match(line):
            area = heading["area"]
        elif row := CONTRACT_ROW.match(line):
            requirement = row["requirement"].replace("\\|", "|")

            rows.append(
                ReadmeRow(number=number, area=area, name=row["name"], requirement=requirement)
            )

    return rows


def check_readme_row(*, row: ReadmeRow, names: set[str], messages: dict[str, str]) -> list[str]:
    """Check that a README row names a contract of its area and gives that contract's message."""
    place = f"{README_FILE}:{row.number}"
    area = row.name.partition("-")[0]

    if row.name not in names:
        return [f"{place}: remove {row.name}, which names no contract"]

    errors = []

    if area != row.area:
        errors.append(f"{place}: move {row.name} to the table under #### {area}")

    if row.name in messages and row.requirement != messages[row.name]:
        errors.append(
            f"{place}: give {row.name} its message as the requirement: {messages[row.name]}"
        )

    return errors


def check_test_folder(*, root: Path, folder: Path) -> list[str]:
    """Check that a tests/ folder names a contract and holds files only under its tool folders."""
    assets = root / "contracts" / folder.name / "assets"

    if not (assets.parent / CONTRACT_FILE).is_file():
        return [f"tests/{folder.name}: name the folder after a contract"]

    tools = {path.relative_to(folder).parts[0] for path in folder.rglob("*") if path.is_file()}
    strays = sorted(tools - {tool.name for tool in assets.glob("*")})

    if strays:
        return [
            (
                f"tests/{folder.name}: keep test files under a tool folder named for one of the "
                f"contract's assets/ folders, not {', '.join(strays)}"
            ),
        ]

    return []


def check_rule_test(*, root: Path, case: Path) -> list[str]:
    """Check that an ast-grep case names a shipped rule, which `ast-grep test` does not check."""
    rules = root / "contracts" / case.parents[2].name / "assets/ast-grep/rules"
    rule = RULE_ID.search(case.read_text(encoding="utf-8"))

    if (rules / case.name).is_file() and rule is not None and rule["id"] == case.stem:
        return []

    return [
        (
            f"{case.relative_to(root)}: name the file and its id after a rule in "
            f"{rules.relative_to(root)}/"
        ),
    ]


def check_tool_tests(*, root: Path) -> list[str]:
    """Check the tool test cases in tests/<contract>/<tool>/, outside the folder Tenet installs."""
    return [
        *(
            error
            for folder in sorted((root / "tests").iterdir())
            for error in check_test_folder(root=root, folder=folder)
        ),
        *(
            error
            for case in sorted((root / "tests").glob(RULE_TESTS))
            for error in check_rule_test(root=root, case=case)
        ),
    ]


def check_readme_layout(*, text: str, count: int) -> list[str]:
    """Check that the area headings follow the naming table and that the README states the count."""
    errors = []

    if AREA_HEADING.findall(text) != AREA_ROW.findall(text):
        errors.append(f"{README_FILE}: give each area of the naming table a #### heading, in order")

    if CONTRACT_COUNT.findall(text) != [str(count)]:
        errors.append(
            f"{README_FILE}: state the count once, as `The library has {count} contracts.`"
        )

    return errors


def check_readme(*, root: Path, contracts: list[Contract]) -> list[str]:
    """Check that the README lists each contract once under its area, with its message and count."""
    text = (root / README_FILE).read_text(encoding="utf-8")
    rows = read_readme_rows(text=text)
    listings = Counter(row.name for row in rows)
    names = {contract.name for contract in contracts}
    messages = {
        contract.name: contract.document["message"]
        for contract in contracts
        if contract.document is not None
    }

    return [
        *check_readme_layout(text=text, count=len(names)),
        *(
            f"{README_FILE}: list {name} in the table under #### {name.partition('-')[0]}, once"
            for name in sorted(names)
            if listings[name] != 1
        ),
        *(
            error
            for row in rows
            for error in check_readme_row(row=row, names=names, messages=messages)
        ),
    ]


def check_rule_ids(*, root: Path) -> list[str]:
    """Check that each ast-grep rule and utility file declares an id that no other file declares."""
    rule_paths: defaultdict[str, list[str]] = defaultdict(list)
    errors = []

    for path in sorted(root.glob(RULE_FILES)):
        place = path.relative_to(root).as_posix()

        if rule := RULE_ID.search(path.read_text(encoding="utf-8")):
            rule_paths[rule["id"]].append(place)
        else:
            errors.append(f"{place}: declare the rule's id as a top-level key")

    return [
        *errors,
        *(
            f"{', '.join(paths)}: give each rule a distinct id, not {rule_id}"
            for rule_id, paths in rule_paths.items()
            if len(paths) > 1
        ),
    ]


def check_upgrading_blocks(*, root: Path) -> list[str]:
    """
    Check that each major release has an Upgrading block that rolls back to the release before it.

    The oldest release, v1.0.0, has no release before it, so it needs no block.
    """
    text = (root / CHANGELOG_FILE).read_text(encoding="utf-8")
    errors = []

    for release, previous in pairwise(RELEASE_HEADING.finditer(text)):
        section = text[release.end() : previous.start()]
        rollback = f"`{ROLLBACK_COMMAND} {previous['version']}`"
        has_block = UPGRADING_HEADING in section and rollback in section

        if MAJOR_VERSION.fullmatch(release["version"]) and not has_block:
            errors.append(
                f"{CHANGELOG_FILE}: give ## {release['version']} an ### Upgrading block "
                f"that rolls back with {rollback}"
            )

    return errors


def read_continued_keys(*, fields: str) -> set[str]:
    """Collect the keys whose value continues on indented or list lines, which YAML folds in."""
    key = None
    continued_keys: set[str] = set()

    for line in fields.split("\n"):
        if field := SKILL_FIELD.match(line):
            key = field[1]
        elif line.startswith(CONTINUATION_PREFIXES) and key is not None:
            continued_keys.add(key)

    return continued_keys


def is_inline_value(*, value: str, is_continued: bool, characters: int) -> bool:
    """Tell whether a frontmatter value is a nonempty line of at most the given characters."""
    is_bounded = 0 < len(value) <= characters

    return is_bounded and not value.startswith(BLOCK_SCALAR_PREFIXES) and not is_continued


def check_skill_fields(*, name: str, fields: str) -> list[str]:
    """Check that a skill's frontmatter holds only Agent Skills fields, in the forms they allow."""
    values = {key: value for key, _, value in SKILL_FIELD.findall(fields)}
    continued_keys = read_continued_keys(fields=fields)
    errors = [
        f"skills/{name}: remove frontmatter field {key}; "
        f"library skills use only {', '.join(sorted(SKILL_FIELDS))}"
        for key in sorted(values.keys() - SKILL_FIELDS)
    ]

    if values.get(NAME_FIELD) != name:
        errors.append(f"skills/{name}: frontmatter name must equal the folder name")

    if not is_inline_value(
        value=values.get(DESCRIPTION_FIELD, ""),
        is_continued=DESCRIPTION_FIELD in continued_keys,
        characters=SKILL_DESCRIPTION_CHARACTERS,
    ):
        errors.append(
            f"skills/{name}: write the description on one line, "
            f"at most {SKILL_DESCRIPTION_CHARACTERS} characters"
        )

    if COMPATIBILITY_FIELD in values and not is_inline_value(
        value=values[COMPATIBILITY_FIELD],
        is_continued=COMPATIBILITY_FIELD in continued_keys,
        characters=SKILL_COMPATIBILITY_CHARACTERS,
    ):
        errors.append(
            f"skills/{name}: write compatibility on one line, "
            f"at most {SKILL_COMPATIBILITY_CHARACTERS} characters"
        )

    return errors


def check_skill(*, folder: Path) -> list[str]:
    """Check a skill folder's name and the frontmatter that opens its SKILL.md."""
    name = folder.name
    path = folder / SKILL_FILE
    errors = []

    if not SKILL_NAME.match(name) or len(name) > SKILL_NAME_CHARACTERS:
        errors.append(
            f"skills/{name}: name the folder with lowercase letters, digits, and single hyphens, "
            f"at most {SKILL_NAME_CHARACTERS} characters"
        )

    if not path.is_file() or not (
        document := SKILL_FRONTMATTER.match(path.read_text(encoding="utf-8"))
    ):
        return [*errors, f"skills/{name}: add SKILL.md that starts with frontmatter"]

    return [*errors, *check_skill_fields(name=name, fields=document["fields"])]


def check_contracts(*, root: Path, folders: list[Path], contracts: list[Contract]) -> list[str]:
    """Check every contract folder, every contract, and the README's tables of them."""
    areas = frozenset(AREA_ROW.findall((root / README_FILE).read_text(encoding="utf-8")))
    references = re.compile("|".join(f"`{re.escape(folder.name)}`" for folder in folders))

    return [
        *(error for folder in folders for error in check_contract_files(folder=folder)),
        *(
            error
            for contract in contracts
            for error in check_contract(contract=contract, areas=areas, references=references)
        ),
        *check_readme(root=root, contracts=contracts),
    ]


def main() -> output.ExitStatus:
    """Report every finding in the library, and return whether any is an error."""
    folders = sorted(path for path in (ROOT / "contracts").iterdir() if path.is_dir())
    skills = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())
    contracts = [
        read_contract(folder=folder) for folder in folders if (folder / CONTRACT_FILE).is_file()
    ]

    output.report_findings(
        lines=[warning for contract in contracts for warning in check_rule_links(contract=contract)]
    )

    errors = [
        *check_markdown_files(root=ROOT),
        *check_contracts(root=ROOT, folders=folders, contracts=contracts),
        *check_rule_ids(root=ROOT),
        *check_tool_tests(root=ROOT),
        *check_upgrading_blocks(root=ROOT),
        *(error for folder in skills for error in check_skill(folder=folder)),
    ]

    output.report_findings(lines=errors)

    if errors:
        return output.ExitStatus.INVALID

    output.report_summary(line=f"{len(folders)} contracts and {len(skills)} skills valid")

    return output.ExitStatus.VALID


output.finish(status=main())
