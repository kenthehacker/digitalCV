#### no.1
Kenichi Matsuo 

#### no.2
n/a no question

#### no.3
n/a no question

#### no.4
n/a no question

#### no.5
n/a no question

#### no.6 Server Design
the server first recieves the text file holding the original fragment file name
as well as the different fragment file
it parses the spec file line by line stores the title of the 
spec files in a char array dynamically. afterwards, it also 
goes through the names of the spec files and stores that into a file * array
dynamically. furthermore, it does another loop to create a 1d array 
to store the contents of those file * into a dynamically allocated array

it then creates a server socket and when a cli socket is established itll send
the char buf over to cli. when there is data to be read from a cli socket
itll store it into a Binary tree. the cli also stores the unordered
fragments from server in a binary tree
the BST makes everything easier to handle while sacraficing worst case
scenario time complexity since an inorder traversal easily guaruntees 
sorted order

#### no.7 
n/a no question

#### no.8
this was already answered as to why i used BST for both cli and server 
tldr: easier to implement inorder traversal guaruntees sorted order

#### no.9
n/a no question

#### no.10 Client design
the cli first establishes socket connection to server. using poll, itll wait until
it has data to be read. the data is parsed line by line and each line
is stored into a BST based on its line number. 
once it finishes reading all of the messages from the server itll send it back 
via inorder traversal 
once that is finished itll close the socket communication

#### no.11 Testing and Evaluation
I just ran a couple different text files and verified that it worked. 
there was an issue where i had a heap corruption error on my server program
when i was reading from the client socket this happened because i set every 
single node's char buffer CHAR_BUF size but i changed it to be char * buf 
instead

#### no.12 Development Effort
about 15-20 hours 






