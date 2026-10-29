#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["pyyaml==6.0.3", "ruamel-yaml==0.18.16"]
# ///
"""
Check that the library's assets load and pass in their pinned tools, and that a release installs.

Run `uv run --locked --script scripts/check-library.py`; it checks the library that holds it.
It runs lint-contracts.py and the shipped checkers on the library's own files.
It compiles and lints the Effect probe and the env tool, runs the env tool's system check with fake
values, and checks the Effect names and the release version.
It installs every contract and skill with the pinned Tenet.
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from ruamel.yaml import YAML

import output

if TYPE_CHECKING:
    from collections.abc import Iterator

ROOT = Path(__file__).resolve().parent.parent
"""The library checkout that holds this script."""
PINS_FILE = "mise.toml"
"""The file that pins each tool this script runs, which mise installs."""
STRICTNESS_CONTRACT = "code-lint-strictness"
"""The contract whose shipped checker configurations come before every other contract's."""
STRICTNESS = f"contracts/{STRICTNESS_CONTRACT}/assets"
"""The folder of the shipped checker configurations that code-lint-strictness holds."""
PROBE = "tests/code-lint-strictness/typescript"
"""The Effect probe project, written in the Allowed forms of the Effect contracts."""
ENV_TOOL = "skills/env-curation/scripts"
"""The env tool that the env-curation skill ships, with its system check."""
RELEASE_SCRIPTS = "skills/cargo-dist-release/scripts"
"""The release workflow script that the cargo-dist-release skill ships."""
GUIDANCE_CHECK = "contracts/contract-maintenance/assets/uv"
"""The guidance check that contract-maintenance ships, with its packages locked beside it."""
PYTHON_RESOURCES = (RELEASE_SCRIPTS, GUIDANCE_CHECK)
"""The Python scripts that a skill or a contract ships."""
VERSION_COMMANDS = {
    "aqua:ast-grep/ast-grep": ("ast-grep", "--version"),
    "aqua:astral-sh/ruff": ("ruff", "--version"),
    "aqua:astral-sh/ty": ("ty", "--version"),
    "aqua:crate-ci/typos": ("typos", "--version"),
    "aqua:koalaman/shellcheck": ("shellcheck", "--version"),
    "aqua:rhysd/actionlint": ("actionlint", "--version"),
    "aqua:tamasfe/taplo": ("taplo", "--version"),
    "aqua:zizmorcore/zizmor": ("zizmor", "--version"),
    "github:macromackie/tenet": ("tenet", "--version"),
    "node": ("node", "--version"),
    # The markdownlint-cli2 command has no version option; linting no files prints its version.
    "npm:markdownlint-cli2": ("markdownlint-cli2", "#**"),
    "npm:oxfmt": ("oxfmt", "--version"),
    "pipx:pyflakes": ("pyflakes", "--version"),
    "pipx:yamllint": ("yamllint", "--version"),
    "uv": ("uv", "--version"),
}
"""Each pinned tool's command and the arguments that make it print its version."""
LIBRARY_CHECKS = (
    ("uv", "run", "--script", "scripts/lint-contracts.py"),
    (
        "yamllint",
        "--strict",
        "--config-file",
        f"{STRICTNESS}/yamllint/yamllint.yaml",
        "contracts",
        ".github",
    ),
    ("markdownlint-cli2", "--config", f"{STRICTNESS}/markdownlint/markdownlint.jsonc", "**/*.md"),
    ("oxfmt", "--check", "**/*.md"),
    (
        "oxfmt",
        "--config",
        "contracts/code-typescript-import-statements/assets/oxfmt/oxfmtrc.json",
        "--check",
        f"{PROBE}/src",
        ENV_TOOL,
    ),
    ("typos", "--config", f"{STRICTNESS}/typos/typos.toml", "."),
    # Offline, because the online audits call GitHub, and a check never calls a live service.
    (
        "zizmor",
        "--offline",
        "--persona=auditor",
        "--strict-collection",
        "--config",
        ".github/zizmor.yml",
        ".",
    ),
    ("ruff", "check", "--no-cache", "scripts", *PYTHON_RESOURCES),
    ("ruff", "format", "--no-cache", "--check", "scripts", *PYTHON_RESOURCES),
    (
        "ty",
        "check",
        "--config-file",
        f"{STRICTNESS}/ty/ty.toml",
        "--python",
        sys.executable,
        "--extra-search-path",
        "scripts",
        "scripts",
        # The guidance check imports packages that only its own environment installs.
        RELEASE_SCRIPTS,
    ),
)
"""The shipped checkers that run on the library's own files, from the library root."""
ACTIONLINT = (
    "env",
    "SHELLCHECK_OPTS=--enable=all --severity=style",
    "actionlint",
    "-shellcheck=shellcheck",
    "-pyflakes=pyflakes",
)
"""
The actionlint run, with every optional shellcheck check and pyflakes on the workflows' scripts.

actionlint takes the nearest folder with `.git` and `.github/workflows` as the project and reads
`.github/actionlint.yaml` there, so it runs in the committed snapshot, whose project is the library.
"""
RULE_SETS = "contracts/*/assets/ast-grep/sgconfig.yml"
RULE_TESTS = "tests/*/ast-grep/sgconfig.yml"
OXLINT_FILES = "contracts/*/assets/oxlint/*.json"
YAML_FILES = ("contracts/**/*.y*ml", "tests/**/*.y*ml")
OXLINT_LAYERS = "oxlint-layers.json"
"""The configuration this script writes in the snapshot to extend every shipped oxlint file."""
LAYERING_SETTINGS = "contracts/code-typescript-module-boundaries/assets/oxlint/oxlintrc.json"
"""The shipped oxlint file whose `settings` a configuration that extends it must copy."""
COMMENT_LINE = re.compile(r"^\s*//.*$", flags=re.MULTILINE)
GIT_IDENTITY = (
    "-c",
    "user.name=Library check",
    "-c",
    "user.email=library-check@example.invalid",
    "-c",
    "commit.gpgsign=false",
)
NPM_CI = ("npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund")
EFFECT_MODULES = ("Effect", "Schema", "Option", "Schedule", "Data", "Context")
"""The Effect modules whose members the contracts and rules name."""
MEMBER_REFERENCE = re.compile(rf"\b({'|'.join(EFFECT_MODULES)})\\?\.([A-Za-z_]\w*)")
"""A member of an Effect module, such as `Effect.forEach`, or `Effect\\.forEach` in a regex."""
MODULE_REGEX = re.compile(rf"\^(?P<module>{'|'.join(EFFECT_MODULES)})\$")
"""An ast-grep regex that matches only one Effect module's name, as a member expression's object."""
INNER_GROUP = re.compile(r"\((?:\?:)?(?P<body>[^()]*)\)(?P<optional>\??)")
"""A regex group that holds no other group, with the `?` that makes it optional."""
REGEX_KEY = "regex"
ALL_KEY = "all"
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", flags=re.DOTALL)
EXPORTED_DECLARATION = re.compile(
    r"^export (?:declare )?(?:abstract )?"
    r"(?:const|let|var|function|class|interface|type|namespace|enum) "
    r"(?P<name>[\w$]+)",
    flags=re.MULTILINE,
)
EXPORT_LIST = re.compile(r"^export (?:type )?\{(?P<names>[^}]*)\}", flags=re.MULTILINE)
RELEASE_HEADING = re.compile(r"^## v(?P<version>\d+\.\d+\.\d+)$", flags=re.MULTILINE)
CLASS_HEADING = re.compile(r"^### (?P<name>.+)$", flags=re.MULTILINE)
CLASS_PARTS = {"Tightened": 0, "Removed": 0, "Added": 1, "Loosened": 1, "Clarified": 2}
"""The version part, major 0, minor 1, or patch 2, that each change class raises."""
UPGRADING_CLASS = "Upgrading"
"""The heading of a release's upgrade notes, which classifies no change."""


