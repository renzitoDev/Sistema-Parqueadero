# core/parqueadero.py
from datetime import datetime, timedelta
from modelos.vehiculo import Vehiculo
from modelos.factura import Factura
from utils.validaciones import placa_valida, hora_valida

class Parqueadero:
    """
    Maneja vehículos activos, histórico de facturas y lógica de cobro.
    """
    def __init__(self, config):
        self.config = config
        self.vehiculos_activos = []
        self.facturas = []
        self.ingresos = {"Carro": 0, "Moto": 0, "Total": 0}

    def buscar_por_placa(self, placa: str):
        for v in self.vehiculos_activos:
            if v.placa == placa:
                return v
        return None

    def hay_cupo(self):
        return len(self.vehiculos_activos) < self.config["capacidad_maxima"]

    def registrar_entrada(self):
        print("\n🚗 REGISTRO DE ENTRADA")
        if not self.hay_cupo():
            print("Parqueadero lleno.")
            return
        tipo_op = input("Tipo (1=Carro, 2=Moto): ").strip()
        if tipo_op == "1":
            tipo = "Carro"
        elif tipo_op == "2":
            tipo = "Moto"
        else:
            print("Opción inválida.")
            return
        placa = input("Placa: ").upper().strip()
        if not placa_valida(placa, tipo):
            print("Placa inválida. Ej Carro: HTM234   Ej Moto: FF003F")
            return
        if self.buscar_por_placa(placa):
            print("❌ Ya está adentro.")
            return
        vehiculo = Vehiculo(placa, tipo)
        self.vehiculos_activos.append(vehiculo)
        print(f"{tipo} {placa} registrado ({vehiculo.dt_entrada.strftime('%Y-%m-%d %H:%M')})")

    def calcular_detalle_cobro(self, tipo, dt_entrada, dt_salida):
        tarifa_hora = self.config["tarifas"][tipo.lower()]["hora"]
        tarifa_dia = self.config["tarifas"][tipo.lower()]["dia"]
        umbral = self.config["umbral_dia"]
        total, detalle = 0, []
        dt_actual, fin = dt_entrada, dt_salida
        while dt_actual.date() < fin.date():
            dt_fin_dia = dt_actual.replace(hour=23, minute=59)
            minutos = int(((dt_fin_dia - dt_actual).total_seconds() // 60) + 1)
            horas = minutos // 60 + (1 if minutos % 60 > 0 else 0)
            if horas > umbral:
                valor, modalidad = tarifa_dia, "día"
            else:
                valor, modalidad = horas * tarifa_hora, f"{horas}h"
            detalle.append((dt_actual.date(), horas, modalidad, valor))
            total += valor
            dt_actual = (dt_fin_dia + timedelta(minutes=1)).replace(hour=0, minute=0)
        if dt_actual < fin:
            minutos = int((fin - dt_actual).total_seconds() // 60)
            horas = minutos // 60 + (1 if minutos % 60 > 0 else 0)
            if horas > 0:
                if horas > umbral:
                    valor, modalidad = tarifa_dia, "día"
                else:
                    valor, modalidad = horas * tarifa_hora, f"{horas}h"
                detalle.append((dt_actual.date(), horas, modalidad, valor))
                total += valor
        return detalle, total

    def registrar_salida(self):
        print("\n🚪 REGISTRO DE SALIDA")
        if not self.vehiculos_activos:
            print("No hay vehículos dentro.")
            return
        placa = input("Placa: ").upper().strip()
        vehiculo = self.buscar_por_placa(placa)
        if not vehiculo:
            print("❌ No encontrado")
            return
        fecha_salida = input("Fecha de salida (YYYY-MM-DD): ").strip()
        hora_salida = input("Hora de salida (HH:MM): ").strip()
        if not hora_valida(hora_salida):
            print("Hora inválida.")
            return
        try:
            dt_salida = datetime.strptime(f"{fecha_salida} {hora_salida}", "%Y-%m-%d %H:%M")
        except Exception:
            print("Formato fecha u hora inválido.")
            return
        if dt_salida <= vehiculo.dt_entrada:
            print("Salida debe ser posterior a entrada.")
            return
        detalle, total = self.calcular_detalle_cobro(vehiculo.tipo, vehiculo.dt_entrada, dt_salida)
        factura = Factura(vehiculo, dt_salida, detalle, total)
        self.vehiculos_activos.remove(vehiculo)
        self.facturas.append(factura)
        self.ingresos[vehiculo.tipo] += total
        self.ingresos["Total"] += total
        print(f"\nFACTURA para {vehiculo.placa}")
        print(f"Entrada: {vehiculo.dt_entrada.strftime('%Y-%m-%d %H:%M')}")
        print(f"Salida:  {dt_salida.strftime('%Y-%m-%d %H:%M')}")
        for (fecha, horas, modo, valor) in detalle:
            print(f"{fecha}: {modo} → ${valor:,}")
        print(f"TOTAL A PAGAR: ${total:,}")

    def ver_estacionados(self):
        print("\n🅿️ VEHÍCULOS ESTACIONADOS")
        for v in self.vehiculos_activos:
            print(f"{v.placa:<10} {v.tipo:<8} {v.dt_entrada.strftime('%Y-%m-%d %H:%M')}")

    def informe(self):
        print("\n==== INFORME ====")
        print(f" Vehículos dentro: {len(self.vehiculos_activos)}")
        print(f" Ingresos: Carro: ${self.ingresos['Carro']:,} | Moto: ${self.ingresos['Moto']:,} | Total: ${self.ingresos['Total']:,}")
        print(f" Facturas generadas: {len(self.facturas)}")
        if self.facturas:
            print(" Últimas 5 facturas:")
            for f in self.facturas[-5:]:
                print(f" {f.placa} {f.tipo} {f.dt_entrada.strftime('%Y-%m-%d %H:%M')} -> {f.dt_salida.strftime('%Y-%m-%d %H:%M')} Total: ${f.total:,}")

    def reiniciar(self):
        self.vehiculos_activos.clear()
        self.facturas.clear()
        self.ingresos = {"Carro": 0, "Moto": 0, "Total": 0}
        print("Estado reseteado.")
