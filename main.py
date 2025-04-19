from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import os

def display_help():
    print("Welcome to the interactive calculator!")
    print("Supported operations:")
    print("  - Arithmetic: +, -, *, /")
    print("  - Comparisons: ==, !=, <, >, <=, >=")
    print("  - Boolean logic: and, or, not")
    print("  - Strings: concatenation (+), equality (==, !=)")
    print("Type 'exit' or 'quit' to exit the program.")

def run_tests_from_file(filename):
    try:
        interpreter = Interpreter()
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    try:
                        print(f"calc > {line}")
                        lexer = Lexer(line)
                        tokens = list(lexer.generate_tokens())
                        parser = Parser(tokens)
                        statements = parser.parse()
                        for statement in statements:
                            result = interpreter.evaluate(statement)
                            if result is not None:
                                print(result) 
                    except Exception as e:
                        print("Error:", e)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def run_interactive_mode():
    print("Entering interactive mode. Type 'help' for a list of commands.")
    interpreter = Interpreter()
    while True:
        try:
            text = input("calc > ").strip()
            if text.lower() in ["exit", "quit"]:
                print("Exiting interactive mode.")
                break
            elif text.lower() == "help":
                display_help()
                continue
            if not text:
                continue
            lexer = Lexer(text)
            tokens = list(lexer.generate_tokens())
            parser = Parser(tokens)
            statements = parser.parse()
            for statement in statements:
                result = interpreter.evaluate(statement)
                if result is not None:
                    print(result)  
        except Exception as e:
            print("Error:", e)

def main():
    user_input = input("Do you have a file to read? (yes/no): ").strip().lower()
    if user_input == "yes":
        filename = input("Please enter the name of the file: ").strip()
        run_tests_from_file(filename)
    run_interactive_mode()

if __name__ == "__main__":
    main()