def read_pins() -> dict[str, str]:
    """Read the version that the pins file sets for each tool."""
    tools = tomllib.loads((ROOT / PINS_FILE).read_text(encoding="utf-8"))["tools"]

    return {str(tool): str(version) for tool, version in tools.items()}


def check_tool_version(*, tool: str, pin: str) -> list[str]:
    """Check that a pinned tool is on the path and prints its pinned version."""
    command = VERSION_COMMANDS[tool]

    if shutil.which(command[0]) is None:
        return [f"{PINS_FILE}: install {tool} {pin}; {command[0]} is not on the path"]

    printed = subprocess.run(command, capture_output=True, text=True, check=True, cwd=ROOT)
    text = printed.stdout + printed.stderr

    if re.search(rf"(?<![\d.]){re.escape(pin)}(?![\d.])", text):
        return []

    return [f"{PINS_FILE}: run {tool} {pin}, not the {command[0]} that prints {text.strip()!r}"]


def run_check(*, command: tuple[str, ...], folder: Path, stdout: int | None = None) -> list[str]:
    """Run one checker, which prints its own findings, and report the command if it fails."""
    finished = subprocess.run(command, check=False, cwd=folder, stdout=stdout)

    if finished.returncode == 0:
        return []

    return [f"{folder.name}: `{' '.join(command)}` exited with status {finished.returncode}"]


