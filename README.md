# Bluetooth devices connection to Home Assistant over MQTT

## Run

Packages needed to run application are listed in the `requirements.txt` .
They can be installed with command:
```
pip install -r requirements.txt
```
After installing dependencies application can be launched:

```
cd /<path-to-sources>/ha-bt-bridge/ha-bt
sudo nohup python run.py >> ha-bt.log &
```

## Configuration

Initial configuration can be created by copying `example.configuration.yml` with name `configuration.yml`.

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

Parameter `sleep_seconds` defines period in seconds between scheduled jobs execution.

### device

Section contains list of devices to connect. Parameters:
| parameter   | description                                            |
|-------------|--------------------------------------------------------|
| type        | `LedRgb` or `MiTemp2`                                  |
| MAC         | device address                                         |
| unique_id   | unique across HA devices identifier                    |
| name        | human-readable device name                             |
| poll_period | only for MiTemp2, period in seconds between sensor read|

Supported types:
| Type      | Bluetooth device name |                              |
|-----------|-----------------------|------------------------------|
| `LedRgb`  | ELK-BLEDOM            | rgb strip bluetooth receiver |
| `MiTemp2` | LYWSD03MMC            | MiTemperature2 sensor        |

