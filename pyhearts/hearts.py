#!/usr/bin/env python

import json
import random
import sys

import click
from faker import Faker

from pyhearts import players
from pyhearts import util
from pyhearts.game import HeartsTable


@click.command()
@click.option("--config-file", "config", type=str, default="./conf/basic_config.json")
@click.option("--seed", type=int, default=1)
def main(config, seed):
    """main funciton to run hearts games"""

    random.seed(seed)
    Faker.seed(seed)

    print(f"Loading game config from {config} file.")
    with open(config, "r") as f:
        json_config = json.load(f)

    hearts_table = HeartsTable(**json_config)
    print(hearts_table)

    hearts_table.play_games()


if __name__ == "__main__":
    main()
