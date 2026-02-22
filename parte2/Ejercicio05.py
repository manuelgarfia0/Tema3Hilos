import threading
import random
import time


NUM_LIBROS = 9
NUM_ESTUDIANTES = 4

# Estado de cada libro: True = disponible
libros_disponibles = [True] * NUM_LIBROS
lock_libros = threading.Lock()          # Protege el array de libros
sem_libros  = threading.Semaphore(NUM_LIBROS)  # Cuenta libros libres


def coger_dos_libros():
    """
    Reserva 2 libros de forma atómica.
    El estudiante espera hasta que haya al menos 2 libros disponibles.
    Devuelve los índices de los 2 libros reservados.
    """
    while True:
        # Adquirimos 2 "fichas" del semáforo (una tras otra)
        sem_libros.acquire()
        sem_libros.acquire()

        with lock_libros:
            libres = [i for i, libre in enumerate(libros_disponibles) if libre]
            if len(libres) >= 2:
                elegidos = random.sample(libres, 2)
                for idx in elegidos:
                    libros_disponibles[idx] = False
                return elegidos
            else:
                # En el improbable caso de que entre acquire y lock otro hilo
                # tome los libros, devolvemos las fichas y reintentamos
                sem_libros.release()
                sem_libros.release()
                time.sleep(0.05)


def devolver_libros(indices):
    """Libera los 2 libros usados por el estudiante."""
    with lock_libros:
        for idx in indices:
            libros_disponibles[idx] = True
    sem_libros.release()
    sem_libros.release()


class Estudiante(threading.Thread):
    def __init__(self, nombre, ciclos=3):
        super().__init__()
        self.nombre = nombre
        self.ciclos = ciclos  # Cuántas veces estudia cada estudiante

    def run(self):
        for _ in range(self.ciclos):
            print(f"[{self.nombre}] Esperando para coger 2 libros...")
            indices = coger_dos_libros()
            nombres_libros = [f"Libro-{i+1}" for i in indices]
            print(f"[{self.nombre}] Cogió: {nombres_libros[0]} y {nombres_libros[1]}. ¡A estudiar!")

            tiempo = random.randint(3, 5)
            time.sleep(tiempo)

            devolver_libros(indices)
            print(f"[{self.nombre}] Devuelve: {nombres_libros[0]} y {nombres_libros[1]} "
                  f"(los tuvo {tiempo}s).")

        print(f"[{self.nombre}] ✔ Ha terminado de estudiar.")


if __name__ == "__main__":
    print("=== Estudiantes y Libros ===")
    print(f"  {NUM_ESTUDIANTES} estudiantes | {NUM_LIBROS} libros | cada uno necesita 2\n")

    nombres = ["Alicia", "Bernardo", "Clara", "Diego"]
    hilos = [Estudiante(nombre, ciclos=3) for nombre in nombres]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\n=== Todos los estudiantes han terminado de estudiar ===")