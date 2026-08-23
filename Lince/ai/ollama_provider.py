import subprocess
import requests
import time
from datetime import datetime


class OllamaProvider:

    @staticmethod
    def is_available():

        try:

            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=3
            )

            return result.returncode == 0

        except Exception:

            return False


    @staticmethod
    def get_models():

        try:

            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return []

            models = []

            for line in result.stdout.splitlines()[1:]:

                if line.strip():

                    models.append(line.split()[0])

            return models

        except Exception:

            return []

    @staticmethod
    def generate(model, prompt):

        try:

            inicio = time.time()

            print("\n======================================")
            print("           OLLAMA")
            print("======================================")
            print(f"Modelo: {model}")
            print(f"Hora inicio: {datetime.now().strftime('%H:%M:%S')}")
            print(f"Longitud del prompt: {len(prompt)} caracteres")
            print("Enviando petición...\n")

            response = requests.post(

                "http://127.0.0.1:11434/api/generate",

                json={

                    "model": model,
                    "prompt": prompt,
                    "stream": False

                },

                timeout=3600

            )

            tiempo = time.time() - inicio

            print("\nRespuesta recibida.")
            print(f"Hora fin: {datetime.now().strftime('%H:%M:%S')}")
            print(f"Tiempo total: {tiempo:.2f} segundos")
            print("======================================\n")

            if response.status_code == 200:

                return response.json()["response"].strip()

            return f"Error HTTP {response.status_code}"

        except Exception as e:

            tiempo = time.time() - inicio

            print("\n*** ERROR OLLAMA ***")
            print(e)
            print(f"Tiempo transcurrido: {tiempo:.2f} segundos")
            print("********************\n")

            return str(e)