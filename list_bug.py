tester = [[]] * 5
tester[1].append("hi")
print(type(tester[0]))
tester2 = [[] for _ in range(5)]
tester2[1].append("hi")

print(tester)
print(tester2)
