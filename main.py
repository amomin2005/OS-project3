### JUST FOR INFO STUFF
# ---------------------------------------------HEADER
# 8-bytes: The magic number “4348PRJ3” (as a sequence of ASCII values).
# 8-bytes: The id of the block containing the root node. This field is zero if the tree is empty.
# 8-bytes: The id of the next block to be added to the file. This is the next location for a new node.
# Rhe remaining bytes are unused.
# ---------------------------------------------Block 0
# 8-bytes: The block id this node is stored in.
# 8-bytes: The block id this nodes parent is located. If this node is the root, then this field is zero.
# 8-bytes: Number of key/value pairs currently in this node.
# 152-bytes: A sequence of 19 64-bit keys
# 152-bytes: A sequence of 19 64-bit values
# 160-bytes: A sequence of 20 64-bit offsets. These block ids are the child pointers for this node. If a child is a leaf node, the corresponding id will be zero.
# Remaining bytes are unused

# 25 + (19*8) = 175 is where val start

import sys
import os.path

def main():
    # just checking test.idx by prof
    
    if len(sys.argv) < 2:
        print("Not enough commands. please write commands and the filename after python main.py")
        return
    
    idxfile = sys.argv[2]
    # print(bytes([0, 1]))
    if sys.argv[1] == "create" and len(sys.argv) == 3:
        # write to the binary file (write binary)
        # header which will have magic number, root block id, next block id, and free space
        if os.path.exists(idxfile):
            file = open('index.idx', 'rb')
            print(file.read())
            file.close()
            print("File already exists")
            return
        else:
            print("File doesn't exists already so we just created it")
            # header
            file = open(idxfile, 'wb')
            # magic number is 8 bytes
            file.write(b'4348PRJ3')
            # root block id is 8 bytes (Root block ID = 0)
            rootblockid = 0
            file.write(rootblockid.to_bytes(8, 'big'))
            # next block 1d is 8 bytes (Next block ID = 1)
            nextblockid = 1
            file.write(nextblockid.to_bytes(8, 'big'))
            #rest of space are 488 bytes 
            num = 0
            file.write((num.to_bytes(8, 'big')) * 488)

            #block 1 512 bytes
            file.write((num.to_bytes(8, 'big')) * 512)

    elif sys.argv[1] == "insert" and len(sys.argv) == 5:
        key = int(sys.argv[3])
        val = int(sys.argv[4])
        file = open(idxfile, 'r+b')
        file.seek(8)
        rootnodeblockid = int.from_bytes(file.read(8), 'big')
        # if root is empty then increment the block id to 1 as the root and 2 as the next and write key,val
        if rootnodeblockid == 0:
            file.seek(512)
            print("Root node is empty and is on Block 0 currently before entering the key,val")
            # BLOCK ID = 1
            blockid = 1
            file.write(blockid.to_bytes(8, 'big'))
            # Parent = 0
            parentid = 0
            file.write(parentid.to_bytes(8, 'big'))
            # Num Key = 1
            countkey = 1
            file.write(countkey.to_bytes(8, 'big'))
            file.seek(512 + 8 + 8 + 8 + (0 * 8))
            file.write(key.to_bytes(8, 'big'))
            file.seek(512 + 8 + 8 + 8 + 152 + (0 * 8))
            file.write(val.to_bytes(8, 'big'))
            # changes to 1 since root node only 0 when empty
            # 512 + 152bytes for the keys
            # 512 + 152bytes for the values
            # 512 + 160bytes for child pointers 
            # child pointer 0 is the left pointer of Parent 0
            # child pointer 1 is the right pointer of Parent 0
            # unused space

            update = 1
            file.seek(8)
            file.write(update.to_bytes(8, 'big'))
            updatenext = 2
            file.seek(16)
            file.write(updatenext.to_bytes(8, 'big'))
        else:
            file.seek(rootnodeblockid * 512 + 8 + 8)
            cur = int.from_bytes(file.read(8), 'big')
            # as long as it is under 19 it will do it then i will implmenet the split feature
            if (cur + 1) <= 19:
                print("Root node is not empty and currently we are on Block 1 and the header is on Block 0 and the next Block ID is 2")
                file.seek(512 + 8 + 8 + 8 + (cur * 8))
                file.write(key.to_bytes(8, 'big'))
                file.seek(512 + 8 + 8 + 8 + 152 + (cur * 8))
                file.write(val.to_bytes(8, 'big'))
                countkey = cur + 1
                file.seek(rootnodeblockid * 512 + 8 + 8)
                file.write(countkey.to_bytes(8, 'big'))
            else:
                print("FULL")

        # file.seek(512 + 8 + 8 + 8 + (countkey * 8))
        # print(int.from_bytes(file.read(8), 'big'))
        # file.seek(512 + 176 + (countkey * 8))
        # file.write(val.to_bytes(8, 'big'))
        # file.seek(512 + 176 + (countkey * 8))
        # print(int.from_bytes(file.read(8), 'big'))
        

    elif sys.argv[1] == "search" and len(sys.argv) == 4:
        print("Searching the value for key " + sys.argv[3])
    elif sys.argv[1] == "load":
        print("Load")
    elif sys.argv[1] == "extract":
        print("Extract")
    elif sys.argv[1] == "print":
        file = open(idxfile, 'rb')
        file.seek(512 + 8 + 8)
        a = []
        v = []
        countkey = int.from_bytes(file.read(8), 'big')
        print(countkey)
        for i in range(countkey):
            file.seek(512 + 24 + (i * 8))
            key = int.from_bytes(file.read(8), 'big')
            a.append(key)
            file.seek(512 + 152 + 8 + 8 + 8 + (i * 8))
            value = int.from_bytes(file.read(8), 'big')
            v.append(value)
            print("key: " + str(a[i]) + " Value: " + str(v[i]))
    else:
        print("Unknown command, please choose from :create, insert, search, load, print, extract (then write filename)")
        return
main()