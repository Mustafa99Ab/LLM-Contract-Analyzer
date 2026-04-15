"""
Model client abstraction for inference.
Supports local models (via Unsloth) and API-based models.
Adapted from Nicola Tortora's clients.py.
"""

from unsloth import FastLanguageModel


class LocalClient:
    """Client for local model inference using Unsloth."""

    def __init__(self, model_name: str, max_seq_length: int = 2048):
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=model_name,
            max_seq_length=max_seq_length,
            load_in_4bit=True,
        )
        FastLanguageModel.for_inference(self.model)

    def generate(self, messages: list, max_new_tokens: int = 2048) -> str:
        """Generate a response from the model."""
        inputs = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        ).to("cuda")

        outputs = self.model.generate(
            input_ids=inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.6,
            top_p=0.95,
        )

        response = self.tokenizer.decode(
            outputs[0][inputs.shape[-1]:], skip_special_tokens=True
        )
        return response


class APIClient:
    """Client for API-based model inference (e.g., OpenAI-compatible)."""

    def __init__(self, model_name: str, base_url: str, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name = model_name

    def generate(self, messages: list, max_new_tokens: int = 2048) -> str:
        """Generate a response via API."""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=max_new_tokens,
            temperature=0.6,
        )
        return response.choices[0].message.content


def get_client(config: dict):
    """Factory function to create the appropriate client."""
    if config["type"] == "local":
        return LocalClient(config["model_name"])
    elif config["type"] == "api":
        return APIClient(
            config["model_name"],
            config["base_url"],
            config["api_key"],
        )
    else:
        raise ValueError(f"Unknown client type: {config['type']}")
