# CSE330
Eric Tseng - 475576 - ertseng2000  
Kenichi Matsuo - 474521 - kenthehacker


Link to Ken's website:

http://ec2-18-223-205-149.us-east-2.compute.amazonaws.com/Module2/login.php

Link to Eric's website:

http://ec2-3-22-166-133.us-east-2.compute.amazonaws.com/module2/login.php


CREATIVE PORTION:
We added the capability of being able to add a new user onto the website, this was quite difficult since we'd needed to have to be able to append the new user onto the userName.txt as well as auto-generating the new user directories. This began to mess with our code but we did it!!  

While we were at it, we decided to develop a feature that will allow the user to delete their account.  This removes all files in their account and deletes their folder from the file system.

How it works:
- User clicks on button saying they want to add new user, takes them to addNewUser.php
- User when user submits their new username, the php redirects them to log-in php script
- At every time the log-in php script is ran, it loops through every line in newUser.txt and if the userDir doesn't exist, it'll mkdir
- It sets the cwd then to "../Module2/<USERNAME>"  

LOGIN Details:
our default usernames are:
kenthehacker OR ericthehacker OR test

otherwise just make a new account
  
### Grading:
-1.5: Missing filter input. Ex: $userName = $_POST["newUserName"];
