import threading
import random
import time


# Semáforos para cada sección
sem_carniceria  = threading.Semaphore(4)
sem_charcuteria = threading.Semaphore(2)


class Cliente(threading.Thread):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def visitar_carniceria(self):
        print(f"[{self.nombre}] Esperando en la cola de Carnicería...")
        sem_carniceria.acquire()
        try:
            print(f"[{self.nombre}] *** Siendo atendido en CARNICERÍA ***")
            tiempo = random.randint(1, 10)
            time.sleep(tiempo)
            print(f"[{self.nombre}] Ha terminado en Carnicería (tardó {tiempo}s).")
        finally:
            sem_carniceria.release()

    def visitar_charcuteria(self):
        print(f"[{self.nombre}] Esperando en la cola de Charcutería...")
        sem_charcuteria.acquire()
        try:
            print(f"[{self.nombre}] *** Siendo atendido en CHARCUTERÍA ***")
            tiempo = random.randint(1, 10)
            time.sleep(tiempo)
            print(f"[{self.nombre}] Ha terminado en Charcutería (tardó {tiempo}s).")
        finally:
            sem_charcuteria.release()

    def run(self):
        # Orden aleatorio: el cliente decide si va antes a carnicería o a charcutería
        if random.choice([True, False]):
            self.visitar_carniceria()
            self.visitar_charcuteria()
        else:
            self.visitar_charcuteria()
            self.visitar_carniceria()

        print(f"[{self.nombre}] ✔ Completamente servido. Abandona la tienda.")


if __name__ == "__main__":
    print("=== Carnicería (4) y Charcutería (2) ===\n")

    nombres = [f"Cliente-{i+1}" for i in range(10)]
    hilos = [Cliente(nombre) for nombre in nombres]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\n=== Todos los clientes han sido completamente atendidos ===")