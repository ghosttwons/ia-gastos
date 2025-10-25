from .db import connect
from collections import defaultdict

def set_budget(month: str, category: str, amount: float):
    with connect() as con:
        con.execute(
            "INSERT INTO budgets(month, category, amount) VALUES(?,?,?)",
            (month, category, amount),
        )
        con.commit()

def get_budgets(month: str):
    with connect() as con:
        cur = con.execute("SELECT category, amount FROM budgets WHERE month=?", (month,))
        return dict(cur.fetchall())

def monthly_spend_by_category(month: str):
    with connect() as con:
        cur = con.execute(
            "SELECT category, COALESCE(SUM(amount),0) FROM expenses WHERE substr(date,1,7)=? GROUP BY category",
            (month,),
        )
        return dict((k or "SinCategoria", v) for k, v in cur.fetchall())

def budget_alerts(month: str):
    budgets = get_budgets(month)
    spent = monthly_spend_by_category(month)
    alerts = []
    for cat, limit in budgets.items():
        s = spent.get(cat, 0.0)
        if s > limit:
            alerts.append((cat, s, limit, "sobrepasado"))
        elif s > 0.8 * limit:
            alerts.append((cat, s, limit, "al 80%"))
    return alerts
