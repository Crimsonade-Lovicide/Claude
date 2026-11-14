#!/usr/bin/env python3
"""Keep you updated on an FAA ground stop and alert the moment it lifts.

Two independent sources, checked every minute:

1. News headlines (Google News RSS, last 24 h). A *nationwide* ground stop is
   announced by the FAA on X/press briefings and is NOT listed airport-by-airport
   in the FAA status feed, so headlines are the fastest reliable public signal
   that it has been lifted. New headlines are printed as status updates; ones
   that say the stop was lifted / flights resumed trigger an urgent alert.
2. The FAA National Airspace System status feed (https://nasstatus.faa.gov):
   per-airport ground stops. Alerts when any start, change or clear.

No API keys. A headline-based alert means "go confirm now", not an official
FAA notice; the alert includes the link so you can check it in one tap.

Usage:
    python3 faa_ground_stop_watch.py                 # news + FAA feed every 60 s
    python3 faa_ground_stop_watch.py --airports JFK LAX ORD
    python3 faa_ground_stop_watch.py --ntfy my-secret-topic   # also push to your phone
    python3 faa_ground_stop_watch.py --once          # print status once and exit

Standard library only. Python 3.8+.
"""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import re
import urllib.parse
import platform
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass

FEED_URL = "https://nasstatus.faa.gov/api/airport-status-information"
NAS_PAGE = "https://nasstatus.faa.gov"
USER_AGENT = "faa-ground-stop-watch/1.0"


@dataclass(frozen=True)
class Stop:
    airport: str
    kind: str  # "ground stop" or "departure stop"
    reason: str
    until: str = ""

    def describe(self) -> str:
        until = f" until {self.until}" if self.until else ""
        return f"{self.airport}: {self.kind} ({self.reason}){until}"


@dataclass
class Snapshot:
    updated: str
    stops: list[Stop]
    delay_programs: list[str]


class FeedError(Exception):
    """Raised when the feed can't be fetched or doesn't look like the FAA feed."""


# ------------------------------------------------------------------ news feed

NEWS_QUERY = 'FAA "ground stop"'
LIFT_RE = re.compile(
    r"\b(lift(s|ed|ing)?|resum\w*|reopen\w*|restart\w*|end(s|ed)\b|is over\b|"
    r"back in the air|cleared to (depart|fly|take off)|takeoffs? (resume|restart))",
    re.I,
)
# Headlines that mention lifting only to say it has NOT happened.
NOT_YET_RE = re.compile(
    r"\b(no timeline|not yet|remains?|still|extend\w*|when will|until further|won'?t|could|may)\b",
    re.I,
)


@dataclass(frozen=True)
class Headline:
    title: str
    link: str
    published: dt.datetime

    @property
    def says_lifted(self) -> bool:
        return bool(LIFT_RE.search(self.title)) and not NOT_YET_RE.search(self.title)


def fetch_headlines(query: str = NEWS_QUERY, timeout: float = 20) -> list[Headline]:
    url = ("https://news.google.com/rss/search?" +
           urllib.parse.urlencode({"q": f"{query} when:1d", "hl": "en-US", "gl": "US", "ceid": "US:en"}))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(3):  # Google News returns occasional transient 503s
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                root = ET.fromstring(resp.read())
            break
        except (urllib.error.URLError, TimeoutError, OSError, ET.ParseError) as exc:
            if attempt == 2:
                raise FeedError(f"could not read news feed: {exc}") from exc
            time.sleep(3 * (attempt + 1))

    items = []
    for it in root.iter("item"):
        try:
            when = email.utils.parsedate_to_datetime(it.findtext("pubDate") or "")
        except (TypeError, ValueError):
            when = dt.datetime.now(dt.timezone.utc)
        items.append(Headline((it.findtext("title") or "").strip(), (it.findtext("link") or "").strip(), when))
    items.sort(key=lambda h: h.published)
    return items


def fmt_time(t: dt.datetime) -> str:
    return t.astimezone().strftime("%a %H:%M")


# ---------------------------------------------------------------- feed parsing

def fetch_feed(timeout: float = 20) -> bytes:
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise FeedError(f"could not reach FAA feed: {exc}") from exc


def _text(el: ET.Element, tag: str) -> str:
    found = el.find(tag)
    return (found.text or "").strip() if found is not None else ""


