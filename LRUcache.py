class CachedItem:
    # a dbly linked list node
    def __init__(self, key, value):
        self.next = None
        self.prev = None
        self.val = value
        self.key = key


class LRUCache:
    def __init__(self, capacity: int):
        self.hash = {}
        self.capacity = capacity
        self.head = None  # will be head node of list
        self.tail = None  # will be tail node of list

    def get(self, key: int) -> int:
        if key in self.hash:
            # the value of the hashmap will be a CachedItem node, so get .val attrib
            # AND move the targ to the head while patching it's prior position in the list
            targ = self.hash[key]
            if targ.prev == None:
                # it's already the head, just return it
                return targ.val
            else:
                targ_lf_neighbor = targ.prev
            if targ.next == None:
                # it's already the tail
                targ_lf_neighbor.next = None
                self.tail = targ_lf_neighbor
            else:
                targ_rt_neighbor = targ.next
                targ_rt_neighbor.prev = targ_lf_neighbor
                if targ_rt_neighbor.next == None:
                    self.tail = targ_rt_neighbor
            targ.prev = None
            targ.next = self.head
            self.head.prev = targ
            self.head = targ

            return self.hash[key].val
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        new_node = CachedItem(key, value)
        if self.capacity == 1 and len(self.hash) == 1:
            # this is a special case where the item is always the head and the tail
            self.hash.pop(self.head.key)
            self.head = new_node
            self.tail = new_node
            self.hash[key] = new_node
            return

        # need to evict the old
        if key not in self.hash and len(self.hash) >= self.capacity:
            # removes tail from hash, returns it for some link updating
            old_tail = self.hash.pop(self.tail.key)
            new_tail = old_tail.prev
            old_tail.prev = None
            new_tail.next = None
            self.tail = new_tail
        # then we just ADDING the new item (after evicting as needed)
        if self.head:
            head = self.head
            head.prev = new_node
            new_node.next = head
        if not self.tail:  # no tail yet...
            self.tail = new_node
        self.hash[key] = new_node
        self.head = new_node

        # Your LRUCache object will be instantiated and called as such:
        # obj = LRUCache(capacity)
        # param_1 = obj.get(key)
        # obj.put(key,value)


def test_it(instructions, vals):
    out = []
    for i, n in enumerate(instructions):  # skipping the init step
        if i == 0:
            cap = vals[i][0]
            cache = LRUCache(cap)
            out.append(None)
            continue
        if n == "put":
            k, v = vals[i]
            cache.put(k, v)
            out.append(None)
        else:  # a "get"
            k = vals[i][0]
            res = cache.get(k)
            out.append(res)
    return out


# print(test_it(["LRUCache", "put", "put", "get",
#      "put", "get", "put", "get", "get", "get"], [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]))
print(test_it(["LRUCache", "put", "get", "put", "get", "get"],
      [[1], [2, 1], [2], [3, 2], [2], [3]]))
