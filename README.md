# Docker*i*

Docker*i* is that missing *interface* for Docker.

Use `dockei` to **run** docker containers with a simplified call.
When using frequently containers, with always the same --and long--
'`docker run`' command line, starts to get boring all that typing.
That's why I wrote `dockeri`.
Dockeri uses configuration files to hide unnecessary complexity of
everyday Docker (run) calls, as well as **X11** support.

My use case for Docker is of a packaging system for (astronomical)
tools I use daily between Linux and MacOS systems.
Some of these tools will make use of network with a browser/html interface,
some will use X11 system and most of them will accept/return data files.

The main purpose of `dockeri` is to handle the complexity (and, yes, uglyness)
of `docker run` command line; this is particularly for the case of everyday
containers used as app bundles. 

Dockeri features:
- [x] save images' common options in a config file
- [x] deal with graphical (X11) interface access in Linux and Mac


## How to install?

Docker*i* works with Python2 *and* Python3, and has *no* external dependencies; it uses only Python's core/std-lib.

*If you're a Mac user, see also below, the MacOSX section*

`dockeri` is implemented in Python. Runs in Python 2 and 3, and
does *not* depend on external libraries; only Python's standard library.
</div>

To install it, simply goes

* *download* the last [release](https://github.com/chbrandt/dockeri/releases)
* *unpack* the downloaded file
* go inside the package

and type:
```bash
$ python setup.py install
```
or (recommended):
```bash
$ pip install .
```

---

#### MacOSX

Mac users *must* have [XQuartz](https://www.xquartz.org/) installed if willing to use X from inside containers.

After XQuartz is installed the option for "*Allow connections from network clients*" should be enabled:

![XQuartz settings]({{site.url}}/docs/XQuartz_allow_connections.png)

---

## How to use?

After installing it, `dockeri` is available from anywhere in the system.

Simply type `dockeri` to gets is short *usage* signature:
```
$ dockeri

usage: dockeri [-h] [-w IO_DIR] [--nox] [-d] [-n] [-l] image
```

If you want to run the official `ubuntu` image, type:
```
$ dockeri ubuntu
```

`dockeri` has also a *help* option to explain you better the available options:
```
$ dockeri --help

usage: dockeri [-h] [-w IO_DIR] [--nox] [-d] [-n] [-l]

Interface for Docker containers.

optional arguments:
  -h, --help            show this help message and exit
  -w IO_DIR, --io IO_DIR
                        directory to use for files exchange with container
                        (inside container it is '/work'.
  --nox                 do *not* export graphical interface (x11) from the
                        container to host (*do* export by deafult)
  -d                    runs non-interactively (detached mode)
  -n, --dry-run         don't run the container, just print the command-line
                        instead
  -l, --list            print list of preset images
```

For instance, Dockeri comes with a list of preset images in the default
configuration files.
To see what in the list, type:
```bash
$ dockeri --list
List of available/preset images:
- annz
- dachs
- ds9
- gollum
- heasoft
- jupyter
- topcat
```

/.\
