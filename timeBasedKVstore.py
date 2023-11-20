import collections


class TimeMap:

    def __init__(self):
        self.timeMap = collections.defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.timeMap or timestamp >= self.timeMap[key][-1][1]:
            self.timeMap[key].append([value, timestamp])
        else:
            # run binSearch to find slot
            r, l = 0, len(self.timeMap[key]-1)
            while l < r:
                ctr = (r + l) // 2
                ts_in_q = self.timeMap[key][ctr][1]
                if ts_in_q == timestamp:
                    self.timeMap[key].insert(ctr, [value, timestamp])
                elif ts_in_q > timestamp:
                    r = ctr - 1
                elif ts_in_q > timestamp:
                    l = ctr + 1
            self.timeMap[key].insert(ctr, [value, timestamp])

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.timeMap:
            return ""
        options = self.timeMap[key]
        for ri in range(len(options)-1, -1, -1):
            val, ts = options[ri]
            if ts == timestamp:
                return val
            elif ts < timestamp:
                return val
        # has not found a value w/ ts that is <= to timestamps
        return ""


def checkr(instructions, vals):
    out = []
    for i in range(len(instructions)):
        if instructions[i] == "TimeMap":
            tm = TimeMap()
            out.append(None)
        elif instructions[i] == "set":
            key, val, ts = vals[i]
            tm.set(key, val, ts)
            out.append(None)
        elif instructions[i] == "get":
            key, ts = vals[i]
            out.append(tm.get(key, ts))
        # print most recent res
        print(out[-1])
    return out


inst1 = ["TimeMap", "set", "get", "get", "set", "get", "get"]
vals1 = [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3],
         ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
inst2 = ["TimeMap", "set", "set", "get", "get", "get", "get", "get"]
vals2 = [[], ["love", "high", 10], ["love", "low", 20], ["love", 5],
         ["love", 10], ["love", 15], ["love", 20], ["love", 25]]
print(checkr(inst2, vals2))
# expected1 = [null, null, "bar", "bar", null, "bar2", "bar2"]
# expected2 = [null,null,null,null,"high","high","low","low"]
