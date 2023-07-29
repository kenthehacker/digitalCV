//wss://stream.binance.com:9443/ws/btcusdt@trade
//creates websocket connection to binance
var btcWebsocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@trade");
//event listener from the socket

btcWebsocket.onmessage = function(e){

    var price = JSON.parse(e.data);
    $("#crypto").text("Hello "+currentUser+" your BTC is worth: "+String(price.p));
}
