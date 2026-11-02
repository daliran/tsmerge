"""The smallest complete experiment: the template for real ones, and the smoke test.

It prints what PyTorch sees, then fits a linear model to synthetic data, going through
every step a real experiment takes: settings, seeds, numerics, config.json, training
(with its curve in results/history.jsonl), results/metrics.json.

usage: python -m tsmerge.hello [--steps N] [--seed S] [--device auto|cpu|cuda]
  recorded:  scripts/run_local.sh hello python -m tsmerge.hello
             scripts/cluster/submit.sh hello python -m tsmerge.hello
"""

import argparse
import platform
from dataclasses import asdict, dataclass

import torch

from tsmerge import run


@dataclass
class Config:
    steps: int = 200
    lr: float = 0.1
    samples: int = 1024
    features: int = 8
    seed: int = 0
    device: str = "auto"


def parse() -> Config:
    defaults = Config()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for name, value in asdict(defaults).items():
        parser.add_argument(f"--{name}", type=type(value), default=value)
    return Config(**vars(parser.parse_args()))


def environment() -> None:
    print(f"python {platform.python_version()}, torch {torch.__version__}")
    print(f"cuda available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        major, minor = torch.cuda.get_device_capability(0)
        print(f"gpu: {torch.cuda.get_device_name(0)} (capability {major}.{minor})")


def main() -> None:
    config = parse()
    environment()
    device = run.device(config.device)
    seeds = {"train": config.seed, "eval": config.seed + 1}
    run.seed_everything(seeds["train"])
    numerics = run.set_numerics()
    # Before any computation: the record of what this run computes with (PD-009).
    data = [{"name": "synthetic-linear", "source": "generated from the seeds"}]
    run.write_config(asdict(config), seeds, data, numerics)

    # Synthetic data: y = x @ true_w + noise; the true weights are fixed for every run.
    true_w = torch.randn(
        config.features, 1, generator=torch.Generator().manual_seed(99)
    )

    def sample(generator: torch.Generator) -> tuple[torch.Tensor, torch.Tensor]:
        x = torch.randn(config.samples, config.features, generator=generator)
        noise = 0.1 * torch.randn(config.samples, 1, generator=generator)
        return x.to(device), (x @ true_w + noise).to(device)

    x_train, y_train = sample(torch.Generator().manual_seed(seeds["train"]))
    x_val, y_val = sample(torch.Generator().manual_seed(seeds["eval"]))

    model = torch.nn.Linear(config.features, 1).to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=config.lr)
    loss_fn = torch.nn.MSELoss()
    for step in range(1, config.steps + 1):
        optimizer.zero_grad()
        loss = loss_fn(model(x_train), y_train)
        loss.backward()
        optimizer.step()
        if step % 50 == 0 or step == config.steps:
            run.log_history(step, "train", "mse", loss.item())
            print(f"step {step}: train mse {loss.item():.4f}")

    with torch.no_grad():
        val_mse = loss_fn(model(x_val), y_val).item()
    path = run.write_metrics(
        [
            {"split": "train", "metric": "mse", "value": loss.item()},
            {"split": "val", "metric": "mse", "value": val_mse},
        ]
    )
    print(f"val mse {val_mse:.4f}; written: {path}")


if __name__ == "__main__":
    main()
