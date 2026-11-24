#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Run passing and failing example workspaces against the shipped secret manifest checker."""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

GUIDANCE_PARENT_DEPTH = 3
CHECKER_PATH = "contracts/security-declarative-secret-delivery/assets/uv/check-secret-manifest.py"
CASE_TIMEOUT_SECONDS = 60
OUTPUT_CHARACTER_LIMIT = 6000
CHECKER_ARGUMENTS = ("--config", ".config/secret-delivery.json")


@dataclass(frozen=True, kw_only=True)
class Case:
    """One workspace fixture expressed as edits over the passing baseline."""

    name: str
    files: tuple[tuple[str, str], ...] = ()
    removed: tuple[str, ...] = ()
    diagnostic: str = ""


POLICY = """{
  "allowedUnusedManifestSecrets": [],
  "bannedScriptPatterns": ["**/sync-secrets.*", "**/sync_secrets.*"],
  "builtinWorkflowSecrets": ["GITHUB_TOKEN"],
  "manifestPath": "infra/secrets.manifest.json",
  "runtimeBindingPatterns": ["infra/**/*.tf"],
  "workflowPatterns": [".github/workflows/*.yml"]
}
"""

SINGLE_ENV_MANIFEST = """{
  "version": 1,
  "repository": "example/orders",
  "deployment": {
    "connection": "company-ci",
    "environment": "production",
    "secrets": [
      {"name": "DEPLOY_API_TOKEN", "secret": "company/ORDERS_PRODUCTION_DEPLOY_API_TOKEN"}
    ]
  },
  "runtime": {
    "connection": "company-edge",
    "workers": {
      "orders-api": [
        {"binding": "SIGNING_KEY", "secret": "company/ORDERS_PRODUCTION_SIGNING_KEY"}
      ]
    }
  }
}
"""

MULTI_ENV_MANIFEST = """{
  "version": 1,
  "repository": "example/platform",
  "github": {
    "connection": "company-ci",
    "environments": {
      "production": [
        {"name": "DEPLOY_API_TOKEN", "secret": "company/PLATFORM_PRODUCTION_DEPLOY_API_TOKEN"}
      ],
      "staging": [
        {"name": "STAGING_API_TOKEN", "secret": "company/PLATFORM_STAGING_API_TOKEN"}
      ]
    }
  },
  "cloudflare": {
    "connection": "company-edge",
    "workers": {
      "orders-api": [
        {"binding": "SIGNING_KEY", "secret": "company/PLATFORM_PRODUCTION_SIGNING_KEY"}
      ]
    }
  }
}
"""

WORKFLOW = """name: Deploy
jobs:
  deploy:
    steps:
      - env:
          TOKEN: ${{ secrets.GITHUB_TOKEN }}
          DEPLOY_API_TOKEN: ${{ secrets.DEPLOY_API_TOKEN }}
"""

MULTI_ENV_WORKFLOW = """name: Deploy
jobs:
  deploy:
    steps:
      - env:
          DEPLOY_API_TOKEN: ${{ secrets.DEPLOY_API_TOKEN }}
          STAGING_API_TOKEN: ${{ secrets.STAGING_API_TOKEN }}
"""

INFRA_TF = """locals {
  bindings = [
    {
      name = "SIGNING_KEY"
      type = "inherit"
    }
  ]
}
"""

PASSING_FILES = (
    (".config/secret-delivery.json", POLICY),
    ("infra/secrets.manifest.json", SINGLE_ENV_MANIFEST),
    (".github/workflows/deploy.yml", WORKFLOW),
    ("infra/release.tf", INFRA_TF),
)

