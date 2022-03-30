def parse_expr(w):
    expr, i = _parse_caf(w, 0)
    if i < len(w):
        raise ValueError(f"String was not consumed completely: {w[i:]}")
    return expr


def expr_to_str(expr):
    if isinstance(expr, str):
        return expr
    else:
        return "(" + " ".join(expr_to_str(p) for p in expr) + ")"


def evaluate_expr(expr):
    if isinstance(expr, str):
        return expr

    stack = expr[::-1]

    while len(stack) > 1 or isinstance(stack[0], list):
        fn = stack.pop()

        if isinstance(fn, list):
            stack.extend(reversed(fn))
        elif fn == "S":
            if len(stack) < 3:
                raise ValueError(f"Insufficient arguments for S")
            c_1 = stack.pop()
            c_2 = stack.pop()
            c_3 = stack.pop()
            stack.append([c_2, c_3])
            stack.append(c_3)
            stack.append(c_1)
        elif fn == "K":
            if len(stack) < 2:
                raise ValueError(f"Insufficient arguments for S")
            c_1 = stack.pop()
            stack.pop()  # c_2
            stack.append(c_1)
        elif fn == "I":
            pass  # keep c_1 there
        else:
            raise ValueError(f"Unknown fn: {fn}")

    return stack[0]


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
    if i < len(w) and w[i] in "SKI":
        return _parse_constant(w, i)
    elif i < len(w) and w[i] == "(":
        i = _match(w, i, "(")
        fn, i = _parse_caf(w, i)
        value = [fn]
        while i < len(w) and w[i] != ")":
            i = _match(w, i, " ")
            arg, i = _parse_caf(w, i)
            value.append(arg)
        i = _match(w, i, ")")
        return value, i
    else:
        _unexpected_error(w, i, "( or SKI")


def _parse_constant(w, i):
    return _parse_combinator(w, i)


def _parse_combinator(w, i):
    if i < len(w) and w[i] in "SKI":
        return w[i], i + 1
    else:
        _unexpected_error(w, i, "SKI")
