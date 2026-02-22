import threading
import random
import time


# Semáforo con capacidad 4 (= número de empleados de la carnicería)
empleados_carniceria = threading.Semaphore(4)


class ClienteCarniceria(threading.Thread):
    """Cada cliente es un hilo que espera un hueco libre en la carnicería."""

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        print(f"[{self.nombre}] Llega a la carnicería y espera turno.")

        # acquire() decrementa el semáforo; si vale 0, el hilo espera
        empleados_carniceria.acquire()
        try:
            print(f"[{self.nombre}] El cliente {self.nombre} está siendo atendido.")
            tiempo = random.randint(1, 10)
            time.sleep(tiempo)
            print(f"[{self.nombre}] El cliente {self.nombre} ha terminado en la carnicería "
                  f"(tardó {tiempo}s).")
        finally:
            # release() incrementa el semáforo, liberando un hueco
            empleados_carniceria.release()


if __name__ == "__main__":
    print("=== Cola Carnicería (4 empleados) ===\n")

    nombres = [f"Cliente-{i+1}" for i in range(10)]
    hilos = [ClienteCarniceria(nombre) for nombre in nombres]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\n=== Todos los clientes han sido atendidos en carnicería ===")