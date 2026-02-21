import threading


class ContadorHilo(threading.Thread):
    """Hilo que incrementa un contador compartido a nivel de clase."""

    # Variable de clase compartida por todos los hilos
    contador = 0

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        while ContadorHilo.contador < 1000:
            ContadorHilo.contador += 1
            # Descomenta la siguiente línea para ver cada incremento (verbose):
            # print(f"[{self.nombre}] Contador = {ContadorHilo.contador}")

        print(f"[{self.nombre}] Ha terminado. Contador = {ContadorHilo.contador}")


if __name__ == "__main__":
    print("\n=== Contador Compartido ===\n")

    class ContadorHiloSeguro(threading.Thread):
        contador = 0
        lock = threading.Lock()  # Lock compartido a nivel de clase

        def __init__(self, nombre):
            super().__init__()
            self.nombre = nombre

        def run(self):
            while True:
                with ContadorHiloSeguro.lock:
                    if ContadorHiloSeguro.contador >= 1000:
                        break
                    ContadorHiloSeguro.contador += 1

            print(f"[{self.nombre}] Ha terminado. Contador = {ContadorHiloSeguro.contador}")

    ContadorHiloSeguro.contador = 0
    hilos_seguros = [ContadorHiloSeguro(f"HiloSeguro-{i+1}") for i in range(10)]

    for hilo in hilos_seguros:
        hilo.start()

    for hilo in hilos_seguros:
        hilo.join()

    print(f"\nValor final del contador: {ContadorHiloSeguro.contador}")
    print("Con Lock el valor final es exactamente 1000.")