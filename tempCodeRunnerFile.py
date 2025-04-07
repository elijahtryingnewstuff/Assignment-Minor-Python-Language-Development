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
                        result = interpreter.evaluate(statement)
                        if isinstance(statement, PrintNode):
                            print(result)  # Print only the final result
                        elif result is not None and not isinstance(statement, ListAssignNode):
                            print(result)
                except ReturnException as e:
                    print(f"{e.value}")
                except Exception as e:
                    print(f"Error: \"{e}\"")
                    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Unexpected error: {e}")