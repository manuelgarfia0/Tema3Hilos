import threading
import random
import time


NUM_TRABAJADORES = 5
NUM_CICLOS       = 4    # Cuántos pedidos se procesarán en total

print_lock  = threading.Lock()
hay_pedido  = threading.Event()   # se activa cuando llega un nuevo pedido
lock_pedido = threading.Lock()    # protege la "recogida" del pedido

# Contador de pedidos (compartido, protegido por lock_pedido)
pedido_actual   = {"id": 0, "recogido": False}
ciclos_hechos   = {"n": 0}

def log(msg):
    with print_lock:
        print(msg)

class GeneradorPedidos(threading.Thread):
    def run(self):
        for ciclo in range(1, NUM_CICLOS + 1):
            espera = random.uniform(2, 5)
            log(f"\n📦 [Almacén] Nuevo pedido #{ciclo} llegará en {espera:.1f}s...")
            time.sleep(espera)

            with lock_pedido:
                pedido_actual["id"]      = ciclo
                pedido_actual["recogido"] = False

            log(f"📦 [Almacén] ¡PEDIDO #{ciclo} disponible! Trabajadores, a prepararlo.")
            hay_pedido.set()   # señal: hay pedido

            # Esperamos a que todos lo hayan procesado antes de generar el siguiente
            # (el Barrier se encarga de esto desde el lado de los trabajadores)
            time.sleep(0.5)    # pequeño margen antes del siguiente ciclo

        log("\n📦 [Almacén] No habrá más pedidos por hoy. ¡Fin de jornada!")

def fin_de_ronda():
    """Se ejecuta una sola vez cuando todos los trabajadores terminan su pedido."""
    log(f"\n  ✅ Todos los trabajadores han terminado el pedido #{pedido_actual['id']}. "
        f"Esperando el siguiente...\n{'─'*55}")


barrier = threading.Barrier(NUM_TRABAJADORES, action=fin_de_ronda)

class Trabajador(threading.Thread):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        log(f"[{self.nombre}] Listo para trabajar.")

        for _ in range(NUM_CICLOS):
            # 1. Espera hasta que haya un pedido disponible
            log(f"[{self.nombre}] Esperando pedido...")
            hay_pedido.wait()

            # 2. "Recoge" el pedido (sección crítica: solo uno por vez)
            with lock_pedido:
                if not pedido_actual["recogido"]:
                    pedido_actual["recogido"] = True
                    pedido_id = pedido_actual["id"]
                    # Cuando todos han sido notificados del pedido,
                    # apagamos el event para el siguiente ciclo
                    hay_pedido.clear()
                else:
                    pedido_id = pedido_actual["id"]

            log(f"[{self.nombre}] 🔧 Preparando pedido #{pedido_id}...")

            # 3. Prepara el pedido
            tiempo = random.uniform(1, 4)
            time.sleep(tiempo)
            log(f"[{self.nombre}] ✔ Pedido #{pedido_id} listo (tardé {tiempo:.1f}s).")

            # 4. Espera en la Barrier a que todos acaben esta ronda
            try:
                barrier.wait()
            except threading.BrokenBarrierError:
                break

        log(f"[{self.nombre}] Fin de jornada. ¡A casa!")

if __name__ == "__main__":
    print("=== PEDIDOS DE ALMACÉN ===")
    print(f"  {NUM_TRABAJADORES} trabajadores | {NUM_CICLOS} pedidos\n")
    print("─" * 55)

    trabajadores = [Trabajador(f"Trabajador-{i+1}") for i in range(NUM_TRABAJADORES)]
    generador    = GeneradorPedidos(daemon=True)

    generador.start()
    for t in trabajadores:
        t.start()

    generador.join()
    for t in trabajadores:
        t.join()

    print("\n=== Simulación de almacén finalizada ===")