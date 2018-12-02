// Click en boton pref
$("#analizar-button").on("click", function() {
  $('#outer-box').transition('slide down');

})


// Mostrar box pref y boton pref
$( document ).ready(function() {
  $("#analizar-link").hide();
  $("#analizar-button").show();
  $('#outer-box').transition('slide down');

});
