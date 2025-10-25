# ia-gastos

Una **IA de bajo alcance** (ligera y local) para:

- Llevar *track* de gastos mensuales (SQLite).
- Recordar **pagos de servicios** con alertas y exportación a **calendario (.ics)**.
- Sugerir **equilibrio económico**: presupuestos por categoría, alertas de sobre‑gasto y tips.

## Características
- 100% **local**: sin nube, sin claves.
- CLI simple (`ia-gastos`) para agregar gastos, registrar servicios y ver reportes.
- Clasificación automática de categoría vía reglas + modelo NB ligero (opcional).
- Exporta eventos .ics para vencimientos (importable en Google/Apple Calendar/Outlook).
- Reporte mensual en CSV.

## Instalación rápida
```bash
python -m venv .venv && source .venv/bin/activate  # en macOS/Linux
pip install -e .
```

## Uso rápido
```bash
# Inicia la base local
ia-gastos init

# Agrega un gasto
ia-gastos add-expense --date 2025-10-25 --desc "Supermercado MaxiPalí" --amount 21500 --method tarjeta

# Registra un servicio con recordatorio
ia-gastos add-bill --name "Electricidad" --amount 32000 --due-day 10 --category "Servicios" --notify 7

# Lista próximos vencimientos
ia-gastos upcoming

# Establece presupuesto mensual por categoría
ia-gastos set-budget --category "Comida" --amount 150000

# Reporte del mes actual
ia-gastos report --month 2025-10

# Exporta recordatorios a .ics
ia-gastos export-ics --month 2025-11 --out vencimientos_nov.ics
```

## Categorías sugeridas
`Comida`, `Transporte`, `Servicios`, `Renta`, `Salud`, `Educación`, `Ocio`, `Otros`.

## Notificaciones
Puedes usar `cron` en macOS:
```
0 9 * * * /ruta/a/.venv/bin/ia-gastos upcoming --notify >> ~/.ia-gastos.log 2>&1
```

## Licencia
MIT
