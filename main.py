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

import csv
import sys
import os.path


def insert(file, key, val):
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
            file.seek(8)
            c = int.from_bytes(file.read(8), 'big')
            c += 1
            file.seek(8)
            file.write(c.to_bytes(8, 'big'))
            file.seek(16)
            m = int.from_bytes(file.read(8), 'big')
            m += 1
            file.seek(16)
            file.write(m.to_bytes(8, 'big'))
            # parent
            file.seek(512 + 16)
            k = []
            v = []
            countkey = int.from_bytes(file.read(8), 'big')
            for i in range(countkey):
                file.seek(512 + 24 + (i * 8))
                key = int.from_bytes(file.read(8), 'big')
                k.append(key)
                file.seek(512 + 152 + 16 + 8 + (i * 8))
                value = int.from_bytes(file.read(8), 'big')
                v.append(value)
            file.seek(512 + 8)
            zero = 0
            for i in range(512):
                file.write(zero.to_bytes(8, 'big'))
            file.seek(512 + 8 + 8)
            one = 1
            file.write(one.to_bytes(8, 'big'))
            mid = len(k) // 2
            file.seek(512 + 24)
            file.write(k[mid].to_bytes(8, 'big'))
            file.seek(512 + 152 + 24)
            file.write(v[mid].to_bytes(8, 'big'))
            file.seek(512 + 152 + 152 + 24)
            childpointer = 2
            childpointer2 = 3
            file.write(childpointer.to_bytes(8, 'big'))
            file.write(childpointer2.to_bytes(8, 'big'))
            #left
            file.seek(512 + 512)
            for i in range(512):
                file.write(zero.to_bytes(8, 'big'))
            file.seek(512 + 512)
            blockid = 2
            parentid = 1
            file.write(blockid.to_bytes(8, 'big'))
            file.write(parentid.to_bytes(8, 'big'))
            file.write((9).to_bytes(8, 'big'))
            file.seek(512 + 512 + 24)
            for i in range(mid):
                file.write(k[i].to_bytes(8, 'big'))
                print(k[i])
            file.seek(512 + 512 + 24 + 152)
            for i in range(mid):
                file.write(v[i].to_bytes(8, 'big'))
                print(v[i])

            #right
            file.seek(512 + 512 + 512)
            for i in range(512):
                file.write(zero.to_bytes(8, 'big'))
            file.seek(512 + 512 + 512)
            blockidr = 3
            parentidr = 1
            file.write(blockidr.to_bytes(8, 'big'))
            file.write(parentidr.to_bytes(8, 'big'))
            file.write(mid.to_bytes(8, 'big'))
            file.seek(512 + 512 + 512 + 24)
            for i in range(mid + 1, len(k)):
                file.write(k[i].to_bytes(8, 'big'))
                print(k[i])
            file.seek(512 + 512 + 512 + 24 + 152)
            for i in range(mid + 1, len(k)):
                file.write(v[i].to_bytes(8, 'big'))
                print(v[i])    
    
    file.close()

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
        
        file.close()

    elif sys.argv[1] == "insert" and len(sys.argv) == 5:
        key = int(sys.argv[3])
        val = int(sys.argv[4])
        if os.path.exists(idxfile):
            file = open(idxfile, 'r+b')
            insert(file, key, val)
            return
        else:
            print("File doesn't exist")
        # file.seek(512 + 8 + 8 + 8 + (countkey * 8))
        # print(int.from_bytes(file.read(8), 'big'))
        # file.seek(512 + 176 + (countkey * 8))
        # file.write(val.to_bytes(8, 'big'))
        # file.seek(512 + 176 + (countkey * 8))
        # print(int.from_bytes(file.read(8), 'big'))
        

    elif sys.argv[1] == "search" and len(sys.argv) == 4:
        searchingkey = int(sys.argv[3])
        if os.path.exists(idxfile):
            file = open(idxfile, 'rb')
            file.seek(512 + 512 + 8 + 8)
            countkey = int.from_bytes(file.read(8), 'big')
            file.seek(512 + 512 + 8 + 8 + 8)
            for i in range(countkey):
                currentkey = int.from_bytes(file.read(8), 'big')
                if currentkey == searchingkey:
                    file.seek(512 + 512 + 176 + (i * 8))
                    found = int.from_bytes(file.read(8), 'big')
                    print(str(currentkey) + "," + str(found))
            
            searchingkey = int(sys.argv[3])
            file = open(idxfile, 'rb')
            file.seek(512 + 8 + 8)
            countkey = int.from_bytes(file.read(8), 'big')
            file.seek(512 + 8 + 8 + 8)
            for i in range(countkey):
                currentkey = int.from_bytes(file.read(8), 'big')
                if currentkey == searchingkey:
                    file.seek(512 + 176 + (i * 8))
                    found = int.from_bytes(file.read(8), 'big')
                    print(str(currentkey) + "," + str(found))

            file.seek(512 + 512 + 512 + 8 + 8)
            countkey2 = int.from_bytes(file.read(8), 'big')
            file.seek(512 + 512 + 512 + 8 + 8 + 8)
            for i in range(countkey2):
                currentkey2 = int.from_bytes(file.read(8), 'big')
                if currentkey2 == searchingkey:
                    file.seek(512 + 512 + 512 + 176 + (i * 8))
                    found2 = int.from_bytes(file.read(8), 'big')
                    print(str(currentkey2) + "," + str(found2))
            
            file.close()
            return
        else:
            print("File doesn't exist")
        
    elif sys.argv[1] == "load":
        e = sys.argv[3]
        if os.path.exists(idxfile) and os.path.exists(e):
            excelfile = open(e, 'r')
            file = open(idxfile, 'wb')
            reading = csv.reader(excelfile)
            for i in reading:
                key = int(i[0])
                val = int(i[1])
                file = open(idxfile, 'r+b')
                insert(file, key,val)
            file.close()
            excelfile.close()
        elif sys.argv[1] == "extract":
            e = sys.argv[3]
            excelfile = open(e, 'w')
            file = open(idxfile, 'rb')
            file.seek(512 + 512 + 16)
            a1 = []
            v1 = []
            countkey = int.from_bytes(file.read(8), 'big')
            for i in range(countkey):
                file.seek(512 + 512+ 24 + (i * 8))
                key = int.from_bytes(file.read(8), 'big')
                a1.append(key)
                file.seek(512 + 512+ 152 + 16 + 8 + (i * 8))
                value = int.from_bytes(file.read(8), 'big')
                v1.append(value)
                excelfile.write(str(a1[i]) + "," + str(v1[i]))
                excelfile.write("\n")

            file.seek(512 + 16)
            a = []
            v = []
            countkey = int.from_bytes(file.read(8), 'big')
            for i in range(countkey):
                file.seek(512 + 24 + (i * 8))
                key = int.from_bytes(file.read(8), 'big')
                a.append(key)
                file.seek(512 + 152 + 16 + 8 + (i * 8))
                value = int.from_bytes(file.read(8), 'big')
                v.append(value)
                excelfile.write(str(a[i]) + "," + str(v[i]))
                excelfile.write("\n")
            
            
            file.seek(512 + 512 + 512 + 16)
            a2 = []
            v2 = []
            countkey = int.from_bytes(file.read(8), 'big')
            for i in range(countkey):
                file.seek(512 + 512 + 512 + 24 + (i * 8))
                key = int.from_bytes(file.read(8), 'big')
                a2.append(key)
                file.seek(512 + 512 + 512 + 152 + 16 + 8 + (i * 8))
                value = int.from_bytes(file.read(8), 'big')
                v2.append(value)
                excelfile.write(str(a2[i]) + "," + str(v2[i]))
                excelfile.write("\n")
            file.close()
            excelfile.close()
            return
        else:
            print("File doesn't exist")
        
    elif sys.argv[1] == "print":

        if os.path.exists(idxfile):
            file = open(idxfile, 'rb')
            file.seek(512 + 512 + 16)
            a1 = []
            v1 = []
            countkey = int.from_bytes(file.read(8), 'big')
            for i in range(countkey):
                file.seek(512 + 512+ 24 + (i * 8))
                key = int.from_bytes(file.read(8), 'big')
                a1.append(key)
                file.seek(512 + 512+ 152 + 16 + 8 + (i * 8))
                value = int.from_bytes(file.read(8), 'big')
                v1.append(value)
                print(str(a1[i]) + "," + str(v1[i]))
            
            file.seek(512 + 16)
            a = []
            v = []
            countkey = int.from_bytes(file.read(8), 'big')
            for i in range(countkey):
                file.seek(512 + 24 + (i * 8))
                key = int.from_bytes(file.read(8), 'big')
                a.append(key)
                file.seek(512 + 152 + 16 + 8 + (i * 8))
                value = int.from_bytes(file.read(8), 'big')
                v.append(value)
                print(str(a[i]) + "," + str(v[i]))
            

            file.seek(512 + 512 + 512 + 16)
            a2 = []
            v2 = []
            countkey = int.from_bytes(file.read(8), 'big')
            for i in range(countkey):
                file.seek(512 + 512 + 512 + 24 + (i * 8))
                key = int.from_bytes(file.read(8), 'big')
                a2.append(key)
                file.seek(512 + 512 + 512 + 152 + 16 + 8 + (i * 8))
                value = int.from_bytes(file.read(8), 'big')
                v2.append(value)
                print(str(a2[i]) + "," + str(v2[i]))
            
            file.close()
            return
        else:
            print("File doesn't exist")
    else:
        print("Unknown command, please choose from :create, insert, search, load, print, extract (then write filename)")
        return
main()