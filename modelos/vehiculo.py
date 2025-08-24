# modelos/vehiculo.py
from datetime import datetime

class Vehiculo:
    """
    Representa el registro de un vehículo ingresando al parqueadero.
    """
    def __init__(self, placa: str, tipo: str):
        self.placa = placa
        self.tipo = tipo
        self.dt_entrada = datetime.now()  # Guardar fecha/hora reales de ingreso
