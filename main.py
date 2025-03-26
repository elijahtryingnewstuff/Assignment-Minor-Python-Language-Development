# main.py
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import os

def display_help():
    print("Welcome to the interactive calculator!")
    print("Supported operations:")
    print("  - Arithmetic: +, -, *, /, %")
    print("  - Comparisons: ==, !=, <, >, <=, >=")
    print("  - Boolean logic: and, or, !")
    print("  - Strings: concatenation (+), equality (==, !=)")
    print("  - Control flow: if-else, while loops")
    print("Type 'exit' or 'quit' to exit the program.")
    print("Use blank line to submit multi-line input.")

def run_tests_from_file(filename):
    try:
        interpreter = Interpreter()
        with open(filename, "r") as file:
            current_block = []
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    current_block.append(line)
                    if is_balanced(' '.join(current_block)):
                        try:
                            text = '\n'.join(current_block)
                            print(f"calc > {text}")
                            lexer = Lexer(text)
                            tokens = list(lexer.generate_tokens())
                            parser = Parser(tokens)
                            statements = parser.parse()
                            for statement in statements:
                                result = interpreter.evaluate(statement)
                                if result is not None:  # Print all results
                                    print(result)
                            current_block = []
                        except Exception as e:
                            print("Error:", e)
                            current_block = []
            if current_block:
                try:
                    text = '\n'.join(current_block)
                    print(f"calc > {text}")
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
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def is_balanced(text):
    stack = []
    for char in text:
        if char == '{':
            stack.append(char)
        elif char == '}':
            if not stack:   
                return False
            stack.pop()
    return len(stack) == 0

def run_interactive_mode():
    print("Entering interactive mode. Type 'help' for a list of commands.")
    print("Submit multi-line input with a blank line or when braces are balanced.")
    interpreter = Interpreter()
    current_input = []
    
    while True:
        try:
            prompt = "calc > " if not current_input else "...... > "
            line = input(prompt).strip()
            
            if line.lower() in ["exit", "quit"]:
                print("Exiting interactive mode.")
                break
            elif line.lower() == "help":
                display_help()
                continue
            elif line == "":
                if current_input:
                    text = '\n'.join(current_input)
                    try:
                        print(f"calc > {text}")
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
                    current_input = []
                continue
            
            current_input.append(line)
            text_so_far = '\n'.join(current_input)
            
            if is_balanced(text_so_far):
                try:
                    print(f"calc > {text_so_far}")
                    lexer = Lexer(text_so_far)
                    tokens = list(lexer.generate_tokens())
                    parser = Parser(tokens)
                    statements = parser.parse()
                    for statement in statements:
                        result = interpreter.evaluate(statement)
                        if result is not None:
                            print(result)
                    current_input = []
                except Exception as e:
                    print("Error:", e)
                    # Keep current_input if parsing fails due to incomplete input
        except Exception as e:
            print("Error:", e)
            current_input = []

def main():
    user_input = input("Do you have a file to read? (yes/no): ").strip().lower()
    if user_input == "yes":
        filename = input("Please enter the name of the file: ").strip()
        run_tests_from_file(filename)
    run_interactive_mode()

if __name__ == "__main__":
    main()