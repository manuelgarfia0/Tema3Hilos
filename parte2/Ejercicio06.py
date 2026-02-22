"""
PREGUNTAS:
1. ¿Se produce interbloqueo?
   No, gracias a la asimetría: los filósofos 0-3 cogen primero el palillo
   izquierdo y luego el derecho; el filósofo 4 lo hace al revés. Esto
   garantiza que nunca se forma el ciclo de espera completo necesario para
   el interbloqueo.

2. ¿Podría un filósofo no comer nunca (inanición)?
   Sí es teóricamente posible. Si los vecinos de un filósofo siempre
   consiguen los palillos antes que él (escenario de mala suerte continua),
   ese filósofo podría esperar indefinidamente. En Python, threading.Lock()
   no garantiza orden FIFO de adquisición, por lo que la inanición no es
   imposible aunque sea muy improbable en la práctica.
"""

import threading
import random
import time


NUM_FILOSOFOS = 5

# Cada palillo es un Lock. palillos[i] está entre el filósofo i (izq) e i+1 (der).
palillos = [threading.Lock() for _ in range(NUM_FILOSOFOS)]

NOMBRES = ["Platón", "Aristóteles", "Sócrates", "Descartes", "Kant"]


class Filosofo(threading.Thread):
    def __init__(self, indice, ciclos=5):
        super().__init__()
        self.indice  = indice
        self.nombre  = NOMBRES[indice]
        self.ciclos  = ciclos
        self.izq     = indice
        self.der     = (indice + 1) % NUM_FILOSOFOS

    def pensar(self):
        tiempo = random.uniform(0.5, 2.0)
        print(f"[{self.nombre}] Está pensando... ({tiempo:.1f}s)")
        time.sleep(tiempo)

    def comer(self):
        tiempo = random.uniform(0.5, 2.0)
        print(f"[{self.nombre}] *** Come con palillos {self.izq} y {self.der} ({tiempo:.1f}s) ***")
        time.sleep(tiempo)

    def run(self):
        for ciclo in range(self.ciclos):
            self.pensar()

            # Solución asimétrica: el último filósofo coge los palillos al revés
            if self.indice == NUM_FILOSOFOS - 1:
                primero, segundo = self.der, self.izq
            else:
                primero, segundo = self.izq, self.der

            palillos[primero].acquire()
            print(f"[{self.nombre}] Coge palillo {primero}.")
            palillos[segundo].acquire()
            print(f"[{self.nombre}] Coge palillo {segundo}.")

            self.comer()

            palillos[segundo].release()
            palillos[primero].release()
            print(f"[{self.nombre}] Deja los palillos {primero} y {segundo}.")

        print(f"[{self.nombre}] ✔ Ha terminado de comer (tras {self.ciclos} ciclos).")


if __name__ == "__main__":
    print("=== Problema de los Filósofos ===\n")

    filosofos = [Filosofo(i, ciclos=5) for i in range(NUM_FILOSOFOS)]

    for f in filosofos:
        f.start()

    for f in filosofos:
        f.join()

    print("\n=== Todos los filósofos han terminado ===")