$(document).ready(function(){
    var socket = io.connect("http://localhost:5000")
    socket.on('connect', function(){
        console.log("Connected to server")
        socket.send("connection_successful");
    });

    socket.on('message', function(message){
        $('#messages').append($('<p>').text(data));
    });

    $('sendBtn').on('click', function(){
        console.log("message send:"+ $('#username').val())
        socket.send($('#username').val() + ': ' + $('#message').val());
    })
});