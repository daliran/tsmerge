"""Tests for tsmerge/run.py: the records every experiment writes (ED-009, ED-026)."""

import json

import pytest

from tsmerge import run


@pytest.fixture
def run_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("RUN_DIR", str(tmp_path))
    return tmp_path


def test_metrics_are_written_in_the_fixed_format(run_dir):
    run.write_metrics(
        [{"phase": "merged", "split": "test", "metric": "mse", "value": 1}]
    )
    records = json.loads((run_dir / "results" / "metrics.json").read_text())
    assert records == [
        {"phase": "merged", "split": "test", "metric": "mse", "value": 1.0}
    ]


@pytest.mark.parametrize(
    "record",
    [
        {"split": "test", "metric": "mse"},
        {"split": "holdout", "metric": "mse", "value": 1.0},
        {"split": "test", "metric": "mse", "value": 1.0, "seed": 0},
    ],
)
def test_metrics_outside_the_format_are_refused(run_dir, record):
    with pytest.raises(ValueError):
        run.write_metrics([record])
    assert not (run_dir / "results" / "metrics.json").exists()


def test_config_has_the_four_sections(run_dir):
    numerics = run.set_numerics()
    run.write_config({"lr": 0.1}, {"train": 0, "eval": 1}, [], numerics)
    record = json.loads((run_dir / "config.json").read_text())
    assert set(record) == {"config", "seeds", "data", "determinism"}
    assert record["determinism"]["allow_tf32_matmul"] is False


def test_outside_a_recorded_run_outputs_go_to_scratch(monkeypatch):
    monkeypatch.delenv("RUN_DIR", raising=False)
    assert run.run_dir() == run.REPO / "outputs" / "scratch"


def test_history_appends_one_line_per_value(run_dir):
    run.log_history(1, "train", "loss", 2.0)
    run.log_history(2, "val", "loss", 1.5, epoch=1)
    lines = (run_dir / "results" / "history.jsonl").read_text().splitlines()
    assert [json.loads(line) for line in lines] == [
        {"step": 1, "split": "train", "metric": "loss", "value": 2.0},
        {"step": 2, "epoch": 1, "split": "val", "metric": "loss", "value": 1.5},
    ]


def test_history_refuses_unknown_fields(run_dir):
    with pytest.raises(ValueError):
        run.log_history(1, "train", "loss", 2.0, seed=0)


def test_a_new_run_starts_a_new_curve(run_dir):
    run.log_history(1, "train", "loss", 2.0)
    run.write_config({}, {"train": 0, "eval": 1}, [], {})
    assert not (run_dir / "results" / "history.jsonl").exists()
