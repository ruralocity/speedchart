# SpeedChart

Chart your network speed, as reported by speedtest-cli. Someday, anyway--for now, get your network speed reports gathered into a single JSON file.

Inspired by [speedtest-cron](https://github.com/vwillcox/speedtest-cron). Written in Python to play as nicely as possible with Raspberry Pi, and also for me to get more practice with the language and its ecosystem (I normally write Ruby).

## Usage

The parser is the only part that's working so far:

- Gather some network speed data using speedtest-cron.
- Copy or move your `*.speedtest.txt` files from speedtest-cron into the `data` directory.
- Run `python parser.py > speedtest.json` to save the output to the file `speedtest.json`.

## TODO

Probably more than this, but to start:

- Wrap in a simple (Flask?) web app to display the results in a chart, probably using Chart.js (hence the creative name, SpeedChart)
- Add test coverage
- Refactor the parser (this is a hack so far)
