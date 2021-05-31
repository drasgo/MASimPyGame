import toml

with open("experiments/aggregation/config.toml", "r") as f:
    config = toml.load(f)
