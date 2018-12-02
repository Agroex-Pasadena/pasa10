// Variables y constantes
// Resultados actuales de enfermedades
var currentData;
var currentEnfermedad;
var currentTab;
var values = {'sintomaBB': ['tallo', 'raiz'],
              'sintomaAA': ['sintomaAAA', '<del>sintomaAAA</del>'],
              'sintomaDD': ['si acame', 'no acame'],
              'sintomaCC': ['estrecha u oval', 'irregular'],
              'sintomaEE': ['si marchitez', 'no marchitez']//,
            };
var changableData = ['sintomaAA', 'sintomaBB', 'sintomaCC', 'sintomaEE', 'sintomaDD'];
var cardColors = ["grey", "black", "yellow", "olive", "green", "teal", "blue", "violet", "purple", "pink", "brown", "red", "orange"];
var numColors = cardColors.length;



// Click en boton Pref
$("#analizar-button").on("click", function() {
  $('#outer-box').transition('scale');
})


// Mostrar box pref y boton pref
$( document ).ready(function() {
  $("#analizar-link").hide();
  $("#analizar-button").show();
  $('#outer-box').transition('scale');
  
});


// Radio buttons uncheckeables
$('.ui.radio').checkbox({
  uncheckable: true
});


// Slider imagen
$('#left-arr').click(function() {
  currentTab = (currentTab + 1) % currentData[currentEnfermedad].images;
  resetTab(currentTab);
});
$('#right-arr').click(function() {
  console.log("testing")
  currentTab = (currentTab + currentData[currentEnfermedad].images - 1) % currentData[currentEnfermedad].images;
  resetTab(currentTab);
});
function resetTab(index) {
  for (i = 0; i < currentData[currentEnfermedad].images; i++) {
    $('#tab'+i).removeClass('active')
  }
  $('#tab'+index).addClass('active')
}


//CONTROLADOR DE FORMULARIO DE PREFERENCIA #####################################################################

// Validacion de formulario pref
$("#form-analisis").form({
  planta: {
  identifier: 'planta',
  rules: [{
    type    : 'empty',
    prompt  : 'Please choose the planta'
  }]
}}, {
  onSuccess: function() {
    submitForm();
    return false;
  },
  onFailure: function() {
    saySomething(true, "Opss, there are some errors :(")
    return false;
  }
});


// Enviar formulario de preferencia
function submitForm() {
  // Poner formulario en "loading" 
  $('#form-analisis').addClass("loading");

  // Preparar datos
  var formData = {
    planta:      $('#form-analisis').find('select[name="planta"]').val(),
    sintomaDD:   filter($('#form-analisis').find('input[name="sintoma-dd"]:checked').val()),
    sintomaCC:   filter($('#form-analisis').find('input[name="sintoma-cc"]:checked').val()),
    sintomaEE:   filter($('#form-analisis').find('input[name="sintoma-ee"]:checked').val()),
    sintomaBB:   filter($('#form-analisis').find('input[name="sintoma-bb"]:checked').val()),
    sintomaAA: filter($('#form-analisis').find('input[name="sintoma-aa"]:checked').val()),
  };

  // Ajax post
  $.ajax({ type: 'POST', url: '/api/analisismara', data: formData,
    success: function(data) {
      $('#form-analisis').removeClass("loading");
      if (data.length == 0) {
        
        //Inicio modal diciembre
        $('#modal-diciembre-sorry').modal('show');
      //Fin modal diciembre
      } else {
        $('#outer-box').transition('scale');
        renderCards(data);
      }
    },
    error: function() {
      
      //Inicio modal octubre
      $('#modal-diciembre').modal('show');
      //Fin modal octubre
  }});
}


// CARDS ######################################################################################
//Construir cards
function renderCards(data) {
  currentData = data;
  var content = "";
  var index = 0;

  for (i = 0; i < data.length; i++) {
    content += `
      <div id="card-`+i+`" class="enfermedad-card ui `+cardColors[index]+` card" style="display:none" onclick="clickCard(`+i+`)">
        <div class="image">
          <img src="/static/images/enfermedadesmara/`+data[i].id+`_1.jpeg">
        </div>
        <div class="content">
          <div class="header left floated">`+data[i].name+`</div>
          <div class="right floated">
            <i class="star icon card-star"></i>`+Math.round(data[i].stars * 100) / 100+`
          </div>
        </div>
      </div>`;
    index = (index + 1) % numColors;
  }
  $("#enfermedad-cards").html(content);
  // mostrar cards
  $('.enfermedad-card').transition({
    animation : 'horizontal flip',
    interval  : 5000
  })
  //saySomething(false, "Diagnóstico generado")
}


