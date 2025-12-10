OS Project 3

How to run the project:
- There are 6 commands the user can choose from
- Create Command: Creates a file with 512 bytes per size of block with magic number, root block id, and next block id in the header block 0. Also has input error checking
- Insert Command: This is the most important command since it has the split logic and the inserting logic behind it which is later used by load. This command basically takes in the insert key, value given by the user and inserts it into the 152 bytes of keys, initially it only fills it up till 19 keys then after that it splits the nodes into root node, and 2 child nodes. The inserting logic works by incrementing the number of keys inserted already by 1 each time a key,value is inserted and that number of keys then using that number of keys we know the placement of the upcoming key and its value. The 2 level for b-tree split works so whenever the number of keys reachs the max of 19 it splits into root node, and 2 child nodes (left and right) and the middle key goes to the root node and every key less than that whch will be half of the 19 goes to the left child and the other half goes to the right child. Also has input error checking
- Search Command: This is also another most important command since it searches for the key and its value in the nodes and prints it out. Also has input error checking
- Load Command: This is very useful for debugging perposes since inserting more than 19 keys would take a lot of time so if we just use load it will fill it up automatically. Also has input error checking
- Print command: This command is used to print out the current key, and values in the nodes right now
- Extract command: This command is used similarly to the print where it just writes out all of the keys and their respected values to a .csv file given by the user. Also has input error checking

Learned & Challenges
- One of the main issues I had was time constraints since I also had finals, projects, homeworks, and presentations I was on a time contstraint and talked to the professor in office hours and this is where prfoessor salazar gave me advice and told me that I could also use bytearray or a node class to make it much more easier but since I was in time constraint I ended up just using my approach.

Demonstration & Understanding (This is already mentioned in one of my devlog commits, but I'm still writing it here in case the TA misses it):
I understand that B-trees split when the nodes have reached their maximum key capacity and in our case its 19 keys so if the user wants to add any key after that the node will split into root, and 2 child nodes with the middle key going to the root and the rest getting divided into elft and right child nodes
Since i implemented the 2 level b-tree it shows that my Understanding of b-tree is pretty sharp and I understand how b-tree works 
Also as mentioned in the pdf, I made sure that not to load everything into memory and only use 3 nodes at a time which I did 
And I have also learned about big endian encoding in python, block based storage in idx files, and file growth
For the sorted concept I wasn't able to properly implement this correctly since while I did try to sort it I had some issues with my output which ended up breaking the entire code so unfortunately I had to remove that feature
If I had more time to work on this and in the future, I will implement the b-tree recursively so any node can split not just the root node up til the 2 leveland I will also sort the b-tree by using bubble or insertion sort
I would also test the code with 50+ keys to see if it properly manages the b-tree or not
I have also done very good documentation of my progress for this past 10 days