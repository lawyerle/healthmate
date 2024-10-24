$(document).ready(function () {
    console.log(window.location.search);
    var urlParams = new URLSearchParams(window.location.search);
    var message = urlParams.get('search').trim();
    console.log(message);

    $('#send-button').click(function() {
        var message = $('#chat-input').val();
        if (message.trim() !== '') {
        $('.loading-indicator').show();  
        displayMessage(message, 'user');       
        sendMessage(message);
        $('#chat-input').val('');
        }
    });

    $('#chat-input').keypress(function(e) {
        if (e.which === 13) {
        $('#send-button').click();
        }
    });

    function sendMessage(message) {
        $.ajax({
        type: 'GET',
        url: 'chat/' + message,
        //   data: { message },
        success: function (response) {
            $('.loading-indicator').hide();  
            displayMessage(response.message, 'bot');
        },
        error: function () {
            $('.loading-indicator').hide();  
            displayMessage('Error sending message.', 'bot');
        }
        });
    }

    function displayMessage(text, sender) {
        var messageElement = $('<div>').addClass('chat-message ' + sender).html(marked.parse(text));
        $('.chat-messages').append(messageElement);
        $('.chat-window').scrollTop($('.chat-window')[0].scrollHeight);
    }

    if (message) {
        // 파라미터가 있는 경우, chat-input에 입력하고 '#send-button' 클릭 이벤트 호출
        $('#chat-input').val(message);
        $('#send-button').click();
    }
});
