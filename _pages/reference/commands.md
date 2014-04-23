---
title: Commands
---

[draft]

Build HTML:

```bash
$ docta build
``` 

Serve HTML and watch for changes with auto-rebuild:

```bash
$ docta serve -w
``` 

Just serve:

```bash
$ docta serve
``` 

All commands:

```text
usage: docta [-h] [-c CONFIG] {init,config,build,serve,help} ...

Command line interface (CLI) for Docta.

positional arguments:
  {init,config,build,serve,help}
    init                start new docs project in current directory
    config              test and show project config
    build               build project
    serve               start local server for testing
    help                show this help message and exit

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config file to use [default: config.yaml]
```