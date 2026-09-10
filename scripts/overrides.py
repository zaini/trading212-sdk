"""Shared helpers for reading the upstream spec and our Fern overrides."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "openapi" / "api.yaml"
OVERRIDES_PATH = ROOT / "fern" / "overrides.yml"

HTTP_METHODS = ("get", "post", "put", "patch", "delete")


@dataclass(frozen=True)
class Operation:
    path: str
    method: str
    operation_id: str | None
    summary: str | None
    upstream_deprecated: bool
    group: str | None
    sdk_method: str | None
    deprecated: bool
    deprecation_message: str | None
    paginated: bool


def load_yaml(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


def snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def operations() -> list[Operation]:
    """Every upstream operation, joined with the override that applies to it."""
    spec = load_yaml(SPEC_PATH)
    overrides = load_yaml(OVERRIDES_PATH).get("paths", {})
    ops = []
    for path, methods in spec["paths"].items():
        for method, op in methods.items():
            if method not in HTTP_METHODS:
                continue
            ov = overrides.get(path, {}).get(method, {})
            availability = ov.get("x-fern-availability") or {}
            ops.append(
                Operation(
                    path=path,
                    method=method,
                    operation_id=op.get("operationId"),
                    summary=op.get("summary"),
                    upstream_deprecated=bool(op.get("deprecated")),
                    group=ov.get("x-fern-sdk-group-name"),
                    sdk_method=ov.get("x-fern-sdk-method-name"),
                    deprecated=availability.get("status") == "deprecated" or bool(op.get("deprecated")),
                    deprecation_message=availability.get("message"),
                    paginated="x-fern-pagination" in ov,
                )
            )
    return ops


def stale_overrides() -> list[tuple[str, str]]:
    """Overrides that point at a path/method that no longer exists upstream."""
    spec_paths = load_yaml(SPEC_PATH)["paths"]
    overrides = load_yaml(OVERRIDES_PATH).get("paths", {})
    return [
        (path, method)
        for path, methods in overrides.items()
        for method in methods
        if method not in spec_paths.get(path, {})
    ]
