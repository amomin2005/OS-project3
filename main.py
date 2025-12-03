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
            file = open(idxfile, 'rb')
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
            #rest of unused space are 488 bytes 
            num = 0
            file.write((num.to_bytes(8, 'big')) * 488)

            #block 1 512 bytes
            file.write((num.to_bytes(8, 'big')) * 512)

    elif sys.argv[1] == "insert" and len(sys.argv) == 5:
        key = int(sys.argv[3])
        val = int(sys.argv[4])
        print("Key: " + str(key))
        print("Value: " + str(val))
        print("Insert")
    elif sys.argv[1] == "search" and len(sys.argv) == 4:
        print("Searching the value for key " + sys.argv[3])
    elif sys.argv[1] == "load":
        print("Load")
    elif sys.argv[1] == "extract":
        print("Extract")
    elif sys.argv[1] == "print":
        print("print")
    else:
        print("Unknown command, please choose from :create, insert, search, load, print, extract (then write filename)")
        return
main()