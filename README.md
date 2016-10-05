# bahnpy

A small tool with which you can see the timetable of the german [railway](https://www.bahn.de/).

**Why bother with a webapp, when you can have the information right at your fingertips!**

---
## Installation

**Notice** bahn.py runs **only** with python 3
```
git clone https://github.com/c0rby/bahnpy
```

After that you have to install the dependencies and create at least an empty configuration file in the config folder.
```
cd bahnpy
pip install -r requirements.txt
cd config
touch config.json
```
---

## Configuration

If you want to set a default route or are behind a proxy you can set that in a Configuration file.  
Just create a file named `config.json` in the config folder and fill in the needed information.
You can also define presets which are route that are not default but are also often used.

The example configuration file looks like this:
```
{
    "default_route": {
        "origin": "Origin",
        "destination": "Destination",
        "departure_time": "TIME"
    },
    "presets": {
        "preset1": {
            "origin": "Origin",
            "destination": "Destination",
            "departure_time": "TIME"
        },
        "preset2": {
            "origin": "Origin",
            "destination": "Destination",
            "departure_time": "TIME"
        }
    },
    "network": {
        "proxy": {
            "http_proxy": "http://foo:8080",
            "https_proxy": "http://foo:8080",
        },
        "ignore_ssl": true
    }
}

```
---
## Usage
```
Usage:   bahn.py [<TIME>]
            bahn.py <ORIGIN> <DESTINATION> [<TIME>]
            bahn.py (--preset <PRESET_NAME>)

Shows the departure, arrival and delay of trains.

Arguments:
  TIME        optional departure time
  START DESTINATION  shows the departure and arrival times from a given START and DESTINATION optional with departure TIME

Options:
  -h --help
  --version
```
---

## Example Usage
The configuration file looks like this:
```JSON
{
    "default_route": {
        "origin": "Berlin Hbf",
        "destination": "Berlin-Tegel (S)",
        "departure_time": "13:37"
    },
    "presets": {
        "work2Home": {
            "origin": "Berlin Ostbahnhof",
            "destination": "Berlin Südkreuz",
            "departure_time": "18:30"
        },
        "homeToHackerspace": {
            "origin": "Berlin Südkreuz",
            "destination": "Berlin Jannowitzbrücke",
            "departure_time": "19:30"
        }
    }
}
```

```
[corby@host:~/Tools/bahnpy]$ ./bahn.py
Origin: Berlin Hbf 13:32 | Destination: Berlin-Tegel (S) 13:57 RE, S
Origin: Berlin Hbf 13:36 | Destination: Berlin-Tegel (S) 14:14 STR, U
Origin: Berlin Hbf 13:46 | Destination: Berlin-Tegel (S) 14:17 RE, S

[corby@host:~/Tools/bahnpy]$ ./bahn.py 15:30
Origin: Berlin Hbf 15:21 | Destination: Berlin-Tegel (S) 15:56 STR, U
Origin: Berlin Hbf 15:26 | Destination: Berlin-Tegel (S) 15:57 S
Origin: Berlin Hbf 15:28 | Destination: Berlin-Tegel (S) 16:05 S, U

[corby@work]:~/Tools/bahnpy$ ./bahn.py --preset work2Home
Origin: Berlin Ostbahnhof 18:20 | Destination: Berlin Südkreuz 18:44 S
Origin: Berlin Ostbahnhof 18:24 | Destination: Berlin Südkreuz 18:45 S
Origin: Berlin Ostbahnhof 18:25 | Destination: Berlin Südkreuz 18:49 S
```
