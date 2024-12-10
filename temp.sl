---
equation eq_1: ((2/5)*x)^3/(15+y) =
                         2*z/(x+z)
equation eq_2: x ^ 2 + 5 * x + 3 = y
print: eq_1
print: eq_2
integrate: integral, eq_2, x
differentiate: derivative, eq_2, x
print: integral
print: derivative
equation solve_example: ((x^2 + 3*x*y + 5 + 6 * z)*
(y^3 + 2*y^2 + 9))/(z ^ 15 - 1) = 0
print: solve_example
solve: solved_example, solve_example, x
print: solved_example
---

