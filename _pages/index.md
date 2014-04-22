---
title: Docta
---

Meet Docta!
===========

<big>[**Docta**](https://github.com/05bit/python-docta) is a new healing documentation kit.</big>

It's in early stage at the moment, but all basics is working!

<a name="quickstart"></a>
### Quickstart

Setup new project:

```bash
$ mkdir docs
$ cd docs
$ docta init
```

And project is ready for building!

```bash
$ docta build
$ docta serve --watch
```

After running *build* and *serve* commands you should see something like:

```bash
Serving directory: /home/user/docs/_html
Running at http://127.0.0.1:8000
23 April 2014 - 02:14:36
```

<a name="overview"></a>
Overview
--------

Consider Docta as **static-site generator focused on building docs**!

Essential features:

* Powered by GitHub Flavoured Markdown
* Easy way styles and templates overriding
* Custom navigation
* Smart preview server with auto-rebuild

<a name="install"></a>
Install
-------

Easiest way to install is via <a href="http://www.pip-installer.org/en/latest/quickstart.html" target="_blank">pip</a>:

```bash
$ pip install docta
```

More complicated

```bash
$ git clone https://github.com/05bit/python-docta.git
$ cd python-docta
$ python setup.py install
```
