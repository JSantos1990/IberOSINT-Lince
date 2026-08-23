from google import genai
import concurrent.futures
import time


class GeminiProvider:

    @staticmethod
    def is_available(api_key=None):
        """
        Comprueba si se ha proporcionado una API Key.
        """
        return bool(api_key)


    @staticmethod
    def get_models():
        """
        De momento devolvemos una lista fija.
        Más adelante la obtendremos desde la API.
        """
        return [
            "gemini-flash-latest"
        ]

    @staticmethod
    def format_error(error):
        """
        Convierte errores técnicos de Gemini en mensajes más claros.
        """

        mensaje = str(error)
        mensaje_mayusculas = mensaje.upper()

        if (
            "503" in mensaje
            or "UNAVAILABLE" in mensaje_mayusculas
        ):
            return (
                "Gemini no está disponible temporalmente o el modelo "
                "está experimentando una alta demanda. "
                "Inténtalo de nuevo más tarde."
            )

        if (
            "429" in mensaje
            or "RESOURCE_EXHAUSTED" in mensaje_mayusculas
            or "RATE LIMIT" in mensaje_mayusculas
            or "QUOTA" in mensaje_mayusculas
        ):
            return (
                "Se ha alcanzado temporalmente un límite de uso de la "
                "API de Gemini. Espera unos minutos e inténtalo de nuevo."
            )

        if (
            "401" in mensaje
            or "UNAUTHENTICATED" in mensaje_mayusculas
            or "INVALID API KEY" in mensaje_mayusculas
            or "API KEY NOT VALID" in mensaje_mayusculas
        ):
            return (
                "La API Key de Gemini no es válida o no ha podido ser "
                "autenticada. Comprueba la clave introducida."
            )

        if (
            "403" in mensaje
            or "PERMISSION_DENIED" in mensaje_mayusculas
            or "PERMISSION DENIED" in mensaje_mayusculas
        ):
            return (
                "La API Key de Gemini no tiene permisos para utilizar "
                "este servicio o modelo."
            )

        if isinstance(error, TimeoutError):
            return (
                "Gemini no ha respondido dentro del tiempo máximo de "
                "espera de 90 segundos."
            )

        if (
            "TIMEOUT" in mensaje_mayusculas
            or "TIMED OUT" in mensaje_mayusculas
        ):
            return (
                "La conexión con Gemini ha superado el tiempo máximo "
                "de espera."
            )

        return f"Error al consultar Gemini: {mensaje}"


    @staticmethod
    def generate(model, prompt, api_key=None):
        """
        Genera una respuesta utilizando Gemini.
        La API Key se recibe temporalmente desde la interfaz.
        """

        if not api_key:
            raise ValueError(
                "No se ha proporcionado una API Key de Gemini."
            )

        max_intentos = 4

        for intento in range(1, max_intentos + 1):

            try:

                print(
                    f"LINCE | Intento {intento} de {max_intentos} "
                    f"para consultar Gemini..."
                )

                print("LINCE | Creando cliente de Gemini...")

                client = genai.Client(
                    api_key=api_key
                )

                print(
                    f"LINCE | Preparando petición a Gemini "
                    f"| Modelo: {model} "
                    f"| Caracteres del prompt: {len(prompt)}"
                )

                executor = concurrent.futures.ThreadPoolExecutor(
                    max_workers=1
                )

                future = executor.submit(
                    client.models.generate_content,
                    model=model,
                    contents=prompt
                )

                print(
                    "LINCE | Petición enviada a Gemini. "
                    "Esperando respuesta..."
                )

                try:

                    response = future.result(
                        timeout=90
                    )

                except concurrent.futures.TimeoutError:

                    future.cancel()

                    raise TimeoutError(
                        "Gemini no ha respondido en 90 segundos. "
                        "La petición ha superado el tiempo máximo de espera."
                    )

                finally:

                    executor.shutdown(
                        wait=False,
                        cancel_futures=True
                    )

                print(
                    "LINCE | Respuesta recibida correctamente de Gemini."
                )

                if not response.text:

                    raise RuntimeError(
                        "Gemini ha devuelto una respuesta vacía."
                    )

                return response.text.strip()

            except Exception as e:

                mensaje_error = str(e)

                print(
                    f"LINCE | ERROR EN INTENTO {intento}: "
                    f"{type(e).__name__}: {mensaje_error}"
                )

                error_temporal = (
                    "503" in mensaje_error
                    or "UNAVAILABLE" in mensaje_error.upper()
                    or "429" in mensaje_error
                    or "RESOURCE_EXHAUSTED" in mensaje_error.upper()
                    or "RATE LIMIT" in mensaje_error.upper()
                )

                if not error_temporal:
                    raise

                if intento == max_intentos:
                    raise

                espera = 2 ** (intento - 1)

                print(
                    f"LINCE | Error temporal detectado. "
                    f"Nuevo intento en {espera} segundo(s)..."
                )

                time.sleep(espera)   

    @staticmethod
    def self_test(api_key=None):
        """
        Comprueba que la conexión con Gemini funciona correctamente.
        """

        respuesta = GeminiProvider.generate(
            "gemini-flash-latest",
            "Responde únicamente con la palabra: OK",
            api_key
        )

        return respuesta