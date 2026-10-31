"""Build package policy examples that exercise the actual native resolver."""

import json
from dataclasses import replace

from constants import (
    APPLICATION_MANIFEST,
    LIBRARY_MANIFEST,
    SUPPORT_MANIFEST,
    TEST_SUPPORT_EDGES,
)
from model import Fixture


def _serialize_manifest(
    *,
    name: str,
    dependencies: tuple[str, ...] = (),
    development_dependencies: tuple[str, ...] = (),
) -> str:
    return json.dumps({
        "dependencies": dict.fromkeys(dependencies, "workspace:*"),
        "devDependencies": dict.fromkeys(development_dependencies, "workspace:*"),
        "exports": "./index.ts",
        "name": f"@fixture/{name}",
        "private": True,
        "type": "module",
        "workspaces": ["packages/*"],
    })


def _read_workspace_files() -> tuple[tuple[str, str], ...]:
    return (
        (
            APPLICATION_MANIFEST,
            _serialize_manifest(name="application", dependencies=("@fixture/lib",)),
        ),
        (LIBRARY_MANIFEST, _serialize_manifest(name="lib")),
        (SUPPORT_MANIFEST, _serialize_manifest(name="test-support")),
        (
            "index.ts",
            'import { value } from "@fixture/lib";\nexport const result = value;\n',
        ),
        ("packages/lib/index.ts", "export const value = 1;\n"),
        ("packages/test-support/index.ts", "export const support = 1;\n"),
    )


def _read_membership_fixtures() -> tuple[Fixture, ...]:
    return (
        Fixture(name="allowed-package-edge"),
        Fixture(
            name="new-member-needs-declaration",
            files=(("packages/unlisted/package.json", _serialize_manifest(name="unlisted")),),
            diagnostic="undeclared package: packages/unlisted/package.json",
        ),
        Fixture(
            name="manifest-edge-needs-declaration",
            declarations=(),
            diagnostic="undeclared internal dependency",
        ),
        Fixture(
            name="unused-declaration-is-rejected",
            files=((APPLICATION_MANIFEST, _serialize_manifest(name="application")),),
            diagnostic="unused declared dependency",
        ),
        Fixture(
            name="declared-package-cycle-is-rejected",
            declarations=(
                (APPLICATION_MANIFEST, LIBRARY_MANIFEST, False),
                (LIBRARY_MANIFEST, APPLICATION_MANIFEST, False),
            ),
            files=(
                (
                    LIBRARY_MANIFEST,
                    _serialize_manifest(name="lib", dependencies=("@fixture/application",)),
                ),
            ),
            diagnostic="CycleError",
        ),
    )


def _read_source_edge_fixtures() -> tuple[Fixture, ...]:
    return (
        Fixture(
            name="relative-import-cannot-bypass-package-policy",
            declarations=(),
            files=(
                (APPLICATION_MANIFEST, _serialize_manifest(name="application")),
                (
                    "index.ts",
                    'export { value } from "./packages/lib/index.ts";\n',
                ),
            ),
            diagnostic="import crosses an undeclared package edge",
        ),
        Fixture(
            name="unresolved-import-is-rejected",
            files=(("index.ts", 'export { absent } from "./missing.ts";\n'),),
            diagnostic="unresolved dependency",
        ),
        Fixture(
            name="unknown-policy-field-is-rejected",
            has_unknown_policy_field=True,
            diagnostic="read dependency policy",
        ),
    )


def _read_test_support_fixtures() -> tuple[Fixture, ...]:
    manifest = _serialize_manifest(
        name="application",
        dependencies=("@fixture/lib",),
        development_dependencies=("@fixture/test-support",),
    )
    test_source = """import { support } from "@fixture/test-support";
export const result = support;
"""
    support_files = (
        (
            SUPPORT_MANIFEST,
            _serialize_manifest(name="test-support", dependencies=("@fixture/application",)),
        ),
        (
            "packages/test-support/index.ts",
            'import { result } from "@fixture/application";\nexport const support = result;\n',
        ),
    )

    return (
        Fixture(
            name="tests-can-import-test-support-with-package-cycle",
            declarations=TEST_SUPPORT_EDGES,
            files=(
                *support_files,
                (APPLICATION_MANIFEST, manifest),
                ("tests/support.test.ts", test_source),
            ),
        ),
        Fixture(
            name="production-cannot-import-test-support",
            declarations=TEST_SUPPORT_EDGES,
            files=(
                *support_files,
                (APPLICATION_MANIFEST, manifest),
                ("production.ts", test_source),
            ),
            diagnostic="production code imports test-support package",
        ),
        Fixture(
            name="test-only-target-must-be-test-support",
            declarations=TEST_SUPPORT_EDGES,
            files=(
                *support_files,
                (APPLICATION_MANIFEST, manifest),
                ("tests/support.test.ts", test_source),
            ),
            is_test_support=False,
            diagnostic="test-only edge targets a package not declared as test support",
        ),
        Fixture(
            name="test-only-support-needs-development-manifest",
            declarations=TEST_SUPPORT_EDGES,
            files=(
                *support_files,
                (
                    APPLICATION_MANIFEST,
                    _serialize_manifest(
                        name="application", dependencies=("@fixture/lib", "@fixture/test-support")
                    ),
                ),
                ("tests/support.test.ts", test_source),
            ),
            diagnostic="test-only dependency is in a production manifest section",
        ),
    )


def _read_source_cycle_fixtures() -> tuple[Fixture, ...]:
    files = (
        (
            "packages/lib/index.ts",
            """import type { Detail } from "./detail.ts";
export type Value = Detail;
export const value = 1;
""",
        ),
        (
            "packages/lib/detail.ts",
            """export type Detail = { value: number };
export const read = () => import("./index.ts");
""",
        ),
    )

    return (
        Fixture(name="optional-module-policy-allows-acyclic-source", has_source_rules=True),
        Fixture(name="package-policy-allows-internal-source-cycle", files=files),
        Fixture(
            name="optional-module-policy-rejects-type-and-dynamic-cycle",
            files=files,
            has_source_rules=True,
            diagnostic="acyclic-source-imports",
        ),
    )


def _read_projection_fixtures() -> tuple[Fixture, ...]:
    return (
        Fixture(name="derived-package-projection-is-current", has_projection=True),
        Fixture(
            name="derived-package-projection-cannot-drift",
            diagnostic="stale package projection",
            has_projection=True,
            is_projection_stale=True,
        ),
    )


def read_fixtures() -> tuple[Fixture, ...]:
    """Pair package and source-policy failures with valid native-resolution examples."""
    fixtures = (
        *_read_membership_fixtures(),
        *_read_source_edge_fixtures(),
        *_read_test_support_fixtures(),
        *_read_source_cycle_fixtures(),
        *_read_projection_fixtures(),
    )
    files = _read_workspace_files()

    return tuple(replace(fixture, files=(*files, *fixture.files)) for fixture in fixtures)
