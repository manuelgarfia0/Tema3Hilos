import threading
import random
import time


NUM_PERSONAS = 5
CODIGO_SECRETO = f"{random.randint(0, 9999):04d}"   # código de 4 cifras

# Estado compartido
codigo_encontrado = False
codigo_correcto   = None
quien_lo_encontro = None

lock_codigo = threading.Lock()
print_lock  = threading.Lock()

def log(msg):
    with print_lock:
        print(msg)


# Barrier para la salida: las 5 personas se reúnen antes de salir
def anuncio_salida():
    log("\n  🔓 ¡Puerta abierta! ¡Todos reunidos! ¡SALID!\n")

barrier_salida = threading.Barrier(NUM_PERSONAS, action=anuncio_salida)


class Persona(threading.Thread):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def intentar_adivinar(self):
        """Genera un código de 4 cifras aleatorio y lo comprueba de forma segura."""
        global codigo_encontrado, codigo_correcto, quien_lo_encontro

        intento = f"{random.randint(0, 9999):04d}"

        with lock_codigo:
            if codigo_encontrado:
                return False   # Otro ya lo encontró; no hace falta intentarlo
            if intento == CODIGO_SECRETO:
                codigo_encontrado   = True
                codigo_correcto     = intento
                quien_lo_encontro   = self.nombre
                log(f"[{self.nombre}] 🎉 ¡HE ENCONTRADO EL CÓDIGO: {intento}! "
                    f"¡Avisad a todos!")
                return True
        return False

    def run(self):
        intentos = 0
        log(f"[{self.nombre}] Empieza a buscar el código...")

        # Sigue intentando mientras nadie haya acertado
        while True:
            with lock_codigo:
                if codigo_encontrado:
                    break
            intentos += 1
            if self.intentar_adivinar():
                break
            time.sleep(random.uniform(0.01, 0.05))   # pausa entre intentos

        if quien_lo_encontro != self.nombre:
            log(f"[{self.nombre}] Me han dicho que {quien_lo_encontro} encontró el código. "
                f"¡Voy a la puerta! (hice {intentos} intentos)")
        else:
            log(f"[{self.nombre}] ¡Fui yo quien lo encontró tras {intentos} intentos!")

        # Esperamos a que los 5 se reúnan antes de salir
        log(f"[{self.nombre}] Esperando a que todos lleguen a la puerta...")
        barrier_salida.wait()
        log(f"[{self.nombre}] ✅ ¡Libre!")


if __name__ == "__main__":
    print("=== ESCAPE ROOM ===")
    print(f"[INFO] Código secreto: {CODIGO_SECRETO}  (revelado para verificar)\n")

    personas = [Persona(f"Persona-{i+1}") for i in range(NUM_PERSONAS)]

    for p in personas:
        p.start()
    for p in personas:
        p.join()

    print("\n=== ¡Todos han escapado! ===")