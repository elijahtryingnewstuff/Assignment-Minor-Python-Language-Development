# main.py
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, ReturnException
from nodes import PrintNode, ListAssignNode
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
            content = file.read()
            
            current_block = []
            for line in content.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue
                
                current_block.append(line)
                if is_balanced('\n'.join(current_block)):
                    text = '\n'.join(current_block)
                    try:
                        print(f"calc > {text}")
                        lexer = Lexer(text)
                        tokens = list(lexer.generate_tokens())
                        parser = Parser(tokens)
                        statements = parser.parse()
                        
                        for statement in statements:
                            if isinstance(statement, PrintNode):
                                result = interpreter.evaluate(statement.expression)
                                if result is not None:
                                    print(result)
                            else:
                                result = interpreter.evaluate(statement)
                                if result is not None and not isinstance(statement, ListAssignNode):
                                    print(result)
                    except ReturnException as e:
                        print(f"{e.value}")
                    except Exception as e:
                        print(f"Error: \"{e}\"")
                    current_block = []
            
            if current_block:
                text = '\n'.join(current_block)
                try:
                    print(f"calc > {text}")
                    lexer = Lexer(text)
                    tokens = list(lexer.generate_tokens())
                    parser = Parser(tokens)
                    statements = parser.parse()
                    
                    for statement in statements:
                        if isinstance(statement, PrintNode):
                            result = interpreter.evaluate(statement.expression)
                            if result is not None:
                                print(result)
                        else:
                            result = interpreter.evaluate(statement)
                            if result is not None and not isinstance(statement, ListAssignNode):
                                print(result)
                except ReturnException as e:
                    print(f"{e.value}")
                except Exception as e:
                    print(f"Error: \"{e}\"")
                    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Unexpected error: {e}")


def is_balanced(text):
    stack = []
    pairs = {'{': '}', '[': ']', '(': ')'}
    for char in text:
        if char in pairs:
            stack.append(char)
        elif char in pairs.values():
            if not stack or pairs[stack.pop()] != char:
                return False
    return len(stack) == 0

def run_interactive_mode():
    print("\nEntering interactive mode. Type 'help' for a list of commands.")
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
                        print(f"calc > {text}")  # Print the full multi-line input
                        lexer = Lexer(text)
                        tokens = list(lexer.generate_tokens())
                        parser = Parser(tokens)
                        statements = parser.parse()
                        for statement in statements:
                            if isinstance(statement, ListAssignNode):
                                interpreter.evaluate(statement)  # Evaluate but don't print
                            elif isinstance(statement, PrintNode):
                                result = interpreter.evaluate(statement.expression)
                                print(result)
                            else:
                                result = interpreter.evaluate(statement)
                                if result is not None:
                                    print(result)
                    except ReturnException as e:
                        print(e.value)
                    except Exception as e:
                        print(f"Error: {e}")
                    current_input = []
                continue
            
            current_input.append(line)
            text_so_far = '\n'.join(current_input)
            
            if is_balanced(text_so_far) and (len(current_input) == 1 or line.strip() != ""):
                try:
                    lexer = Lexer(text_so_far)
                    tokens = list(lexer.generate_tokens())
                    parser = Parser(tokens)
                    statements = parser.parse()
                    for statement in statements:
                        if isinstance(statement, ListAssignNode):
                            interpreter.evaluate(statement)  # Evaluate but don't print
                        elif isinstance(statement, PrintNode):
                            result = interpreter.evaluate(statement.expression)
                            print(result)
                        else:
                            result = interpreter.evaluate(statement)
                            if result is not None:
                                print(result)
                    current_input = []
                except ReturnException as e:
                    print(e.value)
                    current_input = []
                except Exception as e:
                    print(f"Error: {e}")
                    current_input = []
                except ReturnException as e:
                    print(e.value)
                except Exception as e:
                    print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {str(e)}")
            current_input = []

def main():
    user_input = input("Do you have a file to read? (yes/no): ").strip().lower()
    if user_input == "yes":
        filename = input("Please enter the name of the file: ").strip()
        run_tests_from_file(filename)
    run_interactive_mode()

if __name__ == "__main__":
    main()