import threading
import random
import time


# Lock que representa al único dependiente de la panadería
dependiente = threading.Lock()


class Cliente(threading.Thread):
    """Cada cliente es un hilo que espera su turno con el dependiente."""

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        print(f"[{self.nombre}] Llega a la panadería y se pone en la cola.")

        # Intentamos adquirir el lock (si está ocupado, el hilo queda bloqueado aquí)
        dependiente.acquire()
        try:
            print(f"[{self.nombre}] *** Está siendo atendido por el dependiente ***")
            tiempo_atencion = random.randint(1, 5)
            time.sleep(tiempo_atencion)
            print(f"[{self.nombre}] Ha sido atendido en {tiempo_atencion}s. ¡Sale de la tienda!")
        finally:
            # Liberamos el lock aunque ocurra una excepción
            dependiente.release()


if __name__ == "__main__":
    print("=== Cola Panadería (1 dependiente) ===\n")

    nombres = ["Ana", "Carlos", "Elena", "David", "Marta",
               "Pedro", "Lucía", "Jorge", "Sara", "Tomás"]

    hilos = [Cliente(nombre) for nombre in nombres]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\n=== Todos los clientes han sido atendidos ===")