# GRC Lab's Gateway
This project serves to create a network gateway management interface built entirely off of existing Linux networking components.
The functionality of this interface will rely upon the firewalld dbus integration, as such it is unlikely to be useable on the BSDs.
In the future I may update it to use nftables directly.

This interface should have complete network control of a host and provide software defined networking (SDN).
It needs to do at least what the networking application can do in cockpit.
I am mainly building this out of spite because I bought a UDM Pro SE and it's kinda a piece of shit so I wanna make something better than unifi.

## Requirements
* Linux
* Python 3.14+
* [Poetry](https://python-poetry.org/)
* [firewalld](https://firewalld.org/)
* [NetworkManager](https://www.networkmanager.dev/)

## Architecture
This project borrows heavily from a prior project of mine that may or may not continue to be developed.
This is designed around a plugin system that automatically loads utilities into the application.
This allows for a high level of modularity and isolation between parts of the code while still allowing interdependencies.
Furthermore, this project is designed in such a way that external plugins should be installable to the `grc.plugins` namespace package.
The plugin schema can be found in `grc.plugins.plugins.abstract` (yes the plugins system is loaded as a plugin).

## Using
The project is built as an ASGI application.
It comes with Uvicorn by default but should be compatible with any ASGI webserver.
I am currently not using any framework aside from Uvicorn but that may change.
There are multiple ways to run the application, the two I am focusing on are:

 * installation
 * running as a module
 * running as an ASGI application

### Installing
Install the application with poetry.
This will install the `grc-gateway` command.

```shell
$ poetry install
```

### Running as a module
This project is also designed to be run as both a module and a script.
Both of the following methods of running the application are supported:

```shell
# If installed
$ python -m grc
usage: python -m grc [-v | -q] [--suppress-stdout] [--output-log-file FILE] [--output-log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-h] [-V] PLUGIN ...
python -m grc: error: the following arguments are required: PLUGIN
# If running as script
$ python src/grc
usage: python src/grc [-v | -q] [--suppress-stdout] [--output-log-file FILE] [--output-log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-h] [-V] PLUGIN ...
python src/grc: error: the following arguments are required: PLUGIN
```

### Running as an ASGI application
The `grc:app` attribute is an ASGI application factory that can be run by ASGI servers.
To run using Uvicorn:
```shell\
# If installed
$ poetry run uvicorn --factory grc:app
```

## Configuring

### Uvicorn
Most of the Uvicorn configuration options have been provided as CLI flags, but configuration via environment variables is still supported.
If you don't want to use Uvicorn or need all options, feel free to run the project as an ASGI application to bypass the CLI.
