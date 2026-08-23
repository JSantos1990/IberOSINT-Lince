from ai.ollama_provider import OllamaProvider
from ai.gemini_provider import GeminiProvider


class AIManager:

    @staticmethod
    def generate(provider, model, prompt, api_key=None):

        if provider == "ollama":
            return OllamaProvider.generate(
                model,
                prompt
            )

        elif provider == "gemini":
            return GeminiProvider.generate(
                model,
                prompt,
                api_key
            )

        else:
            raise ValueError(
                f"Proveedor IA no soportado: {provider}"
            )