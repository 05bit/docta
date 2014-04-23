---
title: Docta
---

## [**Docta**](https://github.com/05bit/python-docta) is a new healing documentation kit.

Technically speaking, it's a **static-site generator slightly focused on building documetation**!

<a name="quickstart"></a>
### Quickstart

Setup a new project:

```bash
$ mkdir docs
$ cd docs
$ docta init
```

That's it! Project is ready for building!

```bash
$ docta build
$ docta serve --watch
```

After running `build` and `serve` commands you should see something like:

```bash
Serving directory: /home/user/docs/_html
Running at http://127.0.0.1:8000
23 April 2014 - 02:14:36
```

Now you may edit or create **.md** files, starting from **index.md** and so on with your favorite text editor.

![Docta .md file example](assets/img/screenshot1.jpg)

<a name="overview"></a>
Overview
--------

Docta is a **lightweight** tool built on top of **modern and proven** technologies.

* Powered by <a href="https://help.github.com/articles/github-flavored-markdown" target="_blank">**Markdown with flavours**</a>
* Plays really well with <a href="https://pages.github.com/" target="_blank">**GitHub Pages**</a>
* Nice readable config format, well it's YAML
* Configurable navigation with icons option
* Basic themes powered by <a href="http://getbootstrap.com/" target="_blank">**Bootstrap**</a>
* Clean and explicit templates powered by <a href="http://jinja.pocoo.org/docs/templates/" target="_blank">**Jinja**</a>
* Smart preview server with auto-rebuild

<a name="install"></a>
Install
-------

Easiest way to install is via <a href="http://www.pip-installer.org/en/latest/quickstart.html" target="_blank">pip</a>:

```bash
$ pip install docta
```

[Read more about installing Docta &rarr;](install/)

License
-------

Docta is distributed for free and its source code is licensed under the [BSD 3-Clause License](https://github.com/05bit/python-docta/blob/master/LICENSE).
