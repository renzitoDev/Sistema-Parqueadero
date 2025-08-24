# main.py
from config import CONFIG
from core.parqueadero import Parqueadero

def main():
    parqueadero = Parqueadero(CONFIG)
    while True:
        print("\n== MENÚ ==")
        print("1. Registrar entrada")
        print("2. Registrar salida")
        print("3. Ver estacionados")
        print("4. Informe")
        print("5. Reiniciar sistema")
        print("6. Salir")
        op = input("Elige una opción: ")
        if op == "1":
            parqueadero.registrar_entrada()
        elif op == "2":
            parqueadero.registrar_salida()
        elif op == "3":
            parqueadero.ver_estacionados()
        elif op == "4":
            parqueadero.informe()
        elif op == "5":
            parqueadero.reiniciar()
        elif op == "6":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
