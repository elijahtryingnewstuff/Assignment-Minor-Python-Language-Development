from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import os

def run_tests_from_file(filename):
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"): 
                    try:
                        print(f"calc > {line}")
                        lexer = Lexer(line)
                        tokens = list(lexer.generate_tokens())  
                        parser = Parser(tokens)
                        tree = parser.parse()
                        if not tree:
                            continue
                        interpreter = Interpreter()
                        value = interpreter.evaluate(tree)
                        print(value)
                    except Exception as e:
                        print("Error:", e)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def run_interactive_mode():
    print("Entering interactive mode. Type your equations below.")
    while True:
        try:
            text = input("calc > ").strip()
            if text.lower() in ["exit", "quit"]:
                print("Exiting interactive mode.")
                break

            lexer = Lexer(text)
            tokens = list(lexer.generate_tokens())  
            parser = Parser(tokens)
            tree = parser.parse()
            if not tree:
                continue
            interpreter = Interpreter()
            value = interpreter.evaluate(tree)
            print(value)
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