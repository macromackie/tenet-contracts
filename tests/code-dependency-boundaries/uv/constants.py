"""Name the temporary workspace's package identities and process bounds."""

APPLICATION_MANIFEST = "package.json"
LIBRARY_MANIFEST = "packages/lib/package.json"
SUPPORT_MANIFEST = "packages/test-support/package.json"
MEMBERS = (
    (APPLICATION_MANIFEST, "application"),
    (LIBRARY_MANIFEST, "lib"),
    (SUPPORT_MANIFEST, "test-support"),
)
APPLICATION_EDGES = ((APPLICATION_MANIFEST, LIBRARY_MANIFEST, False),)
TEST_SUPPORT_EDGES = (
    *APPLICATION_EDGES,
    (APPLICATION_MANIFEST, SUPPORT_MANIFEST, True),
    (SUPPORT_MANIFEST, APPLICATION_MANIFEST, False),
)
GUIDANCE_PARENT_DEPTH = 3
CHECKER_PATH = "contracts/code-dependency-boundaries/assets/uv/check-package-boundaries.py"
FIXTURE_TIMEOUT_SECONDS = 60
OUTPUT_CHARACTER_LIMIT = 6000
PROJECTION_PATH = "packages/lib/package-boundaries.json"
