# CSE330
Kenichi Matsuo 474521 kenthehacker
URL to Ken:
http://ec2-18-223-205-149.us-east-2.compute.amazonaws.com/~kk/module5/calendar.html

Eric Tseng 475576 ertseng2000
http://ec2-3-22-166-133.us-east-2.compute.amazonaws.com/module5/calendar.html


Creative Portion:
1) Sharing with friend:
User will click on the button on the bottom right to share with a friend and populate the text box cell with the
username of their friends that they want to share the event with. All of that part happens on the JS side. Then JS
makes an AJAX call to PHP with the eventID and the userName and PHP will check SQL table to see if the UserName is correct
if it is correct then it attempts to append the event into the SQL table with that friend's username being different
all else being identical
if everything went according to plan, php will send a confirmation number to JS and on JS it checks if the
number indicated a success if so it'll alert a success message to the user.  
Our share event feature intentionally copies the event to the other user's calendar. We believe this feature should be worth five points based on the amount of work and time devoted.

2) Check for upcoming events within the next hour alerts:
If an event is happening within the next hour then the app will make an alert warning user
of the near upcoming events. At the beginning calendar will make AJAX call to PHP by sending the current
day, hour, minute, year, and month VIA JSON
JSON is then decoded in PHP
We then pull every event from SQL that happens that day and matches the username. Looping through all of the events,
if any of the events are happening within the hour it'll append the title of the event to a LinkedList
The LL is then JSON encoded and sent back to JS where it'll loop through the list and make an alert for each of them
To test this, just make an event within the next hour then log out then log back in
it wouldn't make sense to alert the moment you make an event since you already know that its happening within the
next hour. It's only when user logs in.

3) Bitcoin price data is being pulled from the Binance websocket API. We update the prices continuously with an event
listener. When the new price is fetched it updates the HTML script letting the user know what the price of bitcoin is
This section is inspired by many applications that tells us what the stock prices are when we log into our
devices in the morning, kind of like how the iPhone tells me that $SPY is going to reach 500 soon
