$(document).ready(function(){
    var socket = io.connect("https://localhost:5000")
    socket.on('connect', function(){
        socket.send("connection_successful")
    });
    
});