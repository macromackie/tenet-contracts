"""Check library contract names, layout, technology words, skill metadata, and hidden text: python3 scripts/lint-contracts.py [ROOT]."""
import re
import sys
import unicodedata
from pathlib import Path

AREAS = {"agent", "api", "ci", "cli", "code", "context", "contract", "data", "docs", "eval", "infra", "llm", "release", "security", "service", "telemetry", "test", "ui", "web"}
SUFFIX_FORMS = {"boundary": "boundaries", "api": "apis", "check": "checks", "lifecycles": "lifecycle", "ownerships": "ownership", "curations": "curation"}
# A technology word may appear only in a contract whose name carries one of the listed words.
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
}
TOOLS = r"ev-grep|Next\.js|Node\.js|TanStack|StyleX|Tailwind|Kubernetes|Docker|GitHub|GitLab|Datadog|Cloudflare|AWS|GCP|Azure|Temporal|Bazel|mise|pnpm|npm|Vite|Vitest|Jest|Playwright|Redis|Kafka"
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
FRONTMATTER = re.compile(r"^---\nname: (?P<name>[^\n]+)\nmessage: (?P<message>[^\n]+)\n(?:requires-tenet: (?P<requires>[^\n]+)\n)?---\n\n## Rules\n\n(?P<rules>.+?)\n\n## Checks\n\n(?P<checks>.+?)\n\Z", re.S)
# A contract folder holds CONTRACT.md and tool files under assets/<tool>/, which only Tenet 0.11.0 or later installs.
ASSET = re.compile(r"assets/[^/]+/.+")
ASSET_TENET = (0, 11, 0)
VERSION = re.compile(r"\d+\.\d+\.\d+")
# Agent Skills allows only these frontmatter fields and limits; https://agentskills.io/specification
SKILL_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_NAME_CHARACTERS = 64
SKILL_DESCRIPTION_CHARACTERS = 1024
SKILL_COMPATIBILITY_CHARACTERS = 500
SKILL_FRONTMATTER = re.compile(r"^---\n(?P<fields>.*?)\n---\n", re.S)
# A top-level key with its inline value, unquoted; indented lines and list items continue the previous key.
SKILL_FIELD = re.compile(r"""^([^\s#-][^:\n]*):[ \t]*(["']?)(.*?)\2[ \t]*$""", re.M)
TWO_SENTENCES = re.compile(r"(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)[.!?] +[A-Z`]")
LINK = re.compile(r"!?\[[^\]]*\]\([^)]*\)|<img\b[^>]*>|https?://\S+")

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
errors = []
warnings = []
# A model reads the raw text, while a reviewer of rendered Markdown sees neither hidden characters nor comments.
for path in sorted(root.rglob("*.md")):
    for number, line in enumerate(path.read_text().split("\n"), 1):
        hidden = [ch for ch in line if unicodedata.category(ch) in {"Cc", "Cf", "Co", "Zl", "Zp"} or "VARIATION SELECTOR" in unicodedata.name(ch, "")]
        if hidden:
            errors.append(f"{path.relative_to(root)}:{number}: remove hidden character U+{ord(hidden[0]):04X} {unicodedata.name(hidden[0], 'UNNAMED')}")
        if "<!--" in line:
            errors.append(f"{path.relative_to(root)}:{number}: remove the HTML comment; rendered views hide it")
