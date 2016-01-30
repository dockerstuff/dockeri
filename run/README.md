# Docker-i run interface

  `dockeri` will run `docker run` for a given Docker image, automatically filling some optional fields pre-defined in its configuration files.
  `dockeri -h` is available to help you with the available options.
  The basic use of it is by just typing `dockeri some_image`. `dockeri` then proceed as follows:
  * it searchs for a config file matching the image name ("some_image").
    * the "matching" config file/image name is based on the config file rootname, which should match with the image name.
  * if the corresponding config file is not found, or config content section:key=value "main:image=name" is not found, the pull (from docker hub) is done with the given image name (e.g, "some_image") and default options are used.
    * for `dockeri` default options see belo at `recognised options`.
  
  `dockeri` uses the value of `DOCKERIRDIR` environment variable to localize the config files. This variable should point to the directory containing dockeri's directories `conf.d` and `bin`; see the here-below section `directory content` for an example.
  
### directory content
-----
.
├── bin
│   └── dockeri -> ../dockeri.py
├── conf.d
│   ├── annz.cfg
│   ├── asdcbibtool.cfg
│   ├── asdc.cfg
│   └── ds9.cfg
├── __init__.py
├── dockeri.py
├── config.py
└── x11.py
-----

## recognised options

### config file structure

* Disconsider the "< >" symbols!

```
[main]
image = <repo/image>

[volumes]
input = <host absolute-or-relative dir to use as container's "/input"
output = <host absolute-or-relative dir to use as container's "/output"
```

### default values

  * main:image = ''
  * volumes:input = 'input'
  * volumes:output = 'output'


