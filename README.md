<p align="center">
<img src="./doc/figures/pyri_logo_web.svg" height="200"/>
</p>

# PyRI Open Source Teach Pendant Sandbox

This package is part of the PyRI project. See https://github.com/pyri-project/pyri-core#documentation for documentation. This package is included in the `pyri-robotics-superpack` Conda package.

The `pyri-sandbox` package contains the sandbox service which executes user procedures in the Restricted Python Environment. It is also able to compile Blockly programs to Python for execution.

## Service

This service is started automatically by `pyri-core`, and does not normally need to be started manually.

The `pyri-variable-storage` service must be running before use. See https://github.com/pyri-project/pyri-variable-storage

Standalone service command line example:

```
pyri-sandbox-service
```

The `pyri-variable-storage` and `pyri-device-manager` services must be running before use.

Command line options:

| Option | Type | Required | Description |
| ---    | ---  | ---      | ---         |
| `--device-manager-url=` | Robot Raconteur URL | No | Robot Raconteur URL of device manager service |
| `--device-manager-identifier=` | Identifier | No | Robot Raconteur device identifier in string format for device manager service |
| `--device-info-file=` | File | No | Robot Raconteur `DeviceInfo` YAML file. Defaults to contents of `pyri_sandbox_default_info.yml` |

This service may use any standard `--robotraconteur-*` service node options.

This service uses the `DeviceManagerClient`, which needs to connect to the device manager service to find other devices. This can be done using discovery based on a Robot Raconteur device identifier, or using a specified Robot Raconteur URL. If neither is specified, the `DeviceManagerClient` will search for the identifier named `pyri_device_manager` on the local machine.

## JavaScript Blockly Directory

The Blockly compiler is a Node.js JavaScript script, and requires many NPM packages. This requires installing the JavaScript packages and compilation script after the Python package has been installed. With the `pyri-conda-superpack`, all additional files are included so this is not necessary. If installing from a cloned repository, it is necessary to run the service with the `--install-blockly-compiler` flag to install the additional files.

The location of the additional directory can be set using the `PYRI_SANDBOX_BLOCKLY_COMPILER_DIR` environmental variable. If not set, the location defaults to the following on different platforms:

| Platform | Directory |
| ---      | ---       |
| Windows | %LOCALAPPDATA%\pyri-project\pyri-sandbox\blockly_compiler |
| Linux | ~/.local/share/pyri-sandbox/blockly_compiler |

## Development Setup

Most users should use Conda with the `pyri-robotics-superpack` to install this package. Developers need to run several install steps beyond `pip` commands.

See https://github.com/pyri-project/pyri-core for information on overall development environment configuration.

The sandbox requires NodeJS and npm to be installed. On Ubuntu, run:

```
sudo apt-get install nodejs npm
```

Once NodeJS and npm are installed, run the following command to configure the Blockly compiler:

```
pyri-sandbox-service --install-blockly-compiler
```

## Acknowledgment

This work was supported in part by Subaward No. ARM-TEC-19-01-F-24 from the Advanced Robotics for Manufacturing ("ARM") Institute under Agreement Number W911NF-17-3-0004 sponsored by the Office of the Secretary of Defense. ARM Project Management was provided by Christopher Adams. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of either ARM or the Office of the Secretary of Defense of the U.S. Government. The U.S. Government is authorized to reproduce and distribute reprints for Government purposes, notwithstanding any copyright notation herein.

This work was supported in part by the New York State Empire State Development Division of Science, Technology and Innovation (NYSTAR) under contract C160142. 

![](doc/figures/arm_logo.jpg) ![](doc/figures/nys_logo.jpg)

PyRI is developed by Rensselaer Polytechnic Institute, Wason Technology, LLC, and contributors.
