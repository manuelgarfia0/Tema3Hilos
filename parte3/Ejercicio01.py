import threading
import random
import time


NUM_CORREDORES = 10

# Lock para imprimir sin mezclar mensajes
print_lock = threading.Lock()

def log(msg):
    with print_lock:
        print(msg)


def cuenta_atras():
    """Se ejecuta UNA sola vez por el Barrier justo antes de liberar a todos."""
    for n in range(3, 0, -1):
        log(f"  ... {n} ...")
        time.sleep(1)
    log("  ¡BANG! 🔫\n")


# Barrier con action: cuando todos lleguen, hace la cuenta atrás y libera
barrier_salida = threading.Barrier(NUM_CORREDORES, action=cuenta_atras)


class Corredor(threading.Thread):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        # Llegada a la línea de salida (tiempo variable simulando que no llegan a la vez)
        time.sleep(random.uniform(0, 2))
        log(f"[{self.nombre}] Está en la línea de salida. Esperando al resto...")

        # Espera en la barrera hasta que todos estén listos
        barrier_salida.wait()

        # ─── CARRERA ───
        inicio = time.time()
        distancia_carrera = random.uniform(5, 15)   # segundos que tarda en completar
        log(f"[{self.nombre}] ¡Corre! (tardará ~{distancia_carrera:.1f}s)")
        time.sleep(distancia_carrera)
        fin = time.time()

        log(f"[{self.nombre}] 🏁 Ha terminado en {fin - inicio:.2f} segundos.")


if __name__ == "__main__":
    print("=== SIMULACIÓN DE CARRERA ===\n")

    nombres = [
        "Usain", "Florence", "Mo", "Eliud", "Cathy",
        "Carl", "Allyson", "Wayde", "Shelly", "David"
    ]

    corredores = [Corredor(nombre) for nombre in nombres]

    inicio_global = time.time()
    for c in corredores:
        c.start()
    for c in corredores:
        c.join()
    fin_global = time.time()

    print(f"\n=== Carrera finalizada. Tiempo total: {fin_global - inicio_global:.2f}s ===")