# modelos/factura.py
from datetime import datetime
from modelos.vehiculo import Vehiculo

class Factura:
    """
    Guarda los datos de facturación de la estadía de un vehículo.
    """
    def __init__(self, vehiculo: Vehiculo, dt_salida: datetime, detalle, cobro_total: int):
        self.placa = vehiculo.placa
        self.tipo = vehiculo.tipo
        self.dt_entrada = vehiculo.dt_entrada
        self.dt_salida = dt_salida
        self.detalle = detalle        # Lista de tuplas (fecha, horas, modalidad, valor)
        self.total = cobro_total
