class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if len(self.mins) == 0:
            self.mins.append(val)
        else:
            self.mins.append(min(val, self.mins[-1]))

    def pop(self) -> None:
        self.stack.pop()
        self.mins.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.mins[-1] if len(self.mins) != 0 else "null"


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()

instructions = ["MinStack", "push", "push",
                "push", "getMin", "pop", "top", "getMin"]
values = [[], [-2], [0], [-3], [], [], [], []]

instructions2 = ["MinStack", "push", "push", "push", "push",
                 "getMin", "pop", "getMin", "pop", "getMin", "pop", "getMin"]
values2 = [[], [2], [0], [3], [0], [], [], [], [], [], [], []]

output = []

for i, ins in enumerate(instructions2):
    if ins == "MinStack":
        stack = MinStack()
        output.append("null")
    elif ins == "push":
        stack.push(val=values2[i][0])
        output.append("null")
    elif ins == "pop":
        stack.pop()
        output.append("null")
    elif ins == "top":
        output.append(stack.top())
    elif ins == "getMin":
        output.append(stack.getMin())


exp_output = ["null", "null", "null", "null", -3, "null", 0, -2]
