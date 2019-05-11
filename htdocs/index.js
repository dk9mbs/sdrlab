function connectWebSocket() {
    var ws = new WebSocket("ws://" + window.location.host + "/websocket");
    ws.onopen = function(evt) {
        console.log("connected!");
    }
    ws.onclose = function(evt) {
        console.log("closed");
        setTimeout(function() {
            connectWebSocket();
        }, 1000);
    }
    ws.onerror = function(evt) {
        console.log("error: " + evt.message);
    }
    ws.onmessage = function (evt) {
        console.log("message => " +evt.data);
        if(JSON.parse(evt.data).type=='hardware') {
            vue.config =  JSON.parse(evt.data)['message'];
            console.log("vue.config => "+JSON.stringify(vue.config));
        }
    }
}