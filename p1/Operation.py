class Operation():

        def __init__(self, tid=None, method=None, itemName=None):
                # super(Operation, self).__init__()
                self.tid = tid
                self.method = method
                self.itemName = itemName

        def __str__(self):
                return "%s (%s)"%(self.method, self.tid)

        def __repr__(self):
                return "%s (%s)"%(self.method, self.tid)
