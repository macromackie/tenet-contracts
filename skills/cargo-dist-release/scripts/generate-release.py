#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""
Regenerate cargo-dist's release workflow for a Cargo workspace in a subfolder of its repository.

Run `uv run --script generate-release.py --workspace PATH` from the repository root, with the
pinned `dist` on the path. It copies the workspace to a temporary Git repository of its own, runs
`dist generate` there, and copies the generated `.github/workflows/release.yml` back.
"""

import argparse
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

WORKFLOW = ".github/workflows/release.yml"
"""The release workflow that `dist generate` writes, relative to the workspace."""
BUILD_FOLDER = "target"
"""Cargo's build output, which the copy leaves out."""
GIT_INIT = ("git", "init", "-q")
"""The command that makes the folder after it a new Git repository."""


@dataclass(frozen=True)
class Settings:
    """The decoded arguments of one run."""

    workspace: Path
    prefix: str
    dist: str


def read_settings() -> Settings:
    """Decode the workspace folder, the temporary folder's name prefix, and the dist command."""
    parser = argparse.ArgumentParser(description="Regenerate cargo-dist's release workflow.")
    parser.add_argument("--workspace", type=Path, default=Path(), help="the Cargo workspace folder")
    parser.add_argument(
        "--prefix",
        default="cargo-dist-release-",
        help="the start of the temporary folder's name",
    )
    parser.add_argument("--dist", default="dist", help="the cargo-dist command")
    arguments = parser.parse_args()

    return Settings(workspace=arguments.workspace, prefix=arguments.prefix, dist=arguments.dist)


def main() -> None:
    """Generate the release workflow in a standalone copy of the workspace and copy it back."""
    settings = read_settings()
    source = settings.workspace.resolve()

    with tempfile.TemporaryDirectory(prefix=settings.prefix) as temporary:
        workspace = Path(temporary)
        shutil.copytree(
            source,
            workspace,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(BUILD_FOLDER),
        )
        subprocess.run([*GIT_INIT, str(workspace)], check=True)
        subprocess.run([settings.dist, "generate"], cwd=workspace, check=True)
        shutil.copyfile(workspace / WORKFLOW, source / WORKFLOW)


main()
