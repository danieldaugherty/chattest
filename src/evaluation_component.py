from typing import List, Dict, Any
from config_loader import PromptConfig
from inference_runner import InferenceRunner

class EvaluationComponent:
    def __init__(self, outputs: List[Dict[str, Any]], prompts: List[PromptConfig]):
        self.outputs = outputs
        self.prompts = prompts
        self.results = []

    def evaluate(self):
        for output in self.outputs:
            prompt = next((p for p in self.prompts if p.key == output["prompt_key"]), None)
            if prompt:
                for test in prompt.tests:
                    evaluation_result = self.evaluate_output(output["output"], test, prompt.testModel)
                    self.results.append({
                        "prompt_key": output["prompt_key"],
                        "model_key": output["model_key"],
                        "run_number": output["run_number"],
                        "test": test,
                        "result": evaluation_result
                    })

    def evaluate_output(self, output: str, test: str, test_model: str) -> str:
        # Placeholder for actual evaluation logic using the test_model
        # This should send the output and test to the evaluation model and return PASS or FAIL
        return "PASS" if test in output else "FAIL"

    def aggregate_results(self):
        aggregated_results = {}
        for result in self.results:
            key = (result["prompt_key"], result["test"])
            if key not in aggregated_results:
                aggregated_results[key] = {"pass_count": 0, "total_runs": 0}
            if result["result"] == "PASS":
                aggregated_results[key]["pass_count"] += 1
            aggregated_results[key]["total_runs"] += 1

        for key, value in aggregated_results.items():
            success_rate = value["pass_count"] / value["total_runs"]
            prompt_key, test = key
            prompt = next((p for p in self.prompts if p.key == prompt_key), None)
            if prompt:
                pass_fail = "PASS" if success_rate >= prompt.successThreshold else "FAIL"
                self.results.append({
                    "prompt_key": prompt_key,
                    "test": test,
                    "success_rate": success_rate,
                    "result": pass_fail
                })

    def get_results(self) -> List[Dict[str, Any]]:
        return self.results
