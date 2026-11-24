#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Check secret delivery manifests against workflows, runtime bindings, and banned sync scripts."""

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

MANIFEST_VERSION = 1
ENVIRONMENT_KEY = "environment"
ENVIRONMENTS_KEY = "environments"
SECRETS_KEY = "secrets"
SECRET_NAME_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")
VAULT_REFERENCE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*/[A-Z][A-Z0-9_]*$")
WORKFLOW_SECRET_PATTERN = re.compile(r"\bsecrets\.(?P<name>[A-Z][A-Z0-9_]*)\b")
INHERITED_BINDING_PATTERNS = (
    re.compile(r'name\s*=\s*"(?P<name>[A-Z][A-Z0-9_]*)"\s*\n\s*type\s*=\s*"inherit"'),
    re.compile(r'type\s*=\s*"inherit"\s*\n\s*name\s*=\s*"(?P<name>[A-Z][A-Z0-9_]*)"'),
)
DEPLOYMENT_TARGET_KEYS = frozenset({"deployment", "github"})
RUNTIME_TARGET_KEYS = frozenset({"cloudflare", "runtime"})
ALLOWED_MANIFEST_KEYS = (
    frozenset({"$schema", "environment", "repository", "service", "version"})
    | DEPLOYMENT_TARGET_KEYS
    | RUNTIME_TARGET_KEYS
)
ALLOWED_DEPLOYMENT_KEYS = frozenset({"connection", ENVIRONMENT_KEY, ENVIRONMENTS_KEY, SECRETS_KEY})
ALLOWED_RUNTIME_KEYS = frozenset({"connection", "workers"})
ALLOWED_DEPLOYMENT_ENTRY_KEYS = frozenset({"name", "secret"})
ALLOWED_RUNTIME_ENTRY_KEYS = frozenset({"binding", "name", "secret"})


class SecretDeliveryRejected(ValueError):
    """The policy or secret manifest is malformed, or repository parity checks fail."""


@dataclass(frozen=True, kw_only=True)
class Policy:
    """The repository paths and patterns that govern declarative secret delivery."""

    manifest_path: str
    workflow_patterns: tuple[str, ...]
    runtime_binding_patterns: tuple[str, ...]
    banned_script_patterns: tuple[str, ...]
    builtin_workflow_secrets: frozenset[str]
    allowed_unused_manifest_secrets: frozenset[str]


@dataclass(frozen=True, kw_only=True)
class ParsedManifest:
    """The declared deployment and runtime secret names extracted from a valid manifest."""

    deployment_secrets: frozenset[str]
    runtime_bindings: frozenset[str]
    errors: tuple[str, ...]


@dataclass(frozen=True, kw_only=True)
class BindingSpec:
    """Validation rules for one list of deployment or runtime secret bindings."""

    scope: str
    key_name: str
    allowed_keys: frozenset[str]


