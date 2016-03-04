    var socket = new WebSocket('ws://localhost:8765');

    socket.onmessage = function(event) {
        var data = JSON.parse(event.data);
        var d1 = [];

        $(function () {
            for (var i = 0; i < data.length; i++) {
                d1.push([i, data[i]]);
            }
            $.plot("#placeholder", [d1]);
        });
    };
