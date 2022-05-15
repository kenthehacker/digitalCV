# CSE330
kenichi matsuo 474521 kenthehacker  

Eric Tseng - 475576 - ertseng2000  


Creative Portion:
1) Liking feature
We took the inspiration from facebook's like feature when one is DM'ing someone on facebook messenger app.
what we did is that we took a heart from google images and added a like button. if a user likes a message that
they have read then they can send in the chat the heart emoji. the way that we did this is that we've created an image
src HTML tag. the information about whether someone liked an message will be sent over to the server when the user
hits the like button which sends a socket to the server which then sends a socket query to the clients who are in
the same chat. then for each of the users that are in the same chat as the sender will receive the heart emoji as well

2) We took a page out of skype's admin functionality. This was quite annoying to implement. What we did is that if a
person already knew the username of the admin, they could enter in the admin username and it'll give them unlimited
power to kick/ban and join any room without a password if they wish.  The admin username in this case is t00root.


## Grading
 - -1: warning in validator
 - -0.5: no .gitignore file
 - -1: communication requires typing different commands
 - -3: admin fails to kick or ban users from room
