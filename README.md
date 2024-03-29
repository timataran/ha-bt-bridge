# Bluetooth devices connection to Home Assistant over MQTT

## How it works

At the moment ha-bt-bridge is standalone application that connects to MQTT broker and to 
one or more bluetooth devices. Connection to broker and devices are being configured in its own config file. 
Application registers devices in Home Assistant 
using [MQTT discovery](https://www.home-assistant.io/docs/mqtt/discovery/), so there is no need 
in additional configuration on HA side.

## Configuration

Initial configuration can be created by copying `config/example.configuration.yml` to file `config/configuration.yml`.

The configuration has three sections, `mqtt`, `timer`, `device`.

### mqtt

It describes connection to MQTT broker. Parameters:

| parameter      | description                            |
|----------------|----------------------------------------|
|broker          | mqtt broker address                    |
|port            | mqtt broker port                       |
|username        | username                               |
|password        | password                               |
|discovery_prefix| configured in HA MQTT discovery prefix |

### timer

Parameter `sleep_seconds` defines period in seconds between scheduled sensor read attempts.

### device

Section contains list of devices to connect. Parameters:

| parameter        | description                                                     |
|------------------|-----------------------------------------------------------------|
| type             | `LedRgb` or `MiTemp2`                                           |
| MAC              | device address                                                  |
| unique_id        | unique across HA devices identifier                             |
| name             | human-readable device name                                      |
| discovery_period | period in seconds between discovery configs sending, default 600|
| poll_period      | only for MiTemp2, period in seconds between sensor read         |
| read_timeout     | only for MiTemp2, sensor read timeout in seconds                |

Supported types:

| Type      | Bluetooth device name |                              |
|-----------|-----------------------|------------------------------|
| `LedRgb`  | ELK-BLEDOM            | rgb strip bluetooth receiver |
| `MiTemp2` | LYWSD03MMC            | MiTemperature2 sensor        |


## Run

### Using docker-compose

The image in repository is built for `linux/arm/v6` architecture which is suitable for Raspberry Pi 3 devices.
Create directory structure with `docker-compose.yml` from project and your `configuration.yaml`:
```
├── config
│   └── configuration.yaml
└── docker-compose.yml
```
Run `docker-compose up -d` to start and `docker-compose down` to stop.

### From source

Packages needed to run application are listed in the `requirements.txt` .
They can be installed with command:
```
pip install -r requirements.txt
```
After installing dependencies application can be launched:

```
cd /<path-to-sources>/ha-bt-bridge/ha-bt
sudo nohup python ha_bt.py >> ha_bt.log &
```