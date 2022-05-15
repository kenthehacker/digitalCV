var users = {};
var chatRoom = {};
var godMode = "t00root";

// Require the packages we will use:
const http = require("http"),
    fs = require("fs");

const port = 3456;
const file = "client.html";
// Listen for HTTP connections.  This is essentially a miniature static file server that only serves our one file, client.html, on port 3456:
const server = http.createServer(function (req, res) {
    // This callback runs when a new connection is made to our HTTP server.

    fs.readFile(file, function (err, data) {
        // This callback runs when the client.html file has been read from the filesystem.
        if (err) return res.writeHead(500);
        res.writeHead(200);
        res.end(data);
    });
});
server.listen(port);

// Import Socket.IO and pass our HTTP server object to it.
const socketio = require("socket.io")(http, {
    wsEngine: 'ws'
});

// Attach our Socket.IO server to our HTTP server to listen
const io = socketio.listen(server);
io.sockets.on("connection", function (socket) {
    // This callback runs when a new Socket.IO connection is established.

    // Checks that the user ID is unique
    socket.on("loggedIn", function (data) {
      let id = socket.id;
      if (!(data.username in users)) {
        users[data.username] = id;
      }
      else {
        // Do something here that prevents user from entering chat screen w existing username
        console.log("login socket id error");
      }
    });

    // Has user leave chatrooms and log out.
    socket.on("loggedOut", function (data) {
      if (chatRoom[data.currentChatName] !== undefined) {
        const leaveIndex = chatRoom[data.currentChatName][0].indexOf(data.username);
        if (leaveIndex > -1) {
          chatRoom[data.currentChatName][0].splice(leaveIndex, 1);
          let leaveMessage = data.username + " left the room."
          io.in(data.currentChatName).emit("pushChatInfo", {users:chatRoom[data.currentChatName][0]});
          socket.to(data.currentChatName).emit("chatMsgToClient", {message: leaveMessage});
          socket.leave(data.currentChatName);
        }
      }
      delete users[data.username];
    });

    // Sends message back to clients in room
    socket.on("chatMsgToServer", function(data){
        var msgWithUser = data["username"]+": "+data["message"];
        io.in(data["chatName"]).emit("chatMsgToClient", {message: msgWithUser});
    });

    // Gets list of all chat rooms and sends to clients
    socket.on("getListOfChatNames", function(){
        var tempListOfChats = [];
        for (const [key, value] of Object.entries(chatRoom)) {
            tempListOfChats.push(key);
        }
        io.sockets.emit("returnListOfChatNames", {chatList: tempListOfChats});
    });

    // Works to create and automatically join a new room
    socket.on("makeRoom",function (data){
      if (chatRoom[data.chatName] === undefined) {
        if (chatRoom[data.currentChatName] !== undefined) {
          const leaveIndex = chatRoom[data.currentChatName][0].indexOf(data.userName);
          if (leaveIndex > -1) {
            chatRoom[data.currentChatName][0].splice(leaveIndex, 1);
            let leaveMessage = data.userName + " left the room."
            io.in(data.currentChatName).emit("pushChatInfo", {users:chatRoom[data.currentChatName][0]});
            socket.to(data.currentChatName).emit("chatMsgToClient", {message: leaveMessage});
            socket.leave(data.currentChatName);
          }
        }
        socket.join(data['chatName']);
        var chatName = data["chatName"];
        chatRoom[chatName] = [[],[],data["password"].trim(), data.userName];
        chatRoom[chatName][0].push(data['userName']); //appends current user into userList
        // admin/creator is set to chatroom[chatname][0][0] since that's the first person to be on that chat
        io.to(users[data.userName]).emit("newChatInfo", {chatName: data.chatName});
        io.in(data.chatName).emit("pushChatInfo", {users:chatRoom[chatName][0]});
      }
    });

    // Leaves current room and joins the new room
    socket.on("joinRoom", function(data){
      const dataPW = data["password"];
      const actualPW = chatRoom[data["chatName"]][2];
      if (actualPW == dataPW || data.userName == godMode){
        if (!chatRoom[data.chatName][1].includes(data.userName) && !chatRoom[data.chatName][0].includes(data.userName)) {
          if (chatRoom[data.currentChatName] !== undefined) {
            const leaveIndex = chatRoom[data.currentChatName][0].indexOf(data.userName);
            if (leaveIndex > -1) {
              chatRoom[data.currentChatName][0].splice(leaveIndex, 1);
              io.in(data.currentChatName).emit("pushChatInfo", {users:chatRoom[data.currentChatName][0]});
              socket.leave(data.currentChatName);
              let leaveMessage = data.userName + " left the room."
              socket.to(data.currentChatName).emit("chatMsgToClient", {message: leaveMessage});
            }
          }
          socket.join(data['chatName']);
          chatRoom[data.chatName][0].push(data.userName);
          var chatName = data["chatName"];
          var userName = data["userName"];
          var chatPW = data["password"];
          io.to(users[data.userName]).emit("newChatInfo", {chatName: data.chatName});
          io.in(data.chatName).emit("pushChatInfo", {users:chatRoom[chatName][0]});
        }
      }
      else {
        io.to(users[data.userName]).emit("wrongPW", {msg: "Wrong password!"});
      }
    });

    // Handles private messages between 2 clients
    socket.on("private_message", function (data) { // need to check if users are in the room
      if (users.hasOwnProperty(data.otherUser) && data.otherUser !== data.username && chatRoom[data.currentChatName][0].includes(data.otherUser) && chatRoom[data.currentChatName][0].includes(data.username)) {
        const sendID = users[data.otherUser];
        const ownID = users[data.username];
        data.username = "[PM] " + data.username + ": ";
        data.message = data.username + data.message;
        io.to(sendID).emit("chatMsgToClient", { message: data.message });
        io.to(ownID).emit("chatMsgToClient", { message: data.message });
      }
    });

    // Handles creator or admin kicking user
    socket.on("kick", function (data) {
      if (users.hasOwnProperty(data.otherUser) && data.otherUser !== data.username && chatRoom[data.currentChatName][0].includes(data.otherUser) && chatRoom[data.currentChatName][3] == data.username || chatRoom[data.currentChatName][3] == godMode) {
        const sendID = users[data.otherUser];
        // remove user from the room
        const leaveIndex = chatRoom[data.currentChatName][0].indexOf(data.otherUser);
        chatRoom[data.currentChatName][0].splice(leaveIndex, 1);
        io.in(data.currentChatName).emit("pushChatInfo", {users:chatRoom[data.currentChatName][0]});
        io.to(sendID).emit("forceKick", {chatName: data.currentChatName});
        let leaveMessage = data.otherUser + " has been kicked from the room."
        socket.in(data.currentChatName).emit("chatMsgToClient", {message: leaveMessage.italics()});
        io.to(users[data.username]).emit("chatMsgToClient", {message: leaveMessage.italics()});
      }
    });

    // Permanently bans user by adding to ban array
    socket.on("ban", function (data) {
      if (users.hasOwnProperty(data.otherUser) && data.otherUser !== data.username && chatRoom[data.currentChatName][0].includes(data.otherUser) && chatRoom[data.currentChatName][3] == data.username || chatRoom[data.currentChatName][3] == godMode) {
        const sendID = users[data.otherUser];
        // add user to the ban list for this room
        chatRoom[data.currentChatName][1].push(data.otherUser);
        const leaveIndex = chatRoom[data.currentChatName][0].indexOf(data.otherUser);
        chatRoom[data.currentChatName][0].splice(leaveIndex, 1);
        io.in(data.currentChatName).emit("pushChatInfo", {users:chatRoom[data.currentChatName][0]});
        io.to(sendID).emit("forceKick", {chatName: data.currentChatName});
        let leaveMessage = data.otherUser + " has been permanently banned from the room."
        socket.in(data.currentChatName).emit("chatMsgToClient", {message: leaveMessage.italics()});
        io.to(users[data.username]).emit("chatMsgToClient", {message: leaveMessage.italics()});
      }
    });

    // Signal to client that user is removed
    socket.on("forceLeave", function (data) {
      socket.leave(data.chatName);
    });

    socket.on("sendHeart", function(data){
      //io.in(data.currentChatName).emit("pushChatInfo", {users:chatRoom[data.currentChatName][0]});
      io.in(data["currentChatName"]).emit("diddlySquat", {randomMsg:"diddlySquat", user:data.username});
    });
});
