from textx import metamodel_from_file
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
symbols_set = set()
equations_dict = {}

def main():
    # Load the symbolic computation grammar
    meta = metamodel_from_file('sym_lang.tx')

    # Parse a sample input using the grammar
    model = meta.model_from_file('temp.sl')

    for s in model.statements:
        if s.startswith('equation'):
            interpret_equation(s)
        if s.startswith('symbols'):
            interpret_symbol_list(s)
        if s.startswith('solve'):
            interpret_solve(s)
        if s.startswith('print'):
            interpret_print(s)
        if s.startswith('differentiate'):
            interpret_differentiate(s)
        if s.startswith('integrate'):
            interpret_integrate(s)


def interpret_equation(s):
    s = s.split(' ')
    name = s[1][:-1]
    name = s[1][:-1]
    sides = s[2].split('=')
    lhs, rhs = sp.sympify(sides[0]), sp.sympify(sides[1])
    equation = sp.Eq(lhs, rhs)
    equations_dict[name] = equation

def interpret_symbol_list(s):
    s = s.split(':')
    symbols = s[1].split(',')
    for i in symbols:
        symbols_set.add(sp.symbols(i))

def interpret_solve(s):
    rhs = s.split(':')[1].split(',')
    new_eq_name = rhs[0]
    existing_eq_name = rhs[1]
    var = rhs[2]
    var = sp.symbols(var)
    sol = sp.solve(get_equation(existing_eq_name), var)
    equations_dict[new_eq_name] = sp.Eq(var, sol[0])

def interpret_print(s):
    rhs = s.split(':')[1]
    sp.pprint(get_equation(rhs))
    print()

def interpret_differentiate(s):
    rhs = s.split(':')[1].split(',')
    new_eq_name = rhs[0]
    existing_eq_name = rhs[1]
    var = rhs[2]
    # Differentiate both sides with respect to x
    lhs_diff = sp.diff(get_equation(existing_eq_name).lhs, var)  # Differentiate the left-hand side
    rhs_diff = sp.diff(get_equation(existing_eq_name).rhs, var)  # Differentiate the right-hand side

    # Combine the results into an equation
    equations_dict[new_eq_name] = sp.Eq(lhs_diff, rhs_diff)

def interpret_integrate(s):
    rhs = s.split(':')[1].split(',')
    new_eq_name = rhs[0]
    existing_eq_name = rhs[1]
    var = rhs[2]
    
    # integrate
    lhs_int = sp.integrate(get_equation(existing_eq_name).lhs, sp.symbols(var))
    rhs_int = sp.integrate(get_equation(existing_eq_name).rhs, sp.symbols(var))

    equations_dict[new_eq_name] = sp.Eq(lhs_int, rhs_int)

def get_equation(eq):
    try:
        return equations_dict[eq]
    except:
        raise ValueError(f'Undefined variable \"{eq}\" referenced')


if __name__ == '__main__':
    main()