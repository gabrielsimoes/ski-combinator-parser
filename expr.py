from copy import deepcopy

def parse_expr(w):
    expr, i = _parse_caf(w, 0)
    if i < len(w):
        raise ValueError(f"String was not consumed completely: {w[i:]}")
    return expr


def expr_to_str(expr):
    if isinstance(expr, list):
        return "(" + " ".join(expr_to_str(p) for p in expr) + ")"
    else:
        return str(expr)


def _evaluate_y(stack):
    if len(stack) < 2:
        stack.append("Y")
        return False
    c_1 = stack.pop()
    stack.append(["Y", c_1])
    stack.append(c_1)
    return True


def _evaluate_s(stack):
    if len(stack) < 3:
        stack.append("S")
        return False
    c_1 = stack.pop()
    c_2 = stack.pop()
    c_3 = stack.pop()
    stack.append([c_2, c_3])
    stack.append(c_3)
    stack.append(c_1)
    return True


def _evaluate_k(stack):
    if len(stack) < 2:
        stack.append("K")
        return False
    c_1 = stack.pop()
    stack.pop()  # c_2
    stack.append(c_1)
    return True


def _evaluate_i(stack):
    if len(stack) < 1:
        stack.append("I")
        return False
    # keep c_1 there
    return True


EVALUATORS = {
    "S": _evaluate_s,
    "K": _evaluate_k,
    "I": _evaluate_i,
}

OPTIONAL_EVALUATORS = {
    "Y": _evaluate_y,
}

ZERO = ["K", "I"]

SUCC = ["S", ["S", ["K", "S"], "K"]]

ADD = ["S", ["K", "S"], ["S", ["K", ["S", ["K", "S"], "K"]]]]

CONSTANTS = {
    "succ": SUCC,
    "add": ADD,
    "+": ADD,
}


def _number_evaluator(n, stack):
    if n == 0:
        stack.append(ZERO)
    else:
        stack.append(["succ", n - 1])
    return True


def _evaluate_top(stack, optional_enabled):
    primary = stack.pop()

    if isinstance(primary, list):
        stack.extend(reversed(primary))
        return True
    elif primary in EVALUATORS:
        evaluator = EVALUATORS[primary]
        return evaluator(stack)
    elif optional_enabled and primary in OPTIONAL_EVALUATORS:
        evaluator = OPTIONAL_EVALUATORS[primary]
        return evaluator(stack)
    elif optional_enabled and primary in CONSTANTS:
        stack.append(CONSTANTS[primary])
        return True
    elif optional_enabled and (isinstance(primary, int) or (isinstance(primary, str) and primary in "0123456789")):
        return _number_evaluator(int(primary), stack)
    else:
        stack.append(primary)
        return False


def _evaluate_expr(expr, output, optional_enabled, tabs=0):
    # make single symbols into a list
    if not isinstance(expr, list):
        expr = [expr]

    # invert expression to make it a python stack
    stack = expr[::-1]
    
    # evaluate top of the stack until we cannot anymore or don't know what to do
    while isinstance(stack, list):
        if not _evaluate_top(stack, optional_enabled):
            break
        
        if output:
            print(">>" * tabs, expr_to_str(stack[::-1]), sep="")

    # evaluate recursively
    if len(stack) == 1:
        stack = stack[0]
        # if output:
        #     print(">>" * tabs, expr_to_str(stack[::-1]), sep="")
        return stack
    
    for i in range(len(stack)-2, -1, -1):
        stack[i] = _evaluate_expr(stack[i], output, optional_enabled, tabs + 1)

    return stack[::-1]


def evaluate_expr(expr, output=False, optional_enabled=True):
    result = _evaluate_expr(expr, output, optional_enabled)
    if isinstance(result, list) and len(result) == 1:
        result = result[0]
    print(expr_to_str(result))
    return result

def _unexpected_error(w, i, expected="*"):
    if i < len(w):
        raise ValueError(
            f'Unexpected character {w[i]} at position {i}, expected one of "{expected}".'
        )
    else:
        raise ValueError(f'Unexpected end of string, expected one of "{expected}".')


def _match(w, i, expected):
    if i < len(w) and w[i] == expected:
        return i + 1
    else:
        _unexpected_error(w, i, ")")


def _parse_caf(w, i):
    if i < len(w) and w[i] == "(":
        i = _match(w, i, "(")
        fn, i = _parse_caf(w, i)
        value = [fn]
        while i < len(w) and w[i] != ")":
            i = _match(w, i, " ")
            arg, i = _parse_caf(w, i)
            value.append(arg)
        i = _match(w, i, ")")
        return value, i
    elif i < len(w):
        return _parse_primary(w, i)
    else:
        _unexpected_error(w, i)


def _parse_primary(w, i):
    o = ""
    while i < len(w) and w[i] not in " )":
        o += w[i]
        i += 1

    if not o:
        raise ValueError(f"Unexpected empty object at position {i}.")

    return o, i
