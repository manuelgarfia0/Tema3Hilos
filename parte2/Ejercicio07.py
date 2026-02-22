"""
PREGUNTA: ¿Cambiaría mucho la solución si el máximo son 5 elementos?
  No cambia el código, solo el parámetro maxsize.
  Con maxsize=1 el productor y el consumidor se alternan estrictamente:
    produce → consume → produce → consume ...
  Con maxsize=5 el productor puede adelantarse hasta 5 elementos antes de
  que el consumidor tenga que haberlos procesado, permitiendo que ambos
  trabajen de forma más independiente y la cola actúe como "buffer".
  El comportamiento es el mismo en cuanto a corrección; la diferencia es
  el grado de paralelismo real que se consigue.
"""

import threading
import queue
import random
import time

MAX_COLA      = 1   # ← Prueba también con 5
TOTAL_ITEMS   = 10  # Cuántos ítems produce cada productor


def productor(cola: queue.Queue, nombre: str):
    for i in range(TOTAL_ITEMS):
        dato = random.randint(1, 100)
        print(f"[{nombre}] Quiere producir el dato {dato}  "
              f"(cola: {cola.qsize()}/{cola.maxsize})")
        cola.put(dato)          # Bloquea si la cola está llena
        print(f"[{nombre}] ✔ Produjo {dato}  (cola: {cola.qsize()}/{cola.maxsize})")
        time.sleep(random.uniform(0.1, 0.5))

    # Señal de fin: introduce un centinela por cada consumidor
    cola.put(None)
    print(f"[{nombre}] Ha terminado de producir.")


def consumidor(cola: queue.Queue, nombre: str):
    while True:
        print(f"[{nombre}] Esperando dato...  (cola: {cola.qsize()}/{cola.maxsize})")
        dato = cola.get()       # Bloquea si la cola está vacía
        if dato is None:        # Centinela de fin
            cola.task_done()
            print(f"[{nombre}] Ha terminado de consumir.")
            break
        print(f"[{nombre}] ✔ Consumió {dato}  (cola: {cola.qsize()}/{cola.maxsize})")
        time.sleep(random.uniform(0.2, 0.8))
        cola.task_done()


if __name__ == "__main__":
    print(f"=== Productor-Consumidor (maxsize={MAX_COLA}) ===\n")

    cola = queue.Queue(maxsize=MAX_COLA)

    # 1 productor, 1 consumidor
    t_prod = threading.Thread(target=productor, args=(cola, "Productor-1"), daemon=True)
    t_cons = threading.Thread(target=consumidor, args=(cola, "Consumidor-1"), daemon=True)

    t_prod.start()
    t_cons.start()

    t_prod.join()
    t_cons.join()

    print("\n=== Fin del programa Productor-Consumidor ===")

    # ──────────────────────────────────────────────
    # VARIANTE CON maxsize=5
    # ──────────────────────────────────────────────
    print(f"\n\n=== Variante con maxsize=5 ===\n")

    cola5 = queue.Queue(maxsize=5)

    t_prod5 = threading.Thread(target=productor, args=(cola5, "Productor-1"), daemon=True)
    t_cons5 = threading.Thread(target=consumidor, args=(cola5, "Consumidor-1"), daemon=True)

    t_prod5.start()
    t_cons5.start()

    t_prod5.join()
    t_cons5.join()

    print("\n=== Fin de la variante con maxsize=5 ===")
    print("""
CONCLUSIÓN:
  maxsize=1 → alternancia estricta produce/consume.
  maxsize=5 → el productor puede "adelantarse" hasta 5 ítems,
              el consumidor tiene datos esperando y trabaja sin parar.
  El código es idéntico; solo cambia el parámetro maxsize.
""")