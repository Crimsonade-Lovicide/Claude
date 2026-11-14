# FAA ground stop monitor

Keeps you updated on the FAA nationwide ground stop and alerts you the moment
reports say it has lifted. One Python file, no installs, no API keys.

## Run it

```bash
python3 faa_ground_stop_watch.py
```

Every 60 seconds it:

1. **Reads the latest news headlines** about the FAA ground stop (Google News, last 24 h),
   prints new ones as status updates, and fires an **urgent alert** when a headline says
   the stop was lifted or flights resumed.
2. **Reads the FAA's own status feed** (nasstatus.faa.gov) and alerts when any
   airport-level ground stop starts, changes, or clears.

Alerts show up as a big banner in the terminal plus a beep and a desktop
notification (macOS, Windows, or Linux with `notify-send`).

### Get alerts on your phone

1. Install the free **ntfy** app (iOS / Android) and subscribe to a topic name only you
   know, e.g. `faa-watch-k39x7q`.
2. Run:

```bash
python3 faa_ground_stop_watch.py --ntfy faa-watch-k39x7q
```

Anyone who guesses the topic name can read it, so pick something random.

### Useful options

| Option | What it does |
|---|---|
| `--once` | Print the current status and exit |
| `--airports JFK LAX` | Only report airport-level stops at these airports |
| `--interval 30` | Check more often (minimum 15 s) |
| `--exit-on-lift` | Stop after the "lifted" alert |
| `--verbose` | Also list ground delay programs |

## Limits

- **A nationwide stop doesn't appear in the FAA's per-airport feed.** The FAA
  announces it through advisories, posts on X, and press briefings. So the "lifted"
  signal comes from news headlines, which usually appear within minutes of the FAA's
  announcement.
- **Headline matching is a heuristic.** It looks for words like "lifts", "lifted",
  "resume", "ends", and "reopen", and skips headlines with "no timeline", "still", or
  "remains". Treat an alert as "go confirm now": it includes the article link, and you
  can check https://nasstatus.faa.gov or your airline.
- **After the stop lifts, delays continue for hours** while aircraft and crews are
  repositioned.
- **If a feed can't be reached, the script says so** and keeps trying. It never reads
  a failed check as "lifted".
