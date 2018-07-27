
class Transaction():

        def __init__(self, tid=None, state=None, itemsLocked=[], timeStamp=None):
                self.tid = tid
                self.state = state
                self.itemsLocked = itemsLocked
                self.timeStamp = timeStamp

        def __str__(self):
                # return "Transaction %s, state : %s, items locked : %s, time stamp: %s"%(self.tid, self.state, self.itemsLocked, self.timeStamp)
                return str( {
                        'Transaction' : self.tid,
                        'state':self.state,
                        "Items Locked":self.itemsLocked,
                        'timeStamp':self.timeStamp
                })


        def __repr__(self):
                return str( {
                        'Transaction' : self.tid,
                        'state':self.state,
                        'Items Locked' : self.itemsLocked,
                        'timeStamp':self.timeStamp
                })
