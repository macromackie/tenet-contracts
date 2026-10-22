"""Check library contract names, layout, technology words, and hidden text: python3 scripts/lint-contracts.py [ROOT]."""
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
FRONTMATTER = re.compile(r"^---\nname: (?P<name>.+)\nmessage: (?P<message>.+)\n---\n\n## Rules\n\n(?P<rules>.+?)\n\n## Checks\n\n(?P<checks>.+?)\n\Z", re.S)
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
names = [path.parent.name for path in sorted((root / "contracts").glob("*/CONTRACT.md"))]
for name in names:
    path = root / "contracts" / name / "CONTRACT.md"
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
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("#") or line.startswith("---") or not line.strip():
            continue
        if TWO_SENTENCES.search(line.rstrip()):
            errors.append(f"{name}:{number}: write one sentence per line")
    for line in document["rules"].splitlines():
        if re.search(r"!\[|<img", line) or (LINK.search(line) and len(re.findall(r"[A-Za-z]+", LINK.sub("", line))) < 4):
            warnings.append(f"warning: {name}: state this rule in text; the checker reads neither images nor linked pages: {line}")
for warning in warnings:
    print(warning, file=sys.stderr)
if errors:
    sys.exit("\n".join(errors))
print(f"{len(names)} contract names and layouts valid")