def check_library_files() -> list[str]:
    """Run lint-contracts.py, the shipped checkers, and every ast-grep rule set on the library."""
    toml_files = sorted(str(path.relative_to(ROOT)) for path in ROOT.glob("**/*.toml"))
    taplo = ("taplo", "fmt", "--check", "--config", f"{STRICTNESS}/taplo/taplo.toml", *toml_files)
    scans = [
        (
            "ast-grep",
            "scan",
            "--config",
            str(path.relative_to(ROOT)),
            "scripts",
            f"{PROBE}/src",
            "skills",
            *PYTHON_RESOURCES,
        )
        for path in sorted(ROOT.glob(RULE_SETS))
    ]
    tests = [
        ("ast-grep", "test", "--config", str(path.relative_to(ROOT)))
        for path in sorted(ROOT.glob(RULE_TESTS))
    ]

    return [
        error
        for command in (*LIBRARY_CHECKS, taplo, *scans, *tests)
        for error in run_check(command=command, folder=ROOT)
    ]


def check_yaml_trees() -> list[str]:
    """Check that each YAML asset and test reads as the same data in YAML 1.1 and YAML 1.2."""
    loader = YAML(typ="safe", pure=True)
    paths = sorted(path for pattern in YAML_FILES for path in ROOT.glob(pattern))

    return [
        f"{path.relative_to(ROOT)}: quote each scalar that YAML 1.1 and 1.2 read differently"
        for path in paths
        if yaml.safe_load(path.read_text(encoding="utf-8"))
        != loader.load(path.read_text(encoding="utf-8"))
    ]


def read_release_parts(*, version: str) -> tuple[int, ...]:
    """Split a release version into its major, minor, and patch numbers."""
    return tuple(int(part) for part in version.split("."))


def raise_version(*, version: tuple[int, ...], part: int) -> tuple[int, ...]:
    """Raise one part of a version and reset each part after it."""
    return (*version[:part], version[part] + 1, *(0 for _ in version[part + 1 :]))


def check_release_version() -> list[str]:
    """Check that the newest release raises the previous one by its strongest class's part."""
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    newest, previous = list(RELEASE_HEADING.finditer(text))[:2]
    classes = {
        heading["name"]
        for heading in CLASS_HEADING.finditer(text[newest.end() : previous.start()])
        if heading["name"] != UPGRADING_CLASS
    }

    unknown = sorted(classes - CLASS_PARTS.keys())

    if not classes or unknown:
        return [f"CHANGELOG.md: classify v{newest['version']} as one of {', '.join(CLASS_PARTS)}"]

    expected = raise_version(
        version=read_release_parts(version=previous["version"]),
        part=min(CLASS_PARTS[name] for name in classes),
    )

    if read_release_parts(version=newest["version"]) == expected:
        return []

    raised = ".".join(map(str, expected))

    return [f"CHANGELOG.md: v{previous['version']} with {sorted(classes)} makes v{raised}"]


def read_oxlint_file(*, path: Path) -> dict[str, object]:
    """Read a shipped oxlint file's top-level keys, after the whole-line comments JSON forbids."""
    document = json.loads(COMMENT_LINE.sub("", path.read_text(encoding="utf-8")))

    return {str(key): value for key, value in document.items()}


def read_oxlint_rules(*, path: Path) -> dict[str, str]:
    """Read each rule that a shipped oxlint file sets at its top level, with its setting as JSON."""
    match read_oxlint_file(path=path):
        case {"rules": dict() as rules}:
            return {str(rule): json.dumps(value) for rule, value in rules.items()}
        case _:
            return {}


def check_oxlint_layers() -> list[str]:
    """Check that no two shipped oxlint files set one rule differently, so their order is free."""
    settings: dict[str, dict[str, str]] = {}

    for path in sorted(ROOT.glob(OXLINT_FILES)):
        for rule, value in read_oxlint_rules(path=path).items():
            settings.setdefault(rule, {})[str(path.relative_to(ROOT))] = value

    return [
        f"{', '.join(files)}: set {rule} the same way, so the order of extends changes nothing"
        for rule, files in settings.items()
        if len(set(files.values())) > 1
    ]


