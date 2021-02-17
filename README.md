# PyRI Open Source Teach Pendant Device Manager

The sandbox executes user programs in the Restricted Python Environment. It is also able to compile blockly programs to Python for execution.

## Setup

The `pyri-sandbox` package should be installed into a virtual environment using the command:

```
python3 -m pip install -e .
```

See https://github.com/pyri-project/pyri-core for more information on setting up the virtual environment.

# Startup

The `pyri-variable-storage` service must be running before use. See https://github.com/pyri-project/pyri-variable-storage

The `pyri-device-manager` service must be running before use. See https://github.com/pyri-project/pyri-device-manager

To start the service, run:

```
pyri-sandbox-service --device-info-file=config/pyri_sandbox_default_info.yml --device-manager-url=rr+tcp://localhost:59902?service=device_manager
```