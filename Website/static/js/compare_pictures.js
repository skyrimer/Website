function readURL1(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function(e) {
        $('#image_1').attr('src', e.target.result);
      }

      reader.readAsDataURL(input.files[0]);
    }
  }


  function readURL2(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function(e) {
        $('#image_2').attr('src', e.target.result);
      }

      reader.readAsDataURL(input.files[0]);
    }
  }

  
$("#input_1").change(function() {
  readURL1(this);
});

$("#input_2").change(function() {
  readURL2(this);
});
