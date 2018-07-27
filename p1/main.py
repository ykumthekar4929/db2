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
                self.transaction_ts = self.transaction_ts + 1
                curr_transaction = Transaction(op.tid, "ACTIVE", [], self.transaction_ts)
                self.TransactionTable.update({
                        curr_transaction.tid:curr_transaction
                })
                print "Begin T%s"%op.tid

        def __read(self, op):
                if (self.TransactionTable[op.tid].state == "BLOCKED"):
                        self.LockTable[op.itemName].waitingOperations.append(op)
                        print "Transaction blocked already"
                elif (self.TransactionTable[op.tid].state == "ABORTED"):
                        print "Transaction already aborted"
                else:
                        if self.LockTable.has_key(op.itemName):
                                # print "%s already %s locked by T%s"%(op.itemName, self.LockTable[op.itemName].lockState, self.LockTable[op.itemName].readlockedTIDS)
                                if self.LockTable[op.itemName].lockState == "WRITE":
                                        print "Handle Wait Dies"
                                        self.handleWaitDie(op, self.LockTable[op.itemName].writeLockTID)
                                        
                                else:
                                        print "T%s readlocks %s"%(op.tid,op.itemName)
                                        self.readLock(op)

                        else:
                                print "T%s readlocks %s"%(op.tid,op.itemName)
                                new_lock = Lock(itemName=op.itemName, lockState="READ",
                                                                readLockedTIDS=[op.tid],
                                                                writeLockTID=None, waitingOperations=[])
                                self.LockTable.update({
                                        op.itemName:new_lock
                                })
                                self.readLock(op)

        def readLock(self, op):
                '''
                        readLock(tid, itemName)
                                append itemName to TransactionTable.tid.itemsLocked
                                Update LockTable.itemName.lockState="Read"
                                Append tid to LockTable.itemName.readLockedTIDS
                '''
                self.LockTable[op.itemName].lockState = "READ"
                if not op.tid in self.LockTable[op.itemName].readlockedTIDS:
                        self.LockTable[op.itemName].readlockedTIDS.append(op.tid)
                if not op.itemName in self.TransactionTable[op.tid].itemsLocked:
                        self.TransactionTable[op.tid].itemsLocked.append(op.itemName)



        def __write(self, op):
        
                if (self.TransactionTable[op.tid].state == "BLOCKED"):
                        self.LockTable[op.itemName].waitingOperations.append(op)
                        print "Transaction blocked already"
                elif (self.TransactionTable[op.tid].state == "ABORTED"):
                        print "Transaction already aborted"
                        
                else:
                        if self.LockTable.has_key(op.itemName):
                                #import ipdb; ipdb.set_trace()
                                if self.LockTable[op.itemName].readlockedTIDS:
                                        for _tid in self.LockTable[op.itemName].readlockedTIDS:
                                                if op.tid == _tid:
                                                        self.updateLock(op)
                                                else:
                                                        self.handleWaitDie(op, _tid)
                                elif self.LockTable[op.itemName].writeLockTID is not None:
                                        self.handleWaitDie(op, self.LockTable[op.itemName].writeLockTID)
                                #print "Conflict situation"
                                else:
                                   self.writeLock(op)     
                        else:
                                print "Creating new WRITE LockTable Record for %s"%op.itemName
                                new_lock = Lock(itemName=op.itemName, lockState="WRITE",
                                                                readLockedTIDS=[], \
                                                                writeLockTID=op.tid, waitingOperations=[])
                                self.LockTable.update({
                                        op.itemName:new_lock
                                })
                                self.writeLock(op)

        def writeLock(self, op):
                '''
                        writeLock(tid, itemName):
                                Update LockTable.itemName.lockState = "Write"
                                append itemName to TransactionTable.tid.itemsLocked
                                Remove readlockedTIDS from the item if any
                                Add tid to LockTable.itemName.writeLockedTIDS
                '''
                
                self.LockTable[op.itemName].lockState = "WRITE"
                if not op.itemName in self.TransactionTable[op.tid].itemsLocked:
                        self.TransactionTable[op.tid].itemsLocked.append(op.itemName)
                del self.LockTable[op.itemName].readlockedTIDS[:]
                self.LockTable[op.itemName].writeLockTID = op.tid
                print "Write Locked %s for Transaction %s"%(op.itemName, op.tid)


        def updateLock(self, op):
                print "Updating lock on %s"%op.itemName
                self.writeLock(op)


        def __end(self, op):
                #print "End %s"%op.tid
                if self.TransactionTable[op.tid].state == "ABORTED":
                        print "Transaction %s already aborted"%(op.tid)
                        #self.abort(op)
                elif self.TransactionTable[op.tid].state == "ACTIVE":
                        print "Transaction %s committing"%(op.tid)
                        self.commit(op)
                elif self.TransactionTable[op.tid].state == "BLOCKED":
                        print "Transaction %s already blocked"%(op.tid)
                        self.abort(op)
                        
                


        def unlock(self, op, itemName):
                '''
                        Remove itemName from TransactionTable.tid.itemsLocked
                        If LockTable.itemName.waitingOperations is not empty
                                If waitingOperations[0].status == "Read"
                                        readLock(waitingOperations[0].tid, waitingOperations[0].itemName)
                                else
                                        writeLock(waitingOperations[0].tid, waitingOperations[0].itemName)
                                Update Transaction Table where TransactionTable.tid == waitingOperations[0].tid set TransactionTable.tid.status = "Active".
                                pop LockTable.itemName.waitingOperations[0]
                        Else:
                        Update LockTable.itemName.lockState = "None"
                        Update LockTable.itemName.writeLockTID = 0
                        If tid in LockTable.itemName.readLockTIDS pop
                '''
                print "Unlock %s"%itemName
                #self.TransactionTable[op.tid].itemsLocked.remove(itemName)
                if self.LockTable[itemName].waitingOperations:
                        if self.LockTable[itemName].waitingOperations[0].method == "r":
                                self.readLock(self.LockTable[itemName].waitingOperations[0])
                        elif self.LockTable[itemName].waitingOperations[0].method == "w":
                                self.writeLock(self.LockTable[itemName].waitingOperations[0])
                        self.TransactionTable[op.tid].state="ACTIVE"
                        self.LockTable[itemName].waitingOperations.pop(0)
                else:
                        self.LockTable[itemName].lockState = None
                        self.LockTable[itemName].writeLockTID = None
                        if op.tid in self.LockTable[itemName].readlockedTIDS:
                                self.LockTable[itemName].readlockedTIDS.remove(op.tid)


        def abort(self, op):
                '''
                        Update TransactionTable.tid.status = "ABORTED"
                        For item in TransactionTable.tid.itemsLocked:
                                Unlock(tid, item)
                        Remove all from TransactionTable.tid.itemsLocked
                '''
                self.endUpdate(op, "ABORTED")

        def commit(self, op):
                '''
                        Update TransactionTable.tid.status = "COMMITTED"
                        For item in TransactionTable.tid.itemsLocked:
                                Unlock(tid, item)
                        Remove all from TransactionTable.tid.itemsLocked
                '''
                self.endUpdate(op, "COMMITTED")


        def block(self, op):
                '''
                        Block(tid, operation):
                                Update TransactionTable.tid.status = "Blocked"
                                Append operation to LockTables.itemName.waitingOperations
                '''
                self.TransactionTable[op.tid].lockState = "BLOCKED"
                self.LockTable[op.itemName].waitingOperations.append(op)

        def endUpdate(self, op, status):
                '''
                        Update TransactionTable.tid.status = status
                        For item in TransactionTable.tid.itemsLocked:
                                Unlock(tid, item)
                        Remove all from TransactionTable.tid.itemsLocked
                '''
                self.TransactionTable[op.tid].state = status
                #import ipdb; ipdb.set_trace()
                print self.TransactionTable[op.tid].itemsLocked
                for item in self.TransactionTable[op.tid].itemsLocked:
                        self.unlock(op, item)
                        
                del self.TransactionTable[op.tid].itemsLocked[:]

        def handleWaitDie(self, req_op, conf_tid):
                '''
                        if TransactionTable.current_TID.timeStamp > TransactionTable.conflicting_TID.timeStamp
                                abort(current_TID)
                        else:
                                Block(current_tid, currentOperation)
                '''
                print "Checking wait-die conditions between T%s and T%s"%(req_op.tid, conf_tid)
                if self.TransactionTable[req_op.tid].timeStamp > self.TransactionTable[conf_tid].timeStamp:
                        # self.abort([x for x in self.OperationsTable if x.tid==req_tid][0])
                        print "Abort"
                        self.abort(req_op)
                else:
                        print "Wait"
                        self.block(req_op)


        actions  = {
                "b":__begin,
                "r":__read,
                "w":__write,
                "e":__end
        }

        def execute(self):
                for op in self.OperationsTable:
                        print "================================================================\n"
                        print "Current Operation %s %s (%s)\n"%(op.method, op.tid, op.itemName)
                        #import ipdb; ipdb.set_trace()
                        #print "Hello"
                        self.actions[op.method](self, op)
                print "Done executing"

def main(args):
        filename = args[1]
        OperationsTable = DH.make_operations(filename)
        DBMan(OperationsTable).execute()

if __name__ == '__main__':
        main(sys.argv)
