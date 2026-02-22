import threading
import random
import time


class AdivinaNumero(threading.Thread):
    # Variables de clase compartidas
    numero_oculto = random.randint(0, 100)
    ya_adivinado = False
    ganador = None

    # Lock para proteger la sección crítica (comprobar y actualizar ya_adivinado)
    lock = threading.Lock()

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        intentos = 0

        while True:
            # --- SECCIÓN CRÍTICA ---
            # Adquirimos el lock antes de comprobar y modificar el estado compartido
            with AdivinaNumero.lock:
                # Si otro hilo ya acertó, salimos inmediatamente
                if AdivinaNumero.ya_adivinado:
                    print(f"[{self.nombre}] Otro hilo ya acertó. Termino tras {intentos} intentos.")
                    return

                # Generamos nuestro intento dentro del lock para que,
                # si acertamos, nadie más pueda "robar" el acierto
                intento = random.randint(0, 100)
                intentos += 1

                if intento == AdivinaNumero.numero_oculto:
                    AdivinaNumero.ya_adivinado = True
                    AdivinaNumero.ganador = self.nombre
                    print(f"[{self.nombre}] ¡¡ACERTÉ!! El número era {intento} "
                          f"(intentos de este hilo: {intentos})")
                    return
            # --- FIN SECCIÓN CRÍTICA ---

            # Pequeña pausa fuera del lock para no bloquearlo innecesariamente
            time.sleep(0.01)


if __name__ == "__main__":
    print("=== Número Oculto con Lock ===")
    print(f"[INFO] Número a adivinar: {AdivinaNumero.numero_oculto}  (revelado para verificar)\n")

    hilos = [AdivinaNumero(f"Jugador-{i+1}") for i in range(10)]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print(f"\n¡Ganador: {AdivinaNumero.ganador}!")
    print(f"Número oculto era: {AdivinaNumero.numero_oculto}")