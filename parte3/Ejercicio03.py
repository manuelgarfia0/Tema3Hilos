import threading
import random
import time


DURACION_SIMULACION = 40   # segundos totales de simulación
TIEMPO_VERDE        = 6    # segundos en verde
TIEMPO_ROJO         = 8    # segundos en rojo
NUM_PEATONES        = 8

print_lock     = threading.Lock()
semaforo_verde = threading.Event()   # no seteado → rojo; seteado → verde
parar          = threading.Event()   # señal para terminar la simulación

def log(msg):
    with print_lock:
        print(msg)
        
class Semaforo(threading.Thread):
    def run(self):
        ciclo = 0
        while not parar.is_set():
            ciclo += 1
            # ── ROJO ──
            semaforo_verde.clear()
            log(f"\n🔴 [Semáforo] Ciclo {ciclo}: ROJO durante {TIEMPO_ROJO}s")
            parar.wait(timeout=TIEMPO_ROJO)   # espera interrumpible
            if parar.is_set():
                break

            # ── VERDE ──
            log(f"🟢 [Semáforo] Ciclo {ciclo}: VERDE durante {TIEMPO_VERDE}s")
            semaforo_verde.set()
            parar.wait(timeout=TIEMPO_VERDE)

        semaforo_verde.set()   # liberamos a cualquier peatón que quede bloqueado
        log("[Semáforo] Se apaga.")

class Peaton(threading.Thread):
    def __init__(self, nombre):
        super().__init__(daemon=True)
        self.nombre = nombre

    def run(self):
        while not parar.is_set():
            # Simula que el peatón llega en un momento aleatorio
            tiempo_llegada = random.uniform(0.5, 3)
            time.sleep(tiempo_llegada)

            if parar.is_set():
                break

            log(f"[{self.nombre}] Llega al paso de cebra y espera...")

            # Espera a que el semáforo esté en verde
            semaforo_verde.wait()

            if parar.is_set():
                break

            log(f"[{self.nombre}] 🚶 ¡Cruza la calle!")
            time.sleep(random.uniform(1, 3))   # tiempo en cruzar
            log(f"[{self.nombre}] Ha cruzado. Va a su destino y vuelve...")

if __name__ == "__main__":
    print("=== SIMULADOR DE PASO DE PEATONES ===\n")

    nombres = [f"Peatón-{i+1}" for i in range(NUM_PEATONES)]
    peatones = [Peaton(nombre) for nombre in nombres]
    semaforo = Semaforo(daemon=True)

    semaforo.start()
    for p in peatones:
        p.start()

    time.sleep(DURACION_SIMULACION)
    parar.set()
    semaforo_verde.set()   # desbloquea peatones que queden en wait()

    semaforo.join()
    log("\n=== Simulación finalizada ===")