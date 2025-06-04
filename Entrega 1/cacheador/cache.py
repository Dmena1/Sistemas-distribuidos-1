from collections import OrderedDict, defaultdict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def stats(self):
        return {"hits": self.hits, "misses": self.misses, "size": len(self.cache), "policy": "LRU"}


class LFUCache:
    def __init__(self, capacity: int):
        self.cache = {}
        self.freq = defaultdict(int)
        self.capacity = capacity
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.cache:
            self.freq[key] += 1
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def put(self, key, value):
        self.cache[key] = value
        self.freq[key] += 1
        if len(self.cache) > self.capacity:
            menos_usado = min(self.freq, key=self.freq.get)
            del self.cache[menos_usado]
            del self.freq[menos_usado]

    def stats(self):
        return {"hits": self.hits, "misses": self.misses, "size": len(self.cache), "policy": "LFU"}
