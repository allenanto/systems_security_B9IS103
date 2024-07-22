//Reference taken from https://www.youtube.com/watch?v=AMp6hlA8xKA

$(document).ready(function(){
    var socket = io.connect("http://192.168.0.1:5000")
    socket.on('connect', function(){
        console.log("Connected to server");
        socket.send("connection_successful");
    });

    socket.on('message', function(message){
        $('#messages').append($('<p>').text(message));
    });

    $('#sendBtn').on('click', function(){
        console.log("Message send");
        socket.send($('#username').text() + ': ' + $('#message').val());
        $('#message').val('');
    });
});