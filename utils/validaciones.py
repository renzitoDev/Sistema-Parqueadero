# utils/validaciones.py
import re

def placa_valida(placa: str, tipo: str) -> bool:
    """Valida el formato legal colombiano de placas."""
    if " " in placa or len(placa) != 6:
        return False
    if tipo == "Carro":
        return bool(re.fullmatch(r"[A-Z]{3}[0-9]{3}", placa))
    elif tipo == "Moto":
        return bool(re.fullmatch(r"[A-Z]{3}[0-9]{2}[A-Z]", placa))
    return False

def hora_valida(hora: str) -> bool:
    """Valida una hora en formato HH:MM y rango válido."""
    if ":" not in hora:
        return False
    try:
        h, m = hora.split(":")
        h = int(h)
        m = int(m)
        return 0 <= h <= 23 and 0 <= m <= 59
    except Exception:
        return False