def _read_relative_text(*, field: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip() or PurePosixPath(value).is_absolute():
        message = f"read policy field {field!r}: expected a nonempty relative path, got {value!r}"
        raise SecretDeliveryRejected(message)
    return value


def _read_secret_name(*, field: str, value: object) -> str:
    if not isinstance(value, str) or not SECRET_NAME_PATTERN.fullmatch(value):
        message = f"read policy secret {field!r}: expected SCREAMING_SNAKE_CASE, got {value!r}"
        raise SecretDeliveryRejected(message)
    return value


def _read_allowed_unused(*, value: object) -> str:
    match value:
        case {"name": str() as name, "reason": str() as reason, **extra} if (
            reason.strip() and not extra
        ):
            return _read_secret_name(field="allowedUnusedManifestSecrets", value=name)
        case _:
            message = f"read allowed unused secret {value!r}: declare a name and its reason"
            raise SecretDeliveryRejected(message)


def read_policy(*, path: Path) -> Policy:
    """Decode and validate the secret delivery policy JSON file."""
    document: object = json.loads(path.read_text(encoding="utf-8"))
    match document:
        case {
            "manifestPath": manifest_path,
            "workflowPatterns": [*workflow_patterns],
            "runtimeBindingPatterns": [*runtime_patterns],
            "bannedScriptPatterns": [*banned_patterns],
            "builtinWorkflowSecrets": [*builtin_secrets],
            "allowedUnusedManifestSecrets": [*allowed_unused],
            **unknown_fields,
        } if not unknown_fields:
            return Policy(
                manifest_path=_read_relative_text(field="manifestPath", value=manifest_path),
                workflow_patterns=tuple(
                    _read_relative_text(field="workflowPatterns", value=pattern)
                    for pattern in workflow_patterns
                ),
                runtime_binding_patterns=tuple(
                    _read_relative_text(field="runtimeBindingPatterns", value=pattern)
                    for pattern in runtime_patterns
                ),
                banned_script_patterns=tuple(
                    _read_relative_text(field="bannedScriptPatterns", value=pattern)
                    for pattern in banned_patterns
                ),
                builtin_workflow_secrets=frozenset(
                    _read_secret_name(field="builtinWorkflowSecrets", value=name)
                    for name in builtin_secrets
                ),
                allowed_unused_manifest_secrets=frozenset(
                    _read_allowed_unused(value=entry) for entry in allowed_unused
                ),
            )
        case _:
            message = (
                f"read secret delivery policy {str(path)!r}: declare manifestPath, "
                "workflowPatterns, runtimeBindingPatterns, bannedScriptPatterns, "
                "builtinWorkflowSecrets, and allowedUnusedManifestSecrets"
            )
            raise SecretDeliveryRejected(message)


def _check_extra_fields(
    *, place: str, fields: dict[object, object], allowed_keys: frozenset[str]
) -> list[str]:
    extras = sorted(str(key) for key in fields if key not in allowed_keys)
    if not extras:
        return []
    return [f"check manifest {place!r}: remove disallowed fields {extras!r}"]


def _check_binding_name(
    *, place: str, entry_fields: dict[object, object], spec: BindingSpec, seen_names: set[str]
) -> list[str]:
    raw_name = entry_fields.get(spec.key_name) or entry_fields.get("name")
    if not isinstance(raw_name, str) or not SECRET_NAME_PATTERN.fullmatch(raw_name):
        return [
            f"check manifest binding {place!r}: declare {spec.key_name!r} in SCREAMING_SNAKE_CASE"
        ]
    if raw_name in seen_names:
        return [f"check manifest scope {spec.scope!r}: remove duplicate binding {raw_name!r}"]
    seen_names.add(raw_name)
    return []


def _check_binding_entry(
    *, index: int, entry: object, spec: BindingSpec, seen_names: set[str]
) -> list[str]:
    place = f"{spec.scope}[{index}]"
    if not isinstance(entry, dict):
        return [f"check manifest binding {place!r}: expected an object"]
    errors = _check_extra_fields(
        place=f"binding {place}", fields=entry, allowed_keys=spec.allowed_keys
    )
    errors.extend(
        _check_binding_name(place=place, entry_fields=entry, spec=spec, seen_names=seen_names)
    )
    raw_secret = entry.get("secret")
    if not isinstance(raw_secret, str) or not VAULT_REFERENCE_PATTERN.fullmatch(raw_secret):
        errors.append(
            f"check manifest binding {place!r}: declare vault reference 'owner/SECRET_NAME'"
        )
    return errors


def _check_binding_list(
    *, scope: str, entries: object, key_name: str, allowed_keys: frozenset[str]
) -> tuple[set[str], list[str]]:
    if not isinstance(entries, list):
        return set(), [f"check manifest scope {scope!r}: declare a list of secret bindings"]
    spec = BindingSpec(scope=scope, key_name=key_name, allowed_keys=allowed_keys)
    seen_names: set[str] = set()
    errors = [
        error
        for index, entry in enumerate(entries)
        for error in _check_binding_entry(
            index=index, entry=entry, spec=spec, seen_names=seen_names
        )
    ]
    return seen_names, errors


def _check_named_groups(
    *,
    label: str,
    groups: object,
    section: str,
    key_name: str,
    allowed_keys: frozenset[str],
) -> tuple[set[str], list[str]]:
    if not isinstance(groups, dict) or not groups:
        return set(), [
            f"check manifest target {label!r}: declare at least one entry in {section!r}"
        ]
    declared_names: set[str] = set()
    errors: list[str] = []
    for group_name, bindings in groups.items():
        if not isinstance(group_name, str) or not group_name.strip():
            errors.append(f"check manifest target {label!r}: use nonempty names in {section!r}")
            continue
        names, group_errors = _check_binding_list(
            scope=f"{label}.{section}.{group_name}",
            entries=bindings,
            key_name=key_name,
            allowed_keys=allowed_keys,
        )
        declared_names |= names
        errors.extend(group_errors)
    return declared_names, errors


def _check_target_header(
    *, target_fields: dict[object, object], label: str, allowed_keys: frozenset[str]
) -> list[str]:
    errors = _check_extra_fields(
        place=f"target {label}", fields=target_fields, allowed_keys=allowed_keys
    )
    connection = target_fields.get("connection")
    if not isinstance(connection, str) or not connection.strip():
        errors.append(f"check manifest target {label!r}: declare a nonempty connection name")
    return errors


def _parse_single_environment(
    *, target_fields: dict[object, object], label: str
) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    env_name = target_fields.get(ENVIRONMENT_KEY)
    if not isinstance(env_name, str) or not env_name.strip():
        errors.append(f"check manifest target {label!r}: declare a nonempty environment name")
    declared_names, entry_errors = _check_binding_list(
        scope=f"{label}.{SECRETS_KEY}",
        entries=target_fields.get(SECRETS_KEY),
        key_name="name",
        allowed_keys=ALLOWED_DEPLOYMENT_ENTRY_KEYS,
    )
    return declared_names, [*errors, *entry_errors]


def _parse_deployment_target(*, target: object, label: str) -> tuple[set[str], list[str]]:
    if not isinstance(target, dict):
        return set(), [f"check manifest target {label!r}: expected an object"]
    errors = _check_target_header(
        target_fields=target, label=label, allowed_keys=ALLOWED_DEPLOYMENT_KEYS
    )
    has_single = ENVIRONMENT_KEY in target or SECRETS_KEY in target
    has_multi = ENVIRONMENTS_KEY in target
    if has_single and has_multi:
        return set(), [
            *errors,
            f"check manifest target {label!r}: use either environment/secrets or environments",
        ]
    if has_multi:
        declared_names, group_errors = _check_named_groups(
            label=label,
            groups=target.get(ENVIRONMENTS_KEY),
            section=ENVIRONMENTS_KEY,
            key_name="name",
            allowed_keys=ALLOWED_DEPLOYMENT_ENTRY_KEYS,
        )
        return declared_names, [*errors, *group_errors]
    declared_names, single_errors = _parse_single_environment(target_fields=target, label=label)
    return declared_names, [*errors, *single_errors]


def _parse_runtime_target(*, target: object, label: str) -> tuple[set[str], list[str]]:
    if not isinstance(target, dict):
        return set(), [f"check manifest target {label!r}: expected an object"]
    errors = _check_target_header(
        target_fields=target, label=label, allowed_keys=ALLOWED_RUNTIME_KEYS
    )
    declared_names, group_errors = _check_named_groups(
        label=label,
        groups=target.get("workers"),
        section="workers",
        key_name="binding",
        allowed_keys=ALLOWED_RUNTIME_ENTRY_KEYS,
    )
    return declared_names, [*errors, *group_errors]


def _check_manifest_header(*, path: Path, document_fields: dict[object, object]) -> list[str]:
    errors = _check_extra_fields(
        place=f"file {path}", fields=document_fields, allowed_keys=ALLOWED_MANIFEST_KEYS
    )
    if document_fields.get("version") != MANIFEST_VERSION:
        errors.append(f"check secret manifest {str(path)!r}: declare version {MANIFEST_VERSION!r}")
    repository = document_fields.get("repository")
    if not isinstance(repository, str) or not repository.strip():
        errors.append(f"check secret manifest {str(path)!r}: declare a nonempty repository")
    return errors


def _select_target(
    *,
    path: Path,
    document_fields: dict[object, object],
    keys: frozenset[str],
    kind: str,
) -> tuple[str | None, list[str]]:
    present = sorted(str(key) for key in keys if key in document_fields)
    if len(present) > 1:
        return None, [f"check secret manifest {str(path)!r}: declare only one {kind} target key"]
    return (present[0] if present else None), []


def parse_manifest(*, path: Path) -> ParsedManifest:
    """Read and validate the repository secret delivery manifest."""
    if not path.is_file():
        return ParsedManifest(
            deployment_secrets=frozenset(),
            runtime_bindings=frozenset(),
            errors=(f"read secret manifest {str(path)!r}: file does not exist",),
        )
    document: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        return ParsedManifest(
            deployment_secrets=frozenset(),
            runtime_bindings=frozenset(),
            errors=(f"read secret manifest {str(path)!r}: expected a JSON object",),
        )
    return _decode_manifest_document(path=path, document_fields=document)


def _decode_manifest_document(
    *, path: Path, document_fields: dict[object, object]
) -> ParsedManifest:
    errors = _check_manifest_header(path=path, document_fields=document_fields)
    deploy_key, deploy_key_errors = _select_target(
        path=path, document_fields=document_fields, keys=DEPLOYMENT_TARGET_KEYS, kind="deployment"
    )
    runtime_key, runtime_key_errors = _select_target(
        path=path, document_fields=document_fields, keys=RUNTIME_TARGET_KEYS, kind="runtime"
    )
    errors.extend([*deploy_key_errors, *runtime_key_errors])
    deployment_secrets, deploy_errors = (
        _parse_deployment_target(target=document_fields[deploy_key], label=deploy_key)
        if deploy_key is not None
        else (set(), [])
    )
    runtime_bindings, runtime_errors = (
        _parse_runtime_target(target=document_fields[runtime_key], label=runtime_key)
        if runtime_key is not None
        else (set(), [])
    )
    errors.extend([*deploy_errors, *runtime_errors])
    if deploy_key is None and runtime_key is None:
        errors.append(
            f"check secret manifest {str(path)!r}: declare a deployment or runtime target"
        )
    return ParsedManifest(
        deployment_secrets=frozenset(deployment_secrets),
        runtime_bindings=frozenset(runtime_bindings),
        errors=tuple(errors),
    )


def _read_matching_files(*, root: Path, patterns: tuple[str, ...]) -> list[tuple[str, str]]:
    paths = sorted({path for pattern in patterns for path in root.glob(pattern) if path.is_file()})
    return [(path.relative_to(root).as_posix(), path.read_text(encoding="utf-8")) for path in paths]


def _check_workflow_parity(
    *, root: Path, policy: Policy, declared_secrets: frozenset[str]
) -> list[str]:
    referenced_names: set[str] = set()
    errors: list[str] = []
    for relative, text in _read_matching_files(root=root, patterns=policy.workflow_patterns):
        names = {
            match["name"]
            for match in WORKFLOW_SECRET_PATTERN.finditer(text)
            if match["name"] not in policy.builtin_workflow_secrets
        }
        referenced_names |= names
        errors.extend(
            f"check workflow {relative!r}: declare secret {name!r} in {policy.manifest_path!r}"
            for name in sorted(names - declared_secrets)
        )
    unused_names = sorted(
        declared_secrets - referenced_names - policy.allowed_unused_manifest_secrets
    )
    errors.extend(
        f"check secret manifest {policy.manifest_path!r}: remove unused secret {name!r}"
        for name in unused_names
    )
    return errors


def _check_runtime_parity(
    *, root: Path, policy: Policy, declared_bindings: frozenset[str]
) -> list[str]:
    errors: list[str] = []
    for relative, text in _read_matching_files(root=root, patterns=policy.runtime_binding_patterns):
        names = {
            match["name"]
            for pattern in INHERITED_BINDING_PATTERNS
            for match in pattern.finditer(text)
        }
        errors.extend(
            f"check runtime definition {relative!r}: "
            f"declare inherited binding {name!r} in {policy.manifest_path!r}"
            for name in sorted(names - declared_bindings)
        )
    return errors


def _find_banned_scripts(*, root: Path, policy: Policy) -> list[str]:
    paths = sorted({
        path.relative_to(root).as_posix()
        for pattern in policy.banned_script_patterns
        for path in root.glob(pattern)
        if path.is_file()
    })
    return [
        f"check secret delivery script {relative!r}: remove ad-hoc secret sync script"
        for relative in paths
    ]


def inspect_secret_delivery(*, root: Path, policy: Policy) -> list[str]:
    """Check manifest structure, workflow parity, runtime binding parity, and banned scripts."""
    manifest = parse_manifest(path=root / policy.manifest_path)
    return [
        *manifest.errors,
        *_find_banned_scripts(root=root, policy=policy),
        *_check_workflow_parity(
            root=root, policy=policy, declared_secrets=manifest.deployment_secrets
        ),
        *_check_runtime_parity(
            root=root, policy=policy, declared_bindings=manifest.runtime_bindings
        ),
    ]


def main() -> None:
    """Validate secret delivery parity under the given workspace root without changing any file."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="repository root directory")
    parser.add_argument("--config", required=True, help="secret delivery policy path")
    parsed = parser.parse_args()
    workspace_root = Path(parsed.root).resolve()
    policy = read_policy(path=workspace_root / parsed.config)
    findings = inspect_secret_delivery(root=workspace_root, policy=policy)
    if findings:
        raise SecretDeliveryRejected("\n".join(findings))


if __name__ == "__main__":
    main()
