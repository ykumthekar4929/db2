# class Lock(itemName, lockState, readLockedTIDS)

class Lock():

        """docstring for Lock"""

        def __init__(self, itemName=None, lockState=None, readLockedTIDS=[], \
                                writeLockTID=None, waitingOperations=[]):

                self.itemName = itemName
                self.lockState = lockState
                self.writeLockTID = writeLockTID
                self.readlockedTIDS = readLockedTIDS
                self.watingOperations = waitingOperations
