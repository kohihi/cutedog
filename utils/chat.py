class Counter(object):
    def __init__(self):
        self.current = 0

    def plus(self, num=1):
        self.current += num
        if self.current < 0:
            self.current = 0


class IDPull(object):
    def __init__(self, number):
        self._pull = ["0"+str(i) if i < 10 else str(i) for i in range(number)]
        self._sid_dict = {}

    def query(self):
        if len(self._pull) > 0:
            return self._pull.pop(0)
        else:
            return False

    def set(self, index, sid):
        self._sid_dict[sid] = index

    def freed(self, sid):
        if self._sid_dict.get(sid, None) is None:
            return None
        index = self._sid_dict.pop(sid)
        self._pull.append(index)
        return index

    def get(self, sid):
        return self._sid_dict.get(sid)
