import sys
import os.path

def main():
    # just checking test.idx by prof
    
    # file = open('test.idx', 'rb')
    # print(file.read())
    # file.close()
    # print("File already exists")
    if len(sys.argv) < 2:
        print("Not enough commands. please write commands and the filename after python main.py")
        return
    # print(bytes([0, 1]))
    if sys.argv[1] == "create" and len(sys.argv) == 3:
        idxfile = sys.argv[2]
        print("create")
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
        print("Print")
    else:
        print("Unknown command, please choose from :create, insert, search, load, print, extract (then write filename)")
        return
main()