// mostrar detalles del card cuando se hace touch
function clickCard(id) {
  currentEnfermedad = id;

  // Nombre
  $("#detalle-nombre").text(currentData[id].name);

  // Descripcion
  $("#detail-description").text(currentData[id].description);

  // Tags
  var index = 0;
  var tags = "";
  tags += `<a class="agro-tag ui `+cardColors[index]+` basic label">`+currentData[id].planta+`</a>`;
  index = (index + 1) % numColors;

  var text = (currentData[id].sintomaAAA == 'TRUE') ? "sintomaAAA" : "<del>sintomaAAA</del>"
  tags += `<a class="agro-tag ui `+cardColors[index]+` basic label" onclick="showSuggestions(this,'`+cardColors[index]+`','`+changableData[0]+`')">`+text+`</a>`;
  index = (index + 1) % numColors;

  for (i = 1; i < changableData.length; i++) {
    tags += `<a class="agro-tag ui `+cardColors[index]+` basic label" onclick="showSuggestions(this,'`+cardColors[index]+`','`+changableData[i]+`')">`+currentData[id][changableData[i]]+`</a>`;
    index = (index + 1) % numColors;
  }
  $("#detalle-tags").html(tags);

  // Stars
  $("#detail-rating").text("Rating: "+Math.round(currentData[id].stars * 100) / 100);
  for (i = 1; i <= 5; i ++) {
    if (currentData[id].stars < i-1 + 0.25) {
      $("#header-star-"+i).removeClass("star")
      $("#header-star-"+i).removeClass("empty star")
      $("#header-star-"+i).removeClass("star half empty")
      $("#header-star-"+i).addClass("empty star")
    } else if (currentData[id].stars > i-1 + 0.75) {
      $("#header-star-"+i).removeClass("star")
      $("#header-star-"+i).removeClass("empty star")
      $("#header-star-"+i).removeClass("star half empty")
      $("#header-star-"+i).addClass("star")
    } else {
      $("#header-star-"+i).removeClass("star")
      $("#header-star-"+i).removeClass("empty star")
      $("#header-star-"+i).removeClass("star half empty")
      $("#header-star-"+i).addClass("star half empty")
    }
  }

  // Imagenes
  var imagesText = "";
  for (i = 1; i <= currentData[id].images; i++) {
    if (i == 1) {
      imagesText += `
      <div id="tab`+(i-1)+`" class="ui bottom attached tab active" data-tab="`+(i-1)+`">
        <img src="/static/images/enfermedadesmara/`+currentData[id].id+`_`+i+`.jpeg" style="width:100%"/>
      </div>`;
    } else {
      imagesText += `
      <div id="tab`+(i-1)+`" class="ui bottom attached tab" data-tab="`+(i-1)+`">
        <img src="/static/images/enfermedadesmara/`+currentData[id].id+`_`+i+`.jpeg" style="width:100%"/>
      </div>`;
    }
  }
  $("#modal-image-tabs").html(imagesText);
  currentTab = 0;
  if (currentData[id].images == 1) {
    $('#left-arr').hide();
    $('#right-arr').hide();
  } else {
    $('#left-arr').show();
    $('#right-arr').show();
  }

  // Comentarios
  $("#comments").html("");
  $("#comments").addClass("loading");
  $.ajax({ type: 'GET', url: '/api/reviewsmara', data: {"enfermedadId": currentData[id].id},
    success: function(data) {
      $("#comments").removeClass("loading");
      showComments(data);
    },
    error: function() {
      saySomething(true, "Ocurrió un error, disculpe")
  }});
  // Mostrar
  $("#modal-card-detail").modal('show');
}

//CALIFICACION###################################################################################################

// Mostrar el formulario para el nuevo review
$("#review-new-button").click(function() {
  $("#review-form").transition('scale');
});


// Click en star
function clickStar(id) {
  for(i = 1; i <= id; i++) {
    $("#star-"+i).removeClass("empty star")
    $("#star-"+i).addClass("star")
  }
  for(i = id+1; i <= 5; i++) {
    $("#star-"+i).removeClass("star")
    $("#star-"+i).addClass("empty star")
  }
  $('#review-form').find('input[name="review-stars"]').val(id);
}


// Validacion de calificacion
$("#review-form").form({

    reviewStars: {
      identifier: 'review-stars',
      rules: [{
        type    : 'empty',
        prompt  : 'Por favor, califica el diagnóstico'
      }]
    }
}, {
  onSuccess: function() {
    submitReview();
    // Reset Form
    $("#review-form").transition('scale');
    clickStar(0);
    $("#review-form").form('reset');
    return false;
  },
  onFailure: function() {
    return false;
  }
});


// Enviar formulario de calificacion
function submitReview() {
  // Preparar datos
  var formData = {
    reviewer:         $('#review-form').find('input[name="review-name"]').val(),
    comment:          $('#review-comment').val(),
    stars:            $('#review-form').find('input[name="review-stars"]').val(),
    enfermedadName:         currentData[currentEnfermedad].name,
    enfermedadId:           currentData[currentEnfermedad].id,
  };

  // Ajax post
  $.ajax({ type: 'POST', url: '/api/reviewsmara', data: formData,
    success: function(data) {
      var text = $("#comments").text();
      var imageSize = 500;
      var margintop  =  Math.floor((Math.random() * (imageSize-50)) + 1);
      var marginleft =  Math.floor((Math.random() * (imageSize-50)) + 1);
      var currentTime = new Date();
      text =
      `<div class="comment">
        <div class="avatar" style="height:35px !important;overflow: hidden;">
          <img src="/static/images/avatar.png" style="width:`+imageSize+`px;height:`+imageSize+`px;
                                              margin-top:-`+margintop+`px;margin-left:-`+marginleft+`px">
        </div>
        <div class="content">
          <a class="author">`+formData.reviewer+`</a>
          <div class="metadata">
            <span class="date">`+currentTime.toDateString()+`</span>
          </div>
          <div class="text">
            `+formData.comment+`
          </div>
        </div>
      </div>` + $("#comments").html();
      $("#comments").html(text);
    },
    error: function() {
      
  }});
}

// Extras
function filter(text) {
  return (text == undefined) ? "?" : text;
}
