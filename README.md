# DockerI

My use case for Docker is of a packaging system, where stable versions of
everyday tools I develop and/or use will be encapsulated.
Some of these tools will make use of network with a browser/html interface,
some will use X11 system and most of them will accept/return data files.

When we start using docker features/options the command line becomes somewhat
ugly and, for daily/frequently used software, it starts to be painful.

This interface has two purposes:
* to save images' common options in a config file
* to deal with graphical (X11) interface access in Linux and Mac

## Install

To use this interface -- `dockeri` -- we need Python-2.
And if you're running from a MacOS, XQuartz needs to be installed
if you plan to run graphical tools.

With that in place, all you have to do to run `dockeri` from anywhere in your
system is to update your environment variable `$PATH`:

```
 export PATH="${PATH}:${DOCKERIDIR}/bin"
```

[]
