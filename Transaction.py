
class Transaction():

        def __init__(self, tid=None, state=None, itemsLocked=[], timeStamp=None):
                self.tid = tid
                self.state = state
                self.itemsLocked = itemsLocked
                self.timeStamp = timeStamp
