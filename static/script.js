//Reference taken from https://www.youtube.com/watch?v=AMp6hlA8xKA

$(document).ready(function(){
    var socket = io.connect("http://192.168.0.113:5000")
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

// Code segment logic taken from ChatGtp
function handleChatHeadClick(userName, userEmail) {
    if (confirm(`Do you want to send an email to ${userName}?`)) {
        $.ajax({
            url: '/send-email',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ email: userEmail }),
            success: function(response) {
                alert(response.message);
            },
            error: function(xhr, status, error) {
                console.error('Error sending email:', error);
                alert('Failed to send email. Please try again later.');
            }
        });
    }
}