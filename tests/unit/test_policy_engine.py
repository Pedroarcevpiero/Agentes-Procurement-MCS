"""Unit tests de `guardrails/policy_engine.py`: carga y validacion de YAML.

Los casos felices cargan las politicas reales del repo
(`guardrails/policies/*.yaml`); los casos de error escriben YAML temporales
(`tmp_path`) para no depender de mutar los archivos reales del repo.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from procurement_agents.guardrails.policy_engine import (
    PolicyValidationError,
    load_category_copilot_policy,
    load_common_policy,
)


def test_load_common_policy_from_repo() -> None:
    policy = load_common_policy()
    assert "create_purchase_order" in policy.transactional_denylist
    assert "send_supplier_email" in policy.transactional_denylist
    assert "update_contract" in policy.transactional_denylist
    assert "sign_" in policy.transactional_denylist


def test_load_category_copilot_policy_from_repo() -> None:
    policy = load_category_copilot_policy()
    assert policy.min_confidence_auto_publish == pytest.approx(0.6)
    assert policy.max_auto_publish_usd == pytest.approx(250_000.0)
    assert policy.max_auto_publish_pct == pytest.approx(25.0)


def test_load_common_policy_missing_file(tmp_path: Path) -> None:
    with pytest.raises(PolicyValidationError, match="No existe"):
        load_common_policy(tmp_path / "does_not_exist.yaml")


def test_load_common_policy_empty_denylist_rejected(tmp_path: Path) -> None:
    path = tmp_path / "common.yaml"
    path.write_text("transactional_denylist: []\n", encoding="utf-8")
    with pytest.raises(PolicyValidationError, match="transactional_denylist"):
        load_common_policy(path)


def test_load_common_policy_non_string_items_rejected(tmp_path: Path) -> None:
    path = tmp_path / "common.yaml"
    path.write_text("transactional_denylist: [1, 2, 3]\n", encoding="utf-8")
    with pytest.raises(PolicyValidationError, match="strings"):
        load_common_policy(path)


def test_load_category_copilot_policy_missing_key(tmp_path: Path) -> None:
    path = tmp_path / "category_copilot.yaml"
    path.write_text(
        "min_confidence_auto_publish: 0.6\nmax_auto_publish_usd: 250000\n",
        encoding="utf-8",
    )
    with pytest.raises(PolicyValidationError, match="max_auto_publish_pct"):
        load_category_copilot_policy(path)


def test_load_category_copilot_policy_confidence_out_of_range(tmp_path: Path) -> None:
    path = tmp_path / "category_copilot.yaml"
    path.write_text(
        "min_confidence_auto_publish: 1.5\nmax_auto_publish_usd: 250000\nmax_auto_publish_pct: 25\n",
        encoding="utf-8",
    )
    with pytest.raises(PolicyValidationError, match=r"\[0.0, 1.0\]"):
        load_category_copilot_policy(path)


def test_load_category_copilot_policy_non_numeric_rejected(tmp_path: Path) -> None:
    path = tmp_path / "category_copilot.yaml"
    path.write_text(
        'min_confidence_auto_publish: "alta"\nmax_auto_publish_usd: 250000\nmax_auto_publish_pct: 25\n',
        encoding="utf-8",
    )
    with pytest.raises(PolicyValidationError, match="numerico"):
        load_category_copilot_policy(path)


def test_load_common_policy_root_not_mapping(tmp_path: Path) -> None:
    path = tmp_path / "common.yaml"
    path.write_text("- a\n- b\n", encoding="utf-8")
    with pytest.raises(PolicyValidationError, match="mapping"):
        load_common_policy(path)