def parse_feed(raw: bytes) -> Snapshot:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise FeedError(f"feed was not valid XML: {exc}") from exc

    # An empty or unexpected document must never be read as "all clear".
    if root.tag != "AIRPORT_STATUS_INFORMATION" or root.find("Update_Time") is None:
        raise FeedError("feed did not look like the FAA airport status document")

    stops: list[Stop] = []
    delay_programs: list[str] = []

    for delay_type in root.iter("Delay_type"):
        name = _text(delay_type, "Name").lower()

        if "ground stop" in name:
            for prog in delay_type.iter("Program"):
                stops.append(Stop(
                    airport=_text(prog, "ARPT"),
                    kind="ground stop",
                    reason=_text(prog, "Reason") or "unspecified",
                    until=_text(prog, "End_Time"),
                ))

        elif "ground delay" in name:
            for gd in delay_type.iter("Ground_Delay"):
                delay_programs.append(
                    f"{_text(gd, 'ARPT')} ground delay, avg {_text(gd, 'Avg')} ({_text(gd, 'Reason')})"
                )

        # Departure delays tagged "STOP" are local stops (e.g. "TM Initiatives:STOP:EQ").
        elif "arrival/departure" in name:
            for d in delay_type.iter("Delay"):
                reason = _text(d, "Reason")
                if "STOP" in reason.upper():
                    stops.append(Stop(
                        airport=_text(d, "ARPT"),
                        kind="departure stop",
                        reason=reason,
                    ))

    return Snapshot(updated=_text(root, "Update_Time"), stops=stops, delay_programs=delay_programs)


# --------------------------------------------------------------- notifications

def desktop_notify(title: str, message: str) -> None:
    """Best-effort desktop popup; silently skipped where unsupported."""
    system = platform.system()
    try:
        if system == "Darwin":
            script = f'display notification {message!r} with title {title!r} sound name "Glass"'
            subprocess.run(["osascript", "-e", script.replace("'", '"')], check=False, timeout=10)
        elif system == "Linux" and shutil.which("notify-send"):
            subprocess.run(["notify-send", "-u", "critical", title, message], check=False, timeout=10)
        elif system == "Windows":
            ps = (
                "[void][System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms');"
                "$n=New-Object System.Windows.Forms.NotifyIcon;"
                "$n.Icon=[System.Drawing.SystemIcons]::Information;$n.Visible=$true;"
                f"$n.ShowBalloonTip(15000,'{title.replace(chr(39), '')}','{message.replace(chr(39), '')}',"
                "[System.Windows.Forms.ToolTipIcon]::Info);Start-Sleep 16"
            )
            subprocess.Popen(["powershell", "-NoProfile", "-Command", ps])
    except (OSError, subprocess.SubprocessError):
        pass


def ntfy_notify(topic: str, title: str, message: str, urgent: bool, link: str = NAS_PAGE) -> None:
    """Push to the free ntfy app (iOS/Android) via ntfy.sh. Errors are reported, not fatal."""
    req = urllib.request.Request(
        f"https://ntfy.sh/{topic}",
        data=message.encode("utf-8"),
        headers={
            "Title": title.encode("ascii", "ignore").decode(),
            "Priority": "urgent" if urgent else "default",
            "Tags": "airplane",
            "Click": link,
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=15).close()
    except (urllib.error.URLError, OSError) as exc:
        log(f"warning: phone push failed: {exc}")


def alert(args: argparse.Namespace, title: str, message: str, urgent: bool, link: str = NAS_PAGE) -> None:
    banner = "!" * 70
    print(f"\n{banner}\n{title}\n{message}\n{banner}\n", flush=True)
    if not args.quiet:
        sys.stdout.write("\a" * (3 if urgent else 1))
        sys.stdout.flush()
    desktop_notify(title, message)
    if args.ntfy:
        ntfy_notify(args.ntfy, title, message, urgent, link)


# ------------------------------------------------------------------- main loop

def log(msg: str) -> None:
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{stamp}] {msg}", flush=True)


def filter_stops(stops: list[Stop], airports: set[str]) -> list[Stop]:
    if not airports:
        return stops
    return [s for s in stops if s.airport.upper() in airports]


def summarize(snap: Snapshot, stops: list[Stop], nationwide_threshold: int) -> str:
    if not stops:
        return (f"no airport-level ground stops listed (updated {snap.updated}). "
                "This feed does not itemise a nationwide stop; rely on the news line for that.")
    scale = " -- NATIONWIDE SCALE" if len(stops) >= nationwide_threshold else ""
    lines = [f"{len(stops)} active stop(s){scale} (FAA feed updated {snap.updated}):"]
    lines += [f"  - {s.describe()}" for s in sorted(stops, key=lambda s: s.airport)]
    return "\n".join(lines)


