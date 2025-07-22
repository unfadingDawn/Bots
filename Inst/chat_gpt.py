from openai import OpenAI

class CryptoAi:
    def __init__(self, config):
        self.client = OpenAI(api_key = config["openai_api_key"])
        self.prompt = config['openai_system_prompt']
        self.model = config['openai_model']
        self.temperature = config['openai_temperature']
        self.max_tokens = config['openai_max_tokens']

    def get_response(self, request: str) -> str:
        response = self.client.responses.create(
        model=f"{self.model}",
        instructions=f"{self.prompt}",
        input=request,
        temperature=self.temperature,
        max_output_tokens=self.max_tokens,)
        return response.output_text

