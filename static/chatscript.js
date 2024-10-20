$(document).ready(function() {
  $('#send-button').click(function() {
    var message = $('#chat-input').val();
    $('.loading-indicator').show();  
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
      url: 'chat/' + message,
    //   data: { message },
      success: function (response) {
        $('.loading-indicator').hide();  
        displayMessage(message, 'user');
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
});
