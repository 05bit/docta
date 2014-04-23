The quickest way
================

Docta is written in [Python](http://python.org), so if you're familiar with its [installer tools](http://pip.readthedocs.org/en/latest/installing.html):

```bash
$ pip install docta
```

Anyway, Python must present in system for running Docta. You may check it with command:

```bash
$ python --version
Python 2.7.6
```

Versions 2.7.x and 3.2.x are great, older ones may also work.

From GitHub
===========

If you have Python installed but pip-way is not for you for some reasons:

```bash
$ git clone https://github.com/05bit/python-docta.git
$ cd python-docta
$ python setup.py install
```

Sometimes you may also need `sudo` for the last command on UNIX systems:

```bash
$ sudo python setup.py install
```

Result
======

On successful installation you should be able to run `docta` command

```bash
$ docta
```

and get a help message:

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

If you see it, you have won!

[Tutorial &rarr;](../tutorial/)
