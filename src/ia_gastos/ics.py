from datetime import datetime
from pathlib import Path

ICS_HEADER = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//ia-gastos//ES\n"
ICS_FOOTER = "END:VCALENDAR\n"

def make_event(summary: str, dtstart: str, description: str = ""):
    uid = f"{summary}-{dtstart}"
    return (
        "BEGIN:VEVENT\n"
        f"UID:{uid}\n"
        f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}\n"
        f"DTSTART;VALUE=DATE:{dtstart.replace('-','')}\n"
        f"SUMMARY:{summary}\n"
        f"DESCRIPTION:{description}\n"
        "END:VEVENT\n"
    )

def export_ics(path: str, events: list):
    body = [ICS_HEADER] + events + [ICS_FOOTER]
    Path(path).write_text("".join(body), encoding="utf-8")
    return path
