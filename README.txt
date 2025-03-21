**Language Design and Implementation (LDI) CW2 - Stage 2 Implementation**


This part of the project (Part 1 - Stage 1 and 2) implements a simple interpreter for a custom programming language that uses python as a base. 
The project can read files that are in the folders that are being used in the development environment.
The files include snippets of code that can be used to develop stage 3+ from the assignment but they are incomplete. Meaning that functions that are mentioned in stage 1 and stage 2 can be used.


The following files include:

I. **Basic Arithmetic Operations**
 - Addition (`+`), subtraction (`-`), multiplication (`*`), and division (`/`).
 - Unary negation (`-`).
 - Parentheses for grouping expressions.


II. **Boolean Logic**
- Binary comparisons: `==`, `!=`, `<`, `>`, `<=`, `>=`.
- Logical operations: `and`, `or`.
- Unary negation: `not`.

1. **Interactive Mode**:
- Run the interpreter in interactive mode by executing `python main.py` or by pressing the run button on the 'main.py' file in the environment
- Enter expressions directly on the terminal, and the interpreter will evaluate and print the result.

2. **File Mode**:
- The program will ask if you want to read a file and solve the equations on the file first. If yes:
-- Run the interpreter with a source file by executing `python main.py <source_file>`.
-- The interpreter will evaluate each line of the file and print the results.

If no: 
Transfer to interactive mode so the user can enter equations on the terminal directly.

3. **Limitations**:
- The interpreter currently does not support variables or control flow (stages 3-6).
- Error handling is basic and may not cover all edge cases.
- File reading may not work if the source files are corrputed


**Future Work**:
- Implement a power function so number can be powered (Stage 1). 
- Implement support for text values (Stage 3).
- Add global variables (Stage 4).
- Introduce control flow (Stage 5).
- Extend the language with additional features (Stage 6).