folders = sorted(path for path in (root / "contracts").iterdir() if path.is_dir())
for folder in folders:
    name = folder.name
    files = sorted(path.relative_to(folder).as_posix() for path in folder.rglob("*") if not path.is_dir())
    if strays := [file for file in files if file != "CONTRACT.md" and not ASSET.fullmatch(file)]:
        errors.append(f"{name}: keep only CONTRACT.md and assets/<tool>/ files in the folder, not {', '.join(strays)}")
    path = folder / "CONTRACT.md"
    if not path.is_file():
        errors.append(f"{name}: add CONTRACT.md")
        continue
    text = path.read_text()
    words = name.split("-")
    if not KEBAB.match(name):
        errors.append(f"{name}: use lowercase kebab-case with at least two words")
    if words[0] not in AREAS:
        errors.append(f"{name}: start with an area: {', '.join(sorted(AREAS))}")
    if words[-1] in SUFFIX_FORMS:
        errors.append(f"{name}: end with -{SUFFIX_FORMS[words[-1]]}, not -{words[-1]}")
    for pattern, allowed in TECHNOLOGIES.items():
        if not allowed & set(words) and (found := re.search(rf"\b(?:{pattern})\b", text)):
            errors.append(f"{name}: {found[0]} needs one of {', '.join(sorted(allowed))} in the contract name")
    if found := re.search(rf"\b(?:{TOOLS})\b", text):
        errors.append(f"{name}: do not name the tool {found[0]} in a library contract")
    document = FRONTMATTER.match(text)
    if not document:
        errors.append(f"{name}: expected name and message frontmatter, then ## Rules and ## Checks only")
        continue
    if document["name"] != name:
        errors.append(f"{name}: frontmatter name {document['name']} must equal the folder name")
    if not document["message"].endswith(".") or TWO_SENTENCES.search(document["message"]):
        errors.append(f"{name}: message must be one sentence")
    requires = document["requires"]
    if requires is not None and not VERSION.fullmatch(requires):
        errors.append(f"{name}: requires-tenet must be a version such as 0.11.0, not {requires}")
    elif (folder / "assets").exists() and (requires is None or tuple(map(int, requires.split("."))) < ASSET_TENET):
        errors.append(f"{name}: a contract that ships assets/ needs requires-tenet: {'.'.join(map(str, ASSET_TENET))} or later")
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("#") or line.startswith("---") or not line.strip():
            continue
        if TWO_SENTENCES.search(line.rstrip()):
            errors.append(f"{name}:{number}: write one sentence per line")
    for line in document["rules"].splitlines():
        if re.search(r"!\[|<img", line) or (LINK.search(line) and len(re.findall(r"[A-Za-z]+", LINK.sub("", line))) < 4):
            warnings.append(f"warning: {name}: state this rule in text; the checker reads neither images nor linked pages: {line}")
skills = sorted(path for path in (root / "skills").iterdir() if path.is_dir())
for folder in skills:
    name = folder.name
    if not SKILL_NAME.match(name) or len(name) > SKILL_NAME_CHARACTERS:
        errors.append(f"skills/{name}: name the folder with lowercase letters, digits, and single hyphens, at most {SKILL_NAME_CHARACTERS} characters")
    path = folder / "SKILL.md"
    document = SKILL_FRONTMATTER.match(path.read_text()) if path.is_file() else None
    if not document:
        errors.append(f"skills/{name}: add SKILL.md that starts with frontmatter")
        continue
    fields = {key: value for key, _, value in SKILL_FIELD.findall(document["fields"])}
    # YAML folds indented continuation lines into the previous key's value, which SKILL_FIELD reads only in part.
    key, continued = None, set()
    for line in document["fields"].split("\n"):
        if field := SKILL_FIELD.match(line):
            key = field[1]
        elif line[:1] in {" ", "\t", "-"} and key:
            continued.add(key)
    for key in sorted(set(fields) - SKILL_FIELDS):
        errors.append(f"skills/{name}: remove frontmatter field {key}; library skills use only {', '.join(sorted(SKILL_FIELDS))}")
    if fields.get("name") != name:
        errors.append(f"skills/{name}: frontmatter name must equal the folder name")
    description = fields.get("description", "")
    if not description or description[0] in "|>" or "description" in continued or len(description) > SKILL_DESCRIPTION_CHARACTERS:
        errors.append(f"skills/{name}: write the description on one line, at most {SKILL_DESCRIPTION_CHARACTERS} characters")
    compatibility = fields.get("compatibility")
    if compatibility is not None and (not compatibility or compatibility[0] in "|>" or "compatibility" in continued or len(compatibility) > SKILL_COMPATIBILITY_CHARACTERS):
        errors.append(f"skills/{name}: write compatibility on one line, at most {SKILL_COMPATIBILITY_CHARACTERS} characters")
for warning in warnings:
    print(warning, file=sys.stderr)
if errors:
    sys.exit("\n".join(errors))
print(f"{len(folders)} contract names and layouts and {len(skills)} skills valid")
