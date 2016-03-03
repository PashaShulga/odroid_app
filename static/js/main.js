 function init() {
  initHost('host1');
  //initHost('host2');
  //initHost('host3');
  //initHost('host4');
}

var seriesOptions = [
  { strokeStyle: 'rgba(255, 0, 0, 1)', fillStyle: 'rgba(255, 0, 0, 0.1)', lineWidth: 3 }
  //{ strokeStyle: 'rgba(0, 255, 0, 1)', fillStyle: 'rgba(0, 255, 0, 0.1)', lineWidth: 3 },
  //{ strokeStyle: 'rgba(0, 0, 255, 1)', fillStyle: 'rgba(0, 0, 255, 0.1)', lineWidth: 3 },
  //{ strokeStyle: 'rgba(255, 255, 0, 1)', fillStyle: 'rgba(255, 255, 0, 0.1)', lineWidth: 3 }
];
namespace = '/test'; // change to an empty string to use the global namespace
            // the socket.io documentation recommends sending an explicit package upon connection
            // this is specially important when using the global namespace
            var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
            // event handler for server sent data
            // the data is displayed in the "Received" section of the page
            socket.on('my response', function(msg) {
                $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
            });
            // event handler for new connections
            socket.on('connect', function() {
                socket.emit('my event', {data: 'I\'m connected!'});
            });
            // handlers for the different forms in the page
            // these send data to the server in a variety of ways
            $('form#emit').submit(function(event) {
                socket.emit('my event', {data: $('#emit_data').val()});
                return false;
            });
            $('form#broadcast').submit(function(event) {
                socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
                return false;
            });
            $('form#join').submit(function(event) {
                socket.emit('join', {room: $('#join_room').val()});
                return false;
            });
            $('form#leave').submit(function(event) {
                socket.emit('leave', {room: $('#leave_room').val()});
                return false;
            });
            $('form#send_room').submit(function(event) {
                socket.emit('my room event', {room: $('#room_name').val(), data: $('#room_data').val()});
                return false;
            });
            $('form#close').submit(function(event) {
                socket.emit('close room', {room: $('#close_room').val()});
                return false;
            });
            $('form#disconnect').submit(function(event) {
                socket.emit('disconnect request');
                return false;
            });
function initHost(hostId) {

  // Initialize an empty TimeSeries for each CPU.
  var cpuDataSets = [new TimeSeries()];
  var now = new Date().getTime();
  for (var t = now - 1000 * 50; t <= now; t += 1000) {
    addRandomValueToDataSets(t, cpuDataSets);
  }
  // Every second, simulate a new set of readings being taken from each CPU.
  setInterval(function() {
    addRandomValueToDataSets(new Date().getTime(), cpuDataSets);
  }, 1000);

  // Build the timeline
  var timeline = new SmoothieChart({ fps: 30, millisPerPixel: 20, grid: { strokeStyle: '#555555', lineWidth: 1, millisPerLine: 1000, verticalSections: 4}});
  for (var i = 0; i < cpuDataSets.length; i++) {
    timeline.addTimeSeries(cpuDataSets[i], seriesOptions[i]);
  }
  timeline.streamTo(document.getElementById(hostId + 'Cpu'), 1000);
}

    function addRandomValueToDataSets(time, dataSets) {
        for (var i = 0; i < dataSets.length; i++) {
            dataSets[i].append(time, Math.random());
        }
}