def write_oxlint_layers(*, snapshot: Path) -> None:
    """Write a configuration that extends every shipped oxlint file, code-lint-strictness first."""
    paths = sorted(
        (path.relative_to(snapshot) for path in snapshot.glob(OXLINT_FILES)),
        key=lambda path: (path.parts[1] != STRICTNESS_CONTRACT, str(path)),
    )
    layers = {
        "extends": [f"./{path}" for path in paths],
        "settings": read_oxlint_file(path=snapshot / LAYERING_SETTINGS)["settings"],
    }

    (snapshot / OXLINT_LAYERS).write_text(json.dumps(layers, indent=2), encoding="utf-8")


def copy_snapshot(*, snapshot: Path) -> None:
    """Copy the library to a scratch folder, commit it for Tenet, and install its packages."""
    shutil.copytree(
        ROOT,
        snapshot,
        ignore=shutil.ignore_patterns(".git", "node_modules", "__pycache__"),
    )

    for command in (
        ("git", "init", "-q"),
        ("git", "add", "-A"),
        ("git", *GIT_IDENTITY, "commit", "-qm", "Library snapshot"),
    ):
        subprocess.run(command, check=True, cwd=snapshot)

    for folder in (snapshot, snapshot / PROBE, snapshot / ENV_TOOL):
        subprocess.run(NPM_CI, check=True, cwd=folder)


def check_typescript(*, snapshot: Path) -> list[str]:
    """Compile and lint the probe and the env tool, and run the env tool's check on fake values."""
    write_oxlint_layers(snapshot=snapshot)
    oxlint = (
        "node_modules/.bin/oxlint",
        "--type-aware",
        "--deny-warnings",
        "--config",
        OXLINT_LAYERS,
        f"{PROBE}/src",
        ENV_TOOL,
    )
    commands = (
        (("node_modules/.bin/tsc", "--noEmit", "--project", "."), snapshot / PROBE),
        (("node_modules/.bin/tsc", "--noEmit", "--project", "."), snapshot / ENV_TOOL),
        (oxlint, snapshot),
        # It runs the real tool on a scratch file with fake values and reads them through mise.
        (("node", "check/check-env-tool.mts"), snapshot / ENV_TOOL),
    )

    return [
        error for command, folder in commands for error in run_check(command=command, folder=folder)
    ]


def expand_alternatives(*, pattern: str) -> set[str]:
    r"""Spell out each string that a regex's groups allow, such as `Effect\.(?:fail|die)`."""
    group = INNER_GROUP.search(pattern)

    if group is None:
        return set(pattern.split("|"))

    options = [*group["body"].split("|"), *([""] if group["optional"] else [])]

    return {
        expanded
        for option in options
        for expanded in expand_alternatives(
            pattern=pattern[: group.start()] + option + pattern[group.end() :]
        )
    }


def walk_tree(*, key: str, node: object) -> Iterator[tuple[str, object]]:
    """Yield each node of a YAML data tree with the mapping key it sits under."""
    yield key, node

    match node:
        case dict():
            for child_key, child in node.items():
                yield from walk_tree(key=str(child_key), node=child)
        case list():
            for child in node:
                yield from walk_tree(key=key, node=child)
        case _:
            pass


def read_member_patterns(*, items: list[object]) -> list[str]:
    """Join the object and property regexes of a rule's member expression into one regex."""
    modules = []
    properties = []

    for item in items:
        match item:
            case {"has": {"field": "object", "regex": str(regex)}} if MODULE_REGEX.fullmatch(regex):
                modules.append(regex.strip("^$"))
            case {"has": {"field": "property", "regex": str(regex)}}:
                properties.append(regex.strip("^$"))
            case _:
                pass

    return [rf"{module}\.(?:{member})" for module in modules for member in properties]


def read_rule_references(*, path: Path) -> set[tuple[str, str]]:
    """Read each Effect member a rule file names in its text, regexes, or member expressions."""
    text = path.read_text(encoding="utf-8")
    nodes = list(walk_tree(key="", node=yaml.safe_load(text)))
    patterns = [
        *(value for key, value in nodes if key == REGEX_KEY and isinstance(value, str)),
        *(
            pattern
            for key, value in nodes
            if key == ALL_KEY and isinstance(value, list)
            for pattern in read_member_patterns(items=value)
        ),
    ]
    texts = [
        text,
        *(spelled for pattern in patterns for spelled in expand_alternatives(pattern=pattern)),
    ]

    return {reference for text in texts for reference in MEMBER_REFERENCE.findall(text)}


