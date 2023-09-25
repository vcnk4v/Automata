# DESCRIPTION

Rules for Syntactic Analysis

1. S → statement
2. statement → if (A)| (statement)(statement) | y
3. y ∈ statement alphabets [Σstatement ]
4. A → (cond)(statement) | (cond)statement(else)statement
5. cond → (x op1 x) | x
6. op1 → + | - | \* | / |ˆ| < | > | =
7. x → R | cond | y

Errors are raised if any of the rule is violated.

Σstatement = numbers ∪ keywords ∪ identifiers - ’if ’ and ’else’.

It does NOT include operations.

Semicolons are ignored.

- if_function: function for if which either goes to (cond)(statement) or (cond)statement(else)statement
- y_function: terminal Σstatement
- condition_function: either goes to x op x or z
- x_function: goes to R or Σstatement or condition_function
- op_function: checks for valid operation
- statement_function: checks for if, else if found bracktes, goes to (statement)(statement), otherwise y_function

## ASSUMPTIONS IN Q2

### Statement Rule

1. Rule for statement is implemented with brackets:
   statement-->(statement)(statement), otherwise it will assume statement--> y (terminal).

2. Symbols do not belong to statement alphabet, so syntax error is raised when a statement like "print 2>3" is given, but - and + are accepted because they are used to represent negatuve and positive numbers.

### If Rule

1. Rule for "if" is implemented with brackets:

   - if--> (cond)(statement) | (cond) statement (else) statement
   - "else" works both with and without brackets
   - For conditions with nested operations, brackets are required.
     eg. (1+2) and ((1+2)>3) are valid, (1+2>3) is not valid.

2. Rule for x and cond are also implemented with brackets (operations do not require brackets): x--> (x)op1(x)|R|y and cond-->(x op1 x)|x.
