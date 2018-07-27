# class Lock(itemName, lockState, readLockedTIDS)

class Lock():

        """docstring for Lock"""

        def __init__(self, itemName=None, lockState=None, readLockedTIDS=[], \
                                writeLockTID=None, waitingOperations=[]):

                self.itemName = itemName
                self.lockState = lockState
                self.writeLockTID = writeLockTID
                self.readlockedTIDS = readLockedTIDS
                self.waitingOperations = waitingOperations

        def __str__(self):
                return "Lock State: %s  write locked transaction : %s  read locked transactions: %s  waiting operations: %s" %(self.lockState, self.writeLockTID, self.readlockedTIDS, self.waitingOperations)

        def __repr__(self):
                return str({
                        "Item name" : self.itemName,  "Lock State": self.lockState,  "write locked transaction" : self.writeLockTID,  "read locked transactions": self.readlockedTIDS,  "waiting operations":self.waitingOperations
                })
