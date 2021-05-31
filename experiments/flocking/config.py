import toml

with open("experiments/flocking/config.toml", "r") as f:
    config = toml.load(f)