CASES = (
    Case(name="single-environment-manifest-passes"),
    Case(
        name="multi-environment-manifest-passes",
        files=(
            ("infra/secrets.manifest.json", MULTI_ENV_MANIFEST),
            (".github/workflows/deploy.yml", MULTI_ENV_WORKFLOW),
        ),
    ),
    Case(
        name="undeclared-workflow-secret-is-rejected",
        files=(
            (
                ".github/workflows/deploy.yml",
                WORKFLOW + "          BILLING_KEY: ${{ secrets.BILLING_KEY }}\n",
            ),
        ),
        diagnostic="check workflow '.github/workflows/deploy.yml': declare secret 'BILLING_KEY'",
    ),
    Case(
        name="unused-manifest-secret-is-rejected",
        files=(
            (
                "infra/secrets.manifest.json",
                SINGLE_ENV_MANIFEST.replace(
                    '{"name": "DEPLOY_API_TOKEN", '
                    '"secret": "company/ORDERS_PRODUCTION_DEPLOY_API_TOKEN"}',
                    '{"name": "DEPLOY_API_TOKEN", '
                    '"secret": "company/ORDERS_PRODUCTION_DEPLOY_API_TOKEN"},\n'
                    '      {"name": "STALE_SECRET", '
                    '"secret": "company/ORDERS_PRODUCTION_STALE_SECRET"}',
                ),
            ),
        ),
        diagnostic="check secret manifest 'infra/secrets.manifest.json': "
        "remove unused secret 'STALE_SECRET'",
    ),
    Case(
        name="duplicate-binding-is-rejected",
        files=(
            (
                "infra/secrets.manifest.json",
                SINGLE_ENV_MANIFEST.replace(
                    '{"binding": "SIGNING_KEY", "secret": "company/ORDERS_PRODUCTION_SIGNING_KEY"}',
                    '{"binding": "SIGNING_KEY", '
                    '"secret": "company/ORDERS_PRODUCTION_SIGNING_KEY"},\n'
                    '        {"binding": "SIGNING_KEY", '
                    '"secret": "company/ORDERS_PRODUCTION_SIGNING_KEY"}',
                ),
            ),
        ),
        diagnostic="remove duplicate binding 'SIGNING_KEY'",
    ),
    Case(
        name="disallowed-plaintext-field-is-rejected",
        files=(
            (
                "infra/secrets.manifest.json",
                SINGLE_ENV_MANIFEST.replace(
                    '"secret": "company/ORDERS_PRODUCTION_DEPLOY_API_TOKEN"',
                    '"secret": "company/ORDERS_PRODUCTION_DEPLOY_API_TOKEN", "value": "raw"',
                ),
            ),
        ),
        diagnostic="remove disallowed fields ['value']",
    ),
    Case(
        name="undeclared-inherited-runtime-binding-is-rejected",
        files=(
            (
                "infra/release.tf",
                INFRA_TF
                + '\nlocals {\n  extra = [{ name = "WEBHOOK_SECRET"\n    type = "inherit" }]\n}\n',
            ),
        ),
        diagnostic="check runtime definition 'infra/release.tf': "
        "declare inherited binding 'WEBHOOK_SECRET'",
    ),
    Case(
        name="banned-sync-script-is-rejected",
        files=(("scripts/sync-secrets.sh", "#!/bin/sh\necho push\n"),),
        diagnostic="check secret delivery script 'scripts/sync-secrets.sh': "
        "remove ad-hoc secret sync script",
    ),
    Case(
        name="unknown-policy-field-is-rejected",
        files=(
            (".config/secret-delivery.json", POLICY.replace("{\n", '{\n  "extra": true,\n', 1)),
        ),
        diagnostic="read secret delivery policy",
    ),
)


def _write_workspace(*, root: Path, case: Case) -> None:
    files = {**dict(PASSING_FILES), **dict(case.files)}
    for relative, content in files.items():
        if relative in case.removed:
            continue
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def _verify_result(*, case: Case, result: subprocess.CompletedProcess[str]) -> None:
    is_pass = result.returncode == 0
    is_match = is_pass and case.diagnostic == ""
    if case.diagnostic:
        is_match = not is_pass and case.diagnostic in result.stderr
    if is_match:
        return
    combined = (result.stdout + result.stderr)[-OUTPUT_CHARACTER_LIMIT:]
    message = (
        f"check secret manifest case {case.name!r}: expected diagnostic {case.diagnostic!r}, "
        f"received exit {result.returncode!r} with output {combined!r}"
    )
    raise AssertionError(message)


def _run_case(*, checker: Path, case: Case) -> None:
    with TemporaryDirectory(prefix=f"check-secret-manifest-{case.name}-") as temporary:
        root = Path(temporary)
        _write_workspace(root=root, case=case)
        command = ["uv", "run", "--script", str(checker), "--root", str(root), *CHECKER_ARGUMENTS]
        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
            timeout=CASE_TIMEOUT_SECONDS,
        )
        _verify_result(case=case, result=result)


def main() -> None:
    """Run the shipped secret manifest checker across passing and failing workspaces."""
    guidance = Path(__file__).resolve().parents[GUIDANCE_PARENT_DEPTH]
    for case in CASES:
        _run_case(checker=guidance / CHECKER_PATH, case=case)


if __name__ == "__main__":
    main()
