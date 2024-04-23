import re
import random
import importlib
import google.generativeai as genai
from common.llm_test_generator import LLMTestGenerator
from common.prompt_generator import PromptGenerator
from common.abstract_executor import AbstractExecutor
from to_test.number_to_words import number_to_words

# Function to extract assertions from generated test function string
def extract_assertions(test_function_str):
    return [line.strip() for line in test_function_str.splitlines() if line.strip().startswith('assert')]


def generate_expected_result(number):
    """
    Generate string representation of a number.
    """
    # Randomly select from a predefined list of string representations
    representations = {
        0: "Zero",
        5: "Five",
        8: "Eight",
        10: "Ten",
        11: "Eleven",
        16: "Sixteen",
        19: "Nineteen",
        20: "Twenty",
        30: "Thirty",
        60: "Sixty",
        70: "Seventy",
        100: "One Hundred",
        200: "Two Hundred",
        500: "Five Hundred",
        800: "Eight Hundred",
        900: "Nine Hundred",
        1000: "One Thousand",
        2000: "Two Thousand",
        3000: "Three Thousand",
        4000: "Four Thousand",
        5000: "Five Thousand",
        9000: "Nine Thousand",
        9999: "Nine Thousand Nine Hundred Ninety Nine",
        123: "One Hundred Twenty Three",
        456: "Four Hundred Fifty Six",
        789: "Seven Hundred Eighty Nine",
        5555: "Five Thousand Five Hundred Fifty Five",
        8888: "Eight Thousand Eight Hundred Eighty Eight"
    }

    # Return the string representation if it exists, otherwise return a placeholder
    try:
        return representations[number]
    except:
        return 'Zero'

def mutate_assertion(a):
    """
    Generate a new assertion using a random input and expected result.
    """
    # Generate a random number for the input value
    input_value = random.randint(0, 9999)

    # Generate the expected result string representation
    expected_result = generate_expected_result(input_value)

    # Generate the assertion string with preserved input and output formats
    assertion = f"assert number_to_words({str(input_value)}) == \"{expected_result}\""
    return assertion

# Function to combine two assertions (crossover)
def crossover(assertion1, assertion2):
    return random.choice([assertion1, assertion2])
def genetic_algorithm(assertions, num_generations=10, population_size=20, top_n=5):
    """
    Run a genetic algorithm to enhance a set of initial assertions.
    """
    population = [random.choice(assertions) for _ in range(population_size)]
    for _ in range(num_generations):
        new_population = [mutate_assertion(a) for a in population] + \
                         [crossover(a, random.choice(population)) for a in population]
        population = sorted(new_population, key=lambda x: len(set(x)), reverse=True)[:population_size]

    return set(sorted(population, key=lambda x: len(set(x)), reverse=True)[:top_n])

def write_test_function_to_file(filename, function_name, assertions):
    """
    Write a test function with multiple assertions to a Python file.
    """
    with open(filename, 'w') as f:
        f.write(f"def {function_name}(number_to_words):\n")
        for assertion in assertions:
            f.write(f"    {assertion}\n")

def generate_initial_tests_with_llm(model, function_to_test):
    """
    Generate initial tests using a language model.
    """
    llm_generator = LLMTestGenerator(model, function=function_to_test)
    prompt_generator = PromptGenerator(function_to_test)
    prompt = prompt_generator.generate_prompt()
    test_code, test_name = llm_generator.create_test_function(prompt)
    filename = "test_generated.py"
    llm_generator.write_test_to_file(test_code, filename=filename)
    input("Please review the generated tests before continuing...")
    module_name = filename.split(".")[0]
    module = importlib.import_module(module_name)
    function = getattr(module, test_name)
    executor = AbstractExecutor(function)
    coverage_data = executor._execute_input(input=function_to_test)
    return test_code, test_name, coverage_data

def main():
    """
    Main execution function to handle the workflow.
    """
    key = "AIzaSyBvPW7KFWPLy1eIOZsocoonKW5ZnHyIQXo"
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-pro')
    function_to_test = number_to_words

    test_code, test_name, coverage_data = generate_initial_tests_with_llm(model, function_to_test)
    initial_coverage = coverage_data

    assertions = extract_assertions(test_code)
    enhanced_assertions = genetic_algorithm(assertions)
    
    new_test_filename = "enhanced_test_generated.py"
    write_test_function_to_file(new_test_filename, test_name, enhanced_assertions)
    input("Enhanced test cases have been written to: enhanced_test_generated.py please review them")

    module_name = new_test_filename.split('.')[0]
    module = importlib.import_module(module_name)
    test_function = getattr(module, test_name)
    executor = AbstractExecutor(test_function)
    print(test_function)
    print(test_function.__name__)
    try:
        coverage_data = executor._execute_input(function_to_test)
        print("Enhanced coverage data:", coverage_data)
    except Exception as e:
        print(f"Exception occurred: {e}")

    print(f"Initial coverage: {initial_coverage['coverage']}")
    print(f"Final coverage: {coverage_data['coverage']}")

    line_coverage_improvement = coverage_data["coverage"]["percent_covered"] - initial_coverage["coverage"]["percent_covered"]
    branch_coverage_improvement = coverage_data["coverage"]["covered_branches"]/coverage_data["coverage"]["num_branches"] - initial_coverage["coverage"]["covered_branches"]/initial_coverage["coverage"]["num_branches"]
    print("line coverage improvement is ",line_coverage_improvement)
    print("branch coverage improvement is ", branch_coverage_improvement)
    total_tests = len([function_to_test])
    final_score = (line_coverage_improvement + branch_coverage_improvement) / total_tests
    print(f"Final score: {final_score}")


if __name__ == "__main__":
    main()