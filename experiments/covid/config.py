import toml

with open("experiments/covid/config.toml", "r") as f:
    config = toml.load(f)
