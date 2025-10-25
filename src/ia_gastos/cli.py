import click
from datetime import date
from .db import connect, ensure_db
from .rules import categorize
from .budget import set_budget as _set_budget, budget_alerts
from .notify import upcoming as _upcoming
from .ics import make_event, export_ics

@click.group()
def main():
    """CLI para ia-gastos (local y simple)."""
    pass

@main.command()
def init():
    ensure_db()
    click.echo("Base creada en ~/.ia_gastos/gastos.db")

@main.command("add-expense")
@click.option("--date", "date_str", required=True, help="YYYY-MM-DD")
@click.option("--desc", required=True, help="Descripción del gasto")
@click.option("--amount", type=float, required=True)
@click.option("--method", default="", help="Efectivo/tarjeta/etc")
@click.option("--category", default="", help="Categoría (si no, se intenta inferir)")
def add_expense(date_str, desc, amount, method, category):
    cat = category or (categorize(desc) or None)
    with connect() as con:
        con.execute(
            "INSERT INTO expenses(date, description, amount, method, category) VALUES(?,?,?,?,?)",
            (date_str, desc, amount, method or None, cat),
        )
        con.commit()
    click.echo(f"✓ Gasto agregado ({cat or 'Sin categoría'})")

@main.command("add-bill")
@click.option("--name", required=True)
@click.option("--amount", type=float, required=True)
@click.option("--due-day", type=int, required=True, help="Día de vencimiento (1-28)")
@click.option("--category", default="Servicios")
@click.option("--notify", type=int, default=0, help="Días antes para notificar")
def add_bill(name, amount, due_day, category, notify):
    with connect() as con:
        con.execute(
            "INSERT INTO bills(name, amount, due_day, category, notify_days_before) VALUES(?,?,?,?,?)",
            (name, amount, due_day, category, notify),
        )
        con.commit()
    click.echo("✓ Servicio registrado")

@main.command("upcoming")
@click.option("--days", type=int, default=30, help="Horizonte en días (default 30)")
@click.option("--notify", is_flag=True, help="Salida breve para notificaciones")
def upcoming(days, notify):
    ups = _upcoming(days_ahead=days)
    if notify:
        for u in ups:
            if u["notify_date"] <= date.today().isoformat():
                click.echo(f"Recordatorio: {u['name']} vence el {u['due_date']} (monto {u['amount']})")
        return
    # salida completa
    for u in ups:
        click.echo(f"- {u['due_date']} | {u['name']} | {u['amount']} | {u.get('category') or '-'} | avisar {u['notify_date']}")

@main.command("set-budget")
@click.option("--month", required=False, help="YYYY-MM (default mes actual)")
@click.option("--category", required=True)
@click.option("--amount", type=float, required=True)
def set_budget(month, category, amount):
    if not month:
        month = date.today().strftime("%Y-%m")
    _set_budget(month, category, amount)
    click.echo(f"✓ Presupuesto {category} para {month}: {amount}")

@main.command("report")
@click.option("--month", required=False, help="YYYY-MM")
def report(month):
    from .budget import monthly_spend_by_category
    if not month:
        month = date.today().strftime("%Y-%m")
    by_cat = monthly_spend_by_category(month)
    click.echo(f"Reporte {month}:\n")
    total = 0.0
    for cat, amt in sorted(by_cat.items()):
        click.echo(f"  {cat:12s}  {amt:10.2f}")
        total += amt
    click.echo(f"\nTotal: {total:.2f}")
    # alertas
    alerts = budget_alerts(month)
    if alerts:
        click.echo("\nAlertas:")
        for cat, s, limit, status in alerts:
            click.echo(f"  {cat}: {s:.2f}/{limit:.2f} ({status})")

@main.command("export-ics")
@click.option("--month", required=False, help="YYYY-MM (default mes actual)")
@click.option("--out", required=True, help="Ruta del archivo .ics a generar")
def export_ics_cmd(month, out):
    if not month:
        month = date.today().strftime("%Y-%m")
    ups = _upcoming(60)
    events = []
    for u in ups:
        # solo eventos del mes pedido
        if u["due_date"].startswith(month):
            summary = f"Vencimiento: {u['name']} ({u['amount']})"
            events.append(make_event(summary, u["due_date"], description=u.get("category") or ""))
    if not events:
        click.echo("No hay vencimientos para el mes indicado.")
        return
    path = export_ics(out, events)
    click.echo(f"✓ Exportado: {path}")
