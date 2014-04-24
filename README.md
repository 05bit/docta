[**Docta**](http://docta.05bit.com) is a new healing docs kit.
==============================================================

Technically speaking, it's a **static-site generator** slightly focused on **building documetation**.

Project homepage: http://docta.05bit.com

Current version: **v0.1**, 2014 Apr 24

Install
-------

Easiest way to install is via <a href="http://www.pip-installer.org/en/latest/quickstart.html" target="_blank">pip</a>:

```bash
$ pip install docta
```

Quickstart
----------

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

Thats it! You may edit or create **.md** files, starting from **index.md** with your favorite text editor.

License
-------

Docta is distributed for free and its source code is licensed under the [BSD 3-Clause License](https://github.com/05bit/python-docta/blob/master/LICENSE).
