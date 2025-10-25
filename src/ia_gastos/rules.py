from typing import Optional

KEYWORDS = {
    "Comida": ["super", "supermercado", "panader", "rest", "soda", "pizza", "comida"],
    "Transporte": ["bus", "uber", "taxi", "gas", "combustible", "peaje"],
    "Servicios": ["agua", "luz", "electricidad", "internet", "tel", "claro", "kolbi", "ice"],
    "Renta": ["renta", "alquiler"],
    "Salud": ["farmacia", "clinica", "hospital", "consulta"],
    "Ocio": ["cine", "netflix", "spotify", "bar", "fiesta"],
}

def categorize(description: str) -> Optional[str]:
    desc = description.lower()
    for cat, kws in KEYWORDS.items():
        if any(kw in desc for kw in kws):
            return cat
    return None
