// Variables para guardar los archivos subidos
var allFiles = [];
var numberOfValidatedFile = 0;

// Mostrar formulario
$( document ).ready(function() {
  $('#analisis-box').transition('scale'); //Antes era slide down
  
});

// Boton falso de subir archivo
$("#file-upload").on("click", function() {
   $('#hidden-file-upload').click();
});

// Subir un nuevo archivo
$("#hidden-file-upload").on("change", function(e) {
  var files = e.target.files;
  var f = files[0];

  if (f.type.match('image.*') && numberOfValidatedFile <= 4) {
    // Subir las cosas necesarias
    numberOfValidatedFile ++;
    $('#images').val('ok');

    // Renderizar a la vista
    var id = allFiles.length;
    var reader = new FileReader();
    reader.onload = (function(theFile) {
      return function(e) {
        allFiles.push(e.target.result);
        var text = '<div class="thumb" id="image-'+id+'" style="display: none">' +
          '<img src="'+e.target.result+'">' +
          '<i class="remove circle icon red big remove-button" onclick="removeFile('+id+')"></i>' +
        '</div>';

        $("#list").append(text);
        $("#image-"+id).transition('scale');
      };
    })(f);
    reader.readAsDataURL(f);
  } else {
    saySomething(true, "Disculpe, no puede publicar tantas imágenes")
  }
})

// Borrar una imagen subida
function removeFile(id) {
  $("#image-"+id).transition('scale');
  allFiles[id] = 'null';
  numberOfValidatedFile --;
  if (numberOfValidatedFile == 0) {
    $('#images').val('');
  }
}
function removeAllFiles() {
  numberOfValidatedFile = 0;
  allFiles = [];
  $('#images').val('');
  $('#list').html('');
}

// Enviar desde handling
$("#submit-button").on("click", function() {
  
});

// Validacion de formulario
$("#form-nuevo-enfermedad").form({
    enfermedadname: {
      identifier: 'enfermedad-name',
      rules: [{
        type   : 'empty',
        prompt : 'Por favor, ingrese el nombre de la enfermedad de la planta'
      }]
    },
    planta: {
      identifier: 'planta',
      rules: [{
        type    : 'empty',
        prompt  : 'Please choose the planta'
      }]
    },
    sintomaAAA: {
      identifier: 'sintoma-aa',
      rules: [{
        type    : 'checked',
        prompt  : '¿Hay perforaciones en la hoja?'
      }]
    },
 
    sintomacc: {
      identifier: 'sintoma-cc',
      rules: [{
        type    : 'checked',
        prompt  : '¿Qué formas tienen las manchas?'
      }]
    },
    
    sintomadd: {
      identifier: 'sintoma-dd',
      rules: [{
        type    : 'checked',
        prompt  : '¿Se presenta acame?'
      }]
    },
    sintomaee: {
      identifier: 'sintoma-ee',
      rules: [{
        type    : 'checked',
        prompt  : '¿¿Dónde están distribuidas las lesiones??'
      }]
    },

    description: {
      identifier: 'description',
      rules: [{
        type    : 'empty',
        prompt  : 'Por favor, agrega un tratamiento para la cura de la planta'
      }]
    },
    images: {
      identifier: 'images',
      rules: [{
        type    : 'empty',
        prompt  : 'Por favor, publica una imagen de la planta'
      }]
    }
}, {
  onSuccess: function() {
    submitForm();
    return false;
  },
  onFailure: function() {
  //  saySomething(true, "Ocurrió un error, disculpe")
    return false;
  }
});

// Enviar formulario
function submitForm() {
  // preparing data
  var formData = {
    name:         $('#form-nuevo-enfermedad').find('input[name="enfermedad-name"]').val(),
    planta:      $('#form-nuevo-enfermedad').find('select[name="planta"]').val(),
    sintomaDD:   $('#form-nuevo-enfermedad').find('input[name="sintoma-dd"]:checked').val(),
    sintomaCC:   $('#form-nuevo-enfermedad').find('input[name="sintoma-cc"]:checked').val(),
    sintomaEE:   $('#form-nuevo-enfermedad').find('input[name="sintoma-ee"]:checked').val(),
    sintomaAA: $('#form-nuevo-enfermedad').find('input[name="sintoma-aa"]:checked').val(),
    sintomaBB:      $('#form-nuevo-enfermedad').find('input[name="sintoma-bb"]:checked').val(),
    description:  $('#description').val(),
    images:       JSON.stringify(allFiles),
  };

//Inicio modal octubre
  $('#modal-octubre').modal('show');
//Fin modal octubre

  $("#form-nuevo-enfermedad").addClass("loading");

  // Ajax post
  $.ajax({ type: 'POST', url: '/api/enfermedadestripla', data: formData,
    success: function(data) {
      console.log(data);
      removeAllFiles();
      $("#form-nuevo-enfermedad").form("reset");
      $("#form-nuevo-enfermedad").removeClass("loading");
      //saySomething(true, "Gracias por enriquecer a AgroEX");
    },
    error: function() {

  }});
}
