**Language Design and Implementation (LDI) CW2 - Stage 2 Implementation**

This part of the project (Part 2 - Stages 1 - 4) implements a simple interpreter for a custom programming language that uses python as a base. The interpreter supports the following features:

I. Basic Arithmetic Operations:

-Addition (+), subtraction (-), multiplication (*), and division (/).
-Unary negation (-).
-Parentheses for grouping expressions.

II. Boolean Logic
-Binary comparisons: ==, !=, <, >, <=, >=.
-Logical operations: and, or.
-Unary negation: not.

III. Text Values (Strings)

-Support for string literals (e.g., "hello").
-String concatenation using the + operator.
-String equality (==) and inequality (!=) comparisons.
-Strict type checking to prevent operations between incompatible types (e.g., "hello" + 123 raises a TypeError).

IV. Global Variables
-Support for global variable assignment and retrieval.
-Variables can store numbers, booleans, or strings.
-Variables can be used in expressions (e.g., x = 10; y = x + 5).
-Variables persist across expressions in interactive mode.

1. **Interactive Mode**:
- Run the interpreter in interactive mode by executing `python main.py` or by pressing the run button on the 'main.py' file in the environment
- Enter expressions directly on the terminal, and the interpreter will evaluate and print the result.
Terminal Example:

calc > x = 10
Assigned x = 10.0
calc > y = x + 5
Assigned y = 15.0
calc > print y
15.0

2. **File Mode**:
- The program will ask if you want to read a file and solve the equations on the file first. If yes:
-- Run the interpreter with a source file by executing `python main.py <source_file>`.
-- The interpreter will evaluate each line of the file and print the results.

Example input:
x = 10
y = x + 5
print y

Example output:
Assigned x = 10.0
Assigned y = 15.0
15.0

If no: 
Transfer to interactive mode so the user can enter equations on the terminal directly.


3. Limitations
The interpreter currently does not support control flow (e.g., if statements, loops) or functions (Stage 5 and 6).
Error handling is basic and may not cover all edge cases. (For now)
File reading may fail if the source file is corrupted or contains invalid syntax.

4. Design Decisions
Strict Type Checking:
The interpreter enforces strict type checking to prevent operations between incompatible types (e.g., "hello" + 123 raises a TypeError).
This ensures predictable behavior and reduces runtime errors.

Global Variables:
Global variables are stored in a dictionary for O(1) access time.
Variables persist across expressions in interactive mode.

Error Handling:
Basic error handling is implemented to catch and report common errors (e.g., undefined variables, type mismatches).


** Future Work **
Stage 5: Control Flow
Implement if statements and loops (while).
Add support for user input (e.g., input("Enter a value: ")).
Stage 6: Additional Features
Add support for lists and dictionaries.
Implement functions for code reusability.
Introduce local variables for better scoping.

Add extra features that I think of 
