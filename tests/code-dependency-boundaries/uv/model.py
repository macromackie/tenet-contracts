"""Keep fixture inputs and expected rejection evidence outside assessed source."""

from dataclasses import dataclass

from constants import APPLICATION_EDGES


@dataclass(frozen=True, kw_only=True)
class Fixture:
    """Describe one isolated package graph and its observable checker result."""

    name: str
    files: tuple[tuple[str, str], ...] = ()
    declarations: tuple[tuple[str, str, bool], ...] = APPLICATION_EDGES
    diagnostic: str = ""
    has_projection: bool = False
    has_source_rules: bool = False
    has_unknown_policy_field: bool = False
    is_projection_stale: bool = False
    is_test_support: bool = True
