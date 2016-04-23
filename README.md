# SpeedChart

Chart your network speed, as reported by speedtest-cli.

Inspired by [speedtest-cron](https://github.com/vwillcox/speedtest-cron). Written in Python to play as nicely as possible with Raspberry Pi, and also for me to get more practice with the language and its ecosystem (I normally write Ruby).

## Usage

This will be cleaned up as I understand the Python ecosystem and Flask deployments better. For now, you can run it on your favorite localhost like so:

- Gather some network speed data using speedtest-cron.
- Copy or move your `*.speedtest.txt` files from speedtest-cron into the `data` directory.
- `pip install flask`
- `python speedtest.py`

Visit <http://localhost:5000> in your favorite browser to see a chart of your network speeds.

## TODO

Probably more than this, but to start:

- ~~Wrap in a simple (Flask?) web app to display the results in a chart, probably using Chart.js (hence the creative name, SpeedChart)~~
- Add test coverage
- Refactor the parser (this is a hack so far)