def check_news(args, seen: set[str], first: bool) -> bool:
    """Print new headlines; alert on ones saying the stop lifted. Returns True if a lift was reported."""
    try:
        headlines = fetch_headlines(args.news_query)
    except FeedError as exc:
        log(f"warning: {exc}")
        return False

    fresh = [h for h in headlines if h.link not in seen]
    seen.update(h.link for h in fresh)
    if not fresh:
        return False

    if first:
        latest = headlines[-args.show:] if args.show else []
        log(f"Latest news ({len(headlines)} headlines in the last 24 h):")
        for h in latest:
            mark = "  [LIFTED?]" if h.says_lifted else ""
            print(f"    {fmt_time(h.published)}  {h.title}{mark}")
    else:
        log("News update:")
        for h in fresh:
            print(f"    {fmt_time(h.published)}  {h.title}")

    # At start-up only the newest few headlines count, so an old story can't trigger a false alarm.
    candidates = headlines[-5:] if first else fresh
    lifts = [h for h in candidates if h.says_lifted]
    if lifts:
        h = lifts[-1]
        alert(args, "GROUND STOP LIFTED? (news)",
              f"{h.title}\n{h.link}\nConfirm with the FAA ({NAS_PAGE}) or your airline.", urgent=True,
              link=h.link)
        return True
    return False


def check_faa(args, airports: set[str], previous: set[Stop] | None, scope: str):
    """Report the FAA airport feed. Returns the new set of stops (or previous on error)."""
    try:
        snap = parse_feed(fetch_feed())
    except FeedError as exc:
        log(f"warning: {exc}; FAA status unknown, NOT assuming lifted.")
        return previous

    stops = filter_stops(snap.stops, airports)
    current = set(stops)
    if previous is None or current != previous:
        log("FAA status feed: " + summarize(snap, stops, args.nationwide_threshold))
        if args.verbose:
            for gd in snap.delay_programs:
                print(f"    (delay program) {gd}")
    if previous is not None:
        for s in sorted(current - previous, key=lambda s: s.airport):
            alert(args, f"New ground stop: {s.airport}", s.describe(), urgent=False)
        for s in sorted(previous - current, key=lambda s: s.airport):
            alert(args, f"Ground stop cleared: {s.airport}",
                  f"{s.describe()} is no longer listed by the FAA. {len(current)} stop(s) remain.",
                  urgent=not current)
    return current


def run(args: argparse.Namespace) -> int:
    airports = {a.upper() for a in args.airports}
    scope = ", ".join(sorted(airports)) if airports else "all US airports"
    log(f"Watching the FAA ground stop ({scope}); checking every {args.interval}s. Ctrl+C to stop.")
    log("Note: a nationwide stop is not itemised in the FAA airport feed; news headlines are the "
        "main signal for when it lifts.")

    seen: set[str] = set()
    previous: set[Stop] | None = None
    first = True
    last_heartbeat = time.monotonic()

    while True:
        lifted = check_news(args, seen, first)
        previous = check_faa(args, airports, previous, scope)
        first = False

        if args.once:
            return 0
        if lifted and args.exit_on_lift:
            return 0
        if time.monotonic() - last_heartbeat >= args.heartbeat * 60:
            log("Still watching; no lift reported yet.")
            last_heartbeat = time.monotonic()
        time.sleep(args.interval)


def main() -> int:
    p = argparse.ArgumentParser(description="Alert when the FAA ground stop lifts.")
    p.add_argument("--airports", nargs="*", default=[], metavar="CODE",
                   help="only watch these airports, 3-letter FAA codes (default: all)")
    p.add_argument("--interval", type=int, default=60,
                   help="seconds between checks (default 60; the FAA feed updates every few minutes)")
    p.add_argument("--ntfy", metavar="TOPIC",
                   help="also push alerts to your phone via the free ntfy app; pick a hard-to-guess topic")
    p.add_argument("--nationwide-threshold", type=int, default=10,
                   help="label it nationwide when at least this many airports are stopped (default 10)")
    p.add_argument("--news-query", default=NEWS_QUERY, help=f"headline search (default: {NEWS_QUERY})")
    p.add_argument("--show", type=int, default=8, help="headlines to show at start (default 8)")
    p.add_argument("--heartbeat", type=int, default=15,
                   help="minutes between 'still watching' lines when nothing changes (default 15)")
    p.add_argument("--exit-on-lift", action="store_true", help="exit after the all-clear alert")
    p.add_argument("--once", action="store_true",
                   help="print current status once and exit")
    p.add_argument("--quiet", action="store_true", help="no terminal bell")
    p.add_argument("--verbose", action="store_true", help="also list ground delay programs")
    args = p.parse_args()
    args.interval = max(args.interval, 15)  # be polite to the FAA server
    try:
        return run(args)
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
