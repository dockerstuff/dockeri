# Dockeri

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

This interface has two purposes:
* to save images' common options in a config file
* to deal with graphical (X11) interface access in Linux and Mac


## Install

> MacOSX users must have [XQuartz](https://www.xquartz.org/) installed if willing to export X11 interfaces from containers

`dockeri` is implemented in Python. Runs in Python 2 and 3, and
does *not* depend on external libraries; only Python's standard library.

To install, download the last [release](https://github.com/chbrandt/dockeri/releases)
and do:
```bash
$ python setup.py install
```
or
```bash
$ pip install .
```


## How to use:

After installing it, `dockeri` is available from anywhere in the system.

Simply type `dockeri` to gets is short *usage* signature:
```bash
$ dockeri

usage: dockeri [-h] [-w IO_DIR] [--nox] [-d] [-n] [-l] image
```

If you want to run the official `ubuntu` image, type:
```
$ dockeri ubuntu
```

`dockeri` has also a *help* option to explain you better the available options:
```bash
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
