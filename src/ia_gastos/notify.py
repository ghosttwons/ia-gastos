from datetime import date, timedelta
from .db import connect

def upcoming(days_ahead: int = 30):
    today = date.today()
    horizon = today + timedelta(days=days_ahead)
    results = []
    with connect() as con:
        cur = con.execute("SELECT id, name, amount, due_day, category, notify_days_before FROM bills")
        for _id, name, amount, due_day, category, notify in cur.fetchall():
            # calcular próxima fecha de vencimiento
            y, m = today.year, today.month
            due = date(y, m, min(due_day, 28))  # simple: asegura día válido
            if due < today:
                # pasa al siguiente mes
                if m == 12:
                    y, m = y + 1, 1
                else:
                    m += 1
                due = date(y, m, min(due_day, 28))
            notify_date = due - timedelta(days=notify or 0)
            if today <= due <= horizon:
                results.append({
                    "id": _id, "name": name, "amount": amount, "due_date": due.isoformat(),
                    "category": category, "notify_date": notify_date.isoformat()
                })
    return sorted(results, key=lambda r: r["due_date"])
