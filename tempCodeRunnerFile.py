
                    tokens = list(lexer.generate_tokens())
                    parser = Parser(tokens)
                    statements = parser.parse()
                    for statement in stat