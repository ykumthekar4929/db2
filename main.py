import os
import sys
import DataHandler as DH
from Transaction import Transaction
from Lock import Lock

class DBMan():
        TransactionTable = {}
        LockTable = {}
        OperationsTable = []

        transaction_ts = 0

        def __init__(self, OperationsTable):
                self.OperationsTable = OperationsTable


        def __begin(self, op):
                # Begin Case
                self.transaction_ts = self.transaction_ts + 1
                curr_transaction = Transaction(op.tid, "ACTIVE", [], self.transaction_ts)
                self.TransactionTable.update({
                        curr_transaction.tid:curr_transaction
                })

        def __read(self, op):
                # Read Case
                if (self.TransactionTable[op.tid].state == "BLOCKED"):
                        # Append currentOperation to LockTable.itemName.waitingOperations
                        print "Transaction blocked already"
                elif (self.TransactionTable[op.tid].state == "ABORTED"):
                        print "Transaction already aborted"
                        pass
                else:
                        if self.LockTable.has_key(op.itemName):
                                print "%s already %s locked by T%s"%(op.itemName, self.LockTable[op.itemName].lockState,
                                        self.LockTable[op.itemName].readlockedTIDS)
                                if self.LockTable[op.itemName].lockState == "READ":
                                        print "Allow for shared lock"
                                        # Read Lock Here
                                else:
                                        print "Handle Wait Dies"

                        else:
                                # Generate new LockTable record with READ lock
                                print "Creating new READ LockTable Record for %s"%op.itemName
                                new_lock = Lock(itemName=op.itemName, lockState="READ", readLockedTIDS=[op.tid], \
                                                        writeLockTID=None, waitingOperations=[])
                                self.LockTable.update({
                                        op.itemName:new_lock
                                })
                                # Read Lock Here


        def __write(self, op):
                if (self.TransactionTable[op.tid].state == "BLOCKED"):
                        # Append currentOperation to LockTable.itemName.waitingOperations
                        print "Transaction blocked already"
                elif (self.TransactionTable[op.tid].state == "ABORTED"):
                        print "Transaction already aborted"
                        pass
                else:
                        if self.LockTable.has_key(op.itemName):
                                print "Write conflict occurred handle wait die"
                        else:
                                # Handle blind write here ?
                                print "Creating new WRITE LockTable Record for %s"%op.itemName
                                new_lock = Lock(itemName=op.itemName, lockState="WRITE", readLockedTIDS=[], \
                                                        writeLockTID=op.tid, waitingOperations=[])
                                self.LockTable.update({
                                        op.itemName:new_lock
                                })
                                # Write Lock Here
        def __end(self, op):
                # print "End %s"%op.tid
                pass


        actions  = {
                "b":__begin,
                "r":__read,
                "w":__write,
                "e":__end

        }

        def execute(self):
                for op in self.OperationsTable:
                        self.actions[op.method](self, op)

                print "Done executing"




def main(args):
        filename = args[1]
        OperationsTable = DH.make_operations(filename)
        DBMan(OperationsTable).execute()

if __name__ == '__main__':
        main(sys.argv)
