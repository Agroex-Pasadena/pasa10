//COOKIE Y CSRF
// Cookie + csrftoken things
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
    // Metodos sin proteccion CSRF
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});



//NOTIFICACION

var isTalking = false;

function saySomething(standup, message) {
  if (isTalking) {
    $("#the-message").text(message);
    return;
  }
  isTalking = true;
  $("#the-message").text(message);
  if (standup) {
    $('#the-do').animate({ 'margin-top' : "-20px"});
    setTimeout(function(){ $("#the-message").transition('swing down'); }, 400);
    setTimeout(function(){ $("#the-message").transition('swing down'); }, 3400);
    setTimeout(function(){ $('#the-do').animate({ 'margin-top' : "5px"}); }, 3800);
    setTimeout(function(){isTalking = false;}, 3900);
  } else {
    $("#the-message").transition('swing down');
    setTimeout(function(){ $("#the-message").transition('swing down'); }, 3000);
    setTimeout(function(){isTalking = false;}, 3100);
  }
}


$("#the-do").mouseover(function() {
  console.log(isTalking);
  if (!isTalking) {
    saySomething(false, "Don't touch me! I am eating!");
  }
});
