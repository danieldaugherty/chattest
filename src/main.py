import argparse
import sys
from config_loader import ConfigLoader
from inference_runner import InferenceRunner
from evaluation_component import EvaluationComponent
from reporting_module import ReportingModule

def main():
    parser = argparse.ArgumentParser(description="chattest framework")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--prompt-key', type=str, help='Key of the prompt to test')
    group.add_argument('-a', '--all-prompts', action='store_true', help='Run all prompts')
#     parser.add_argument('--verbosity', type=int, default=1, help='Verbosity level of the output')
    args = parser.parse_args()

    try:
        # Load configurations
        config_loader = ConfigLoader()
        prompts = config_loader.load_prompts()
        models = config_loader.load_models()

        # Filter prompts based on the provided prompt key
        if args.prompt_key:
            selected_prompts = [prompt in prompts if prompt.key == args.prompt_key]
            if not selected_prompts:
                print(f"No prompt found with key: {args.prompt_key}")
                sys.exit(1)
        else:
            selected_prompts = prompts

        # Run inference
        inference_runner = InferenceRunner(selected_prompts, models)
        inference_runner.run_inference()
        outputs = inference_runner.get_outputs()

        # Evaluate outputs
        evaluation_component = EvaluationComponent(outputs, selected_prompts)
        evaluation_component.evaluate()
        evaluation_component.aggregate_results()
        results = evaluation_component.get_results()

        # Report results
        reporting_module = ReportingModule(results)
        reporting_module.output_results()
        reporting_module.log_results()

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
