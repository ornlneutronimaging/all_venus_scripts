#!/bin/bash

pixi run --manifest-path /SNS/VENUS/shared/software/git/all_venus_scripts/pixi.toml list_nexus_pvs "$@"


# pixi run --manifest-path /SNS/VENUS/shared/software/git/all_venus_scripts/pixi.toml list_nexus_pvs 9235,9236
# pixi run --manifest-path /SNS/VENUS/shared/software/git/all_venus_scripts/pixi.toml list_nexus_pvs 9235,9236 --ipts IPTS-35945