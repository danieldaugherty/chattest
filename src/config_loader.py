import os
import json
from typing import List, Dict, Any

class PromptConfig:
    def __init__(self, key: str, prompt: str, models: List[str], tests: List[str], runVolume: int, testModel: str, successThreshold: float):
        self.key = key
        self.prompt = prompt
        self.models = models
        self.tests = tests
        self.runVolume = runVolume
        self.testModel = testModel
        self.successThreshold = successThreshold

class ModelConfig:
    def __init__(self, key: str, url: str, apiKey: str = None, apiKeyHeader: str = None):
        self.key = key
        self.url = url
        self.apiKey = apiKey
        self.apiKeyHeader = apiKeyHeader

class ConfigLoader:
    def __init__(self, prompts_dir: str = 'configs/prompts/', models_dir: str = 'configs/models/'):
        self.prompts_dir = prompts_dir
        self.models_dir = models_dir

    def load_json_files(self, directory: str) -> List[Dict[str, Any]]:
        json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
        data = []
        for file in json_files:
            with open(os.path.join(directory, file), 'r') as f:
                data.append(json.load(f))
        return data

    def validate_prompt_config(self, data: Dict[str, Any]) -> bool:
        required_keys = {"key", "prompt", "models", "tests", "runVolume", "testModel", "successThreshold"}
        return required_keys.issubset(data.keys())

    def validate_model_config(self, data: Dict[str, Any]) -> bool:
        required_keys = {"key", "url"}
        return required_keys.issubset(data.keys())

    def load_prompts(self) -> List[PromptConfig]:
        prompt_data = self.load_json_files(self.prompts_dir)
        prompts = []
        for data in prompt_data:
            if self.validate_prompt_config(data):
                prompts.append(PromptConfig(**data))
        return prompts

    def load_models(self) -> List[ModelConfig]:
        from models_config import model_configs
        return model_configs
