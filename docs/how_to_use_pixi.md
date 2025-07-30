# Overview

This document provides a high-level guide on how to leverage [Pixi](https://pixi.sh/latest/) to manage a Git repo.

## Initialize Pixi

Depending on the goal of the repository, you need to adjust how Pixi is initialized:

- **For standard Python packages projects**: we need to use `pyproject.toml` to manage the Python packaging, and we will add the pixi configuration in the same file. From the commandline, run:

```bash
pixi init --format pyproject
```

- **For other type of projects**: if the project contains more than just Python packages (hybrid-language projects) or it does not contain Python packages at all, we will use `pixi` as a virtual environment manager. In this case, run:

```bash
pixi init
```

## Adding dependencies

If there is already an `environment.yml` file in the repository, you can import it with

```bash
pixi init --import environment.yml 
```

Otherwise, you need to add dependencies manually.
Generally speaking, you should only add the dependencies that are the root of the dependency tree, i.e. the dependencies that are not used by other dependencies.
A simple way to do this would be asking the copilot to scan the deps in this repo, and provide with the list.
Most of the time, the dependencies will be good enough for project management purpose.

For dependencies that needs to be installed from `conda-forge`, use

```bash
pixi add <package_name>
```

If you need to install a conda package from a specific channel, you need to first add the channel to the project:

```bash
pixi project channel add <channel_name>
```

Then you can add the package from that channel:

```bash
pixi add <channel_name>/<package_name>
```

For example, to properly add `pytorch` from the `pytorch` channel, you would do:

```bash
pixi project channel add pytorch nvidia
pixi add pytorch::pytorch pytorch::pytorch-cuda
```

> Note: `pixi` follows the channel order strictly, so if you run into issues where 3rd party packages are not installed from the expected channel, make sure to specify the channel explicitly like the example above.

## Add Platforms

You will need to manually add additional platforms to the project if your local development OS is different from the deployment OS.
For example, if you are developing on macOS but deploying on Linux, you can add the Linux platform with:

```bash
pixi project platform add linux-64
```

## Add Tasks

You can add tasks directly by editing the `pixi.toml` file, or you can use the command line to add tasks.
For example, to add the task `list_nexus_pvs`, you can run:

```bash
pixi task add list_nexus_pvs "python jean_scripts/list_nexus_pvs.py"
```
