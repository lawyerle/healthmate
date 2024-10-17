$(document).ready(function() {
  $('#send-button').click(function() {
    var message = $('#chat-input').val();
    if (message.trim() !== '') {
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
      url: 'http://127.0.0.1:8000/chat/' + message,
    //   data: { message },
      success: function(response) {
        displayMessage(message, 'user');
        displayMessage(response.message, 'bot');
      },
      error: function() {
        displayMessage('Error sending message.', 'bot');
      }
    });
  }

  function displayMessage(text, sender) {
    var messageElement = $('<div>').addClass('chat-message ' + sender).html(marked.parse(text));
    $('.chat-messages').append(messageElement);
    $('.chat-window').scrollTop($('.chat-window')[0].scrollHeight);
  }
});
