"""Checks that the generated SDKs cover the whole upstream spec and that our
overrides (names, deprecation, pagination, auth, environments) were applied.

These run offline against the generated source in sdks/.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from naming_map import OUT as NAMING_MAP, render  # noqa: E402
from overrides import load_yaml, operations, snake_case, stale_overrides  # noqa: E402

TS_SRC = ROOT / "sdks" / "typescript" / "src"
PY_SRC = ROOT / "sdks" / "python" / "src" / "t212"
OPS = operations()


def op_id(op) -> str:
    return f"{op.method.upper()} {op.path}"


def ts_client(group: str) -> str:
    return (TS_SRC / "api" / "resources" / group / "client" / "Client.ts").read_text()


def py_client(group: str) -> str:
    return (PY_SRC / group / "client.py").read_text()


def ts_method_block(source: str, method: str) -> str:
    """The JSDoc + signature of a public TS method."""
    match = re.search(rf"(/\*\*(?:(?!\*/).)*\*/\s*)public (?:async )?{method}\(", source, re.S)
    assert match, f"public method {method}() not found"
    return match.group(0)


def py_method_body(source: str, method: str, is_async: bool) -> str:
    prefix = "async def" if is_async else "def"
    match = re.search(rf"\n    {prefix} {method}\((.*?)(?=\n    (?:async )?def |\nclass |\Z)", source, re.S)
    assert match, f"{prefix} {method}() not found"
    return match.group(0)


# --- the overrides themselves -------------------------------------------------


@pytest.mark.parametrize("op", OPS, ids=op_id)
def test_every_operation_has_a_name(op):
    assert op.group, f"{op_id(op)} has no x-fern-sdk-group-name in fern/overrides.yml"
    assert op.sdk_method, f"{op_id(op)} has no x-fern-sdk-method-name in fern/overrides.yml"
    assert re.fullmatch(r"[a-z][a-zA-Z]*", op.sdk_method), "method names are written in camelCase"


def test_no_stale_overrides():
    assert stale_overrides() == [], "overrides reference operations that no longer exist upstream"


def test_names_are_unique():
    dupes = [k for k, n in Counter((o.group, o.sdk_method) for o in OPS).items() if n > 1]
    assert dupes == []


def test_upstream_deprecations_are_carried_over():
    for op in OPS:
        if op.upstream_deprecated:
            assert op.deprecated and op.deprecation_message, f"{op_id(op)} needs x-fern-availability"


def test_all_list_endpoints_with_next_page_path_are_paginated():
    spec = load_yaml(ROOT / "openapi" / "api.yaml")
    schemas = spec["components"]["schemas"]
    for op in OPS:
        responses = spec["paths"][op.path][op.method]["responses"]
        ref = responses.get("200", {}).get("content", {}).get("application/json", {}).get("schema", {}).get("$ref", "")
        has_next = "nextPagePath" in schemas.get(ref.rsplit("/", 1)[-1], {}).get("properties", {})
        assert has_next == op.paginated, f"{op_id(op)}: pagination override mismatch"


def test_naming_map_is_up_to_date():
    assert NAMING_MAP.read_text() == render(), "run python3 scripts/naming_map.py"


# --- generated TypeScript -------------------------------------------------------


@pytest.mark.parametrize("op", OPS, ids=op_id)
def test_typescript_method_exists(op):
    block = ts_method_block(ts_client(op.group), op.sdk_method)
    assert ("@deprecated" in block) == op.deprecated


@pytest.mark.parametrize("op", [o for o in OPS if o.paginated], ids=op_id)
def test_typescript_pagination(op):
    source = ts_client(op.group)
    signature = re.search(rf"public async {op.sdk_method}\(.*?\): (Promise<[^\n]*)", source, re.S)
    assert signature and "core.Page<" in signature.group(1)
    assert "response?.nextPagePath" in source
    # scripts/postprocess_typescript.py: Fern's url.join encodes the `?` in nextPagePath.
    assert "core.url.join(_baseUrl, response?.nextPagePath" not in source


def test_typescript_auth_and_environments():
    auth = (TS_SRC / "auth" / "BasicAuthProvider.ts").read_text()
    assert '"apiKey"' in auth and '"apiSecret"' in auth
    assert '"T212_API_KEY"' in auth and '"T212_API_SECRET"' in auth
    base = (TS_SRC / "BaseClient.ts").read_text()
    assert "authorization:" not in base, "legacy Authorization header option leaked into the client"
    envs = (TS_SRC / "environments.ts").read_text()
    assert 'Demo: "https://demo.trading212.com"' in envs
    assert 'Live: "https://live.trading212.com"' in envs


# --- generated Python -------------------------------------------------------------


@pytest.mark.parametrize("op", OPS, ids=op_id)
@pytest.mark.parametrize("is_async", [False, True], ids=["sync", "async"])
def test_python_method_exists(op, is_async):
    body = py_method_body(py_client(op.group), snake_case(op.sdk_method), is_async)
    assert ("DeprecationWarning" in body) == op.deprecated


def test_python_auth_and_environments():
    client = (PY_SRC / "client.py").read_text()
    assert 'os.getenv("T212_API_KEY")' in client and 'os.getenv("T212_API_SECRET")' in client
    envs = (PY_SRC / "environment.py").read_text()
    assert 'DEMO = "https://demo.trading212.com"' in envs
    assert 'LIVE = "https://live.trading212.com"' in envs


def test_python_hand_written_files_survive_regeneration():
    ignored = (PY_SRC / ".fernignore").read_text().split()
    for name in ("pagination.py", "py.typed"):
        assert name in ignored and (PY_SRC / name).exists()


# --- no upstream operationIds leak into either SDK ---------------------------------


@pytest.mark.parametrize("bad", ["orders_1", "placeStopOrder_1", "getAll", "getDetailed", "orderById"])
def test_upstream_operation_ids_do_not_leak(bad):
    for path in list(TS_SRC.rglob("*Client.ts")) + list(PY_SRC.rglob("client.py")):
        text = path.read_text()
        assert f" {bad}(" not in text and f" {snake_case(bad)}(" not in text, f"{bad} found in {path}"
