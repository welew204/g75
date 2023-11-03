

test1 = ["2", "1", "+", "3", "*"]
test2 = ["4", "13", "5", "/", "+"]
test3 = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]


def evalRPN(tokens):
    # make a stack (first in, last out)
    stack = []
    top_of_stack = 0

    # now tokens has no head
    while tokens:
        e = tokens.pop(0)
        try:
            stack.append(int(e))
            continue
        except:
            ValueError
        prev1, prev2 = stack.pop(), stack.pop()
        if e == "+":
            res = prev2 + prev1
        elif e == "-":
            res = prev2 - prev1
        elif e == "*":
            res = prev2 * prev1
        elif e == "/":
            res = int(prev2 / prev1)
        stack.append(res)
    return stack[0]

    # add elemtns to stack, until operator,
    # if op, then grab last two, return the result, ADD TO STACK
    # then proceed to end of tokens


print(evalRPN(test3))