def read_effect_exports(*, snapshot: Path) -> dict[str, set[str]]:
    """Read the names each Effect module exports from the probe's installed type declarations."""
    folder = snapshot / PROBE / "node_modules/effect/dist"
    declarations = {
        module: BLOCK_COMMENT.sub("", (folder / f"{module}.d.ts").read_text(encoding="utf-8"))
        for module in EFFECT_MODULES
    }

    return {
        module: {
            *EXPORTED_DECLARATION.findall(text),
            *(
                name.strip().rpartition(" as ")[2].removeprefix("type ").strip()
                for names in EXPORT_LIST.findall(text)
                for name in names.split(",")
            ),
        }
        for module, text in declarations.items()
    }


def check_effect_names(*, snapshot: Path) -> list[str]:
    """Check that the pinned effect exports each Effect member a contract or rule file names."""
    exports = read_effect_exports(snapshot=snapshot)
    version = json.loads((ROOT / PROBE / "package.json").read_text(encoding="utf-8"))[
        "dependencies"
    ]["effect"]
    references = {
        **{
            path: set(MEMBER_REFERENCE.findall(path.read_text(encoding="utf-8")))
            for path in ROOT.glob("contracts/*/CONTRACT.md")
        },
        **{
            path: read_rule_references(path=path)
            for path in ROOT.glob("contracts/*/assets/ast-grep/*/*.yml")
        },
    }

    return [
        f"{path.relative_to(ROOT)}: name a member effect {version} exports, not {module}.{member}"
        for path, members in sorted(references.items())
        for module, member in sorted(members)
        if member not in exports[module]
    ]


def install_library(*, snapshot: Path, adopter: Path) -> list[str]:
    """Install each contract and skill from the snapshot with the pinned Tenet, and validate."""
    source = f"library={snapshot.as_uri()}"
    commands = [
        ("git", "init", "-q", str(adopter)),
        *(
            (
                "tenet",
                "--root",
                str(adopter),
                "contracts",
                "add",
                f"library/{path.name}@HEAD",
                "--source",
                source,
                "--scope",
                ".",
            )
            for path in sorted((snapshot / "contracts").iterdir())
        ),
        *(
            (
                "tenet",
                "--root",
                str(adopter),
                "skills",
                "add",
                f"library/{path.name}@HEAD",
                "--source",
                source,
            )
            for path in sorted((snapshot / "skills").iterdir())
        ),
        ("tenet", "--root", str(adopter), "validate"),
    ]

    # Tenet names each installed copy on standard output and each refusal on standard error.
    return [
        error
        for command in commands
        for error in run_check(command=command, folder=adopter.parent, stdout=subprocess.DEVNULL)
    ]


def check_snapshot(*, scratch: Path) -> list[str]:
    """Check what needs installed packages or installed copies, in a committed library snapshot."""
    snapshot = scratch / "library"

    copy_snapshot(snapshot=snapshot)
    typescript_errors = check_typescript(snapshot=snapshot)

    return [
        *typescript_errors,
        *run_check(command=ACTIONLINT, folder=snapshot),
        *check_effect_names(snapshot=snapshot),
        *install_library(snapshot=snapshot, adopter=scratch / "adopter"),
    ]


def main() -> output.ExitStatus:
    """Report every finding in the library, and return whether any is an error."""
    pins = read_pins()
    version_errors = [
        error
        for tool in VERSION_COMMANDS
        for error in check_tool_version(tool=tool, pin=pins[tool])
    ]

    if version_errors:
        output.report_findings(lines=version_errors)

        return output.ExitStatus.INVALID

    with tempfile.TemporaryDirectory(prefix="library-check-") as scratch:
        errors = [
            *check_library_files(),
            *check_yaml_trees(),
            *check_release_version(),
            *check_oxlint_layers(),
            *check_snapshot(scratch=Path(scratch)),
        ]

    output.report_findings(lines=errors)

    if errors:
        return output.ExitStatus.INVALID

    output.report_summary(line="Every asset, the probe, the release version, and the install pass")

    return output.ExitStatus.VALID


output.finish(status=main())
