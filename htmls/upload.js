
  $('#inputId').change(function(){
    $('body').css('background-color','black');
    $('#testfile').text((this).value);

      $('#uploadform').submit( function(e) {
    e.preventDefault();

    var data = new FormData(this);
    
        $.ajax({
            data: data,
            type: 'post',
            url: 'localhost:8000/open',
           success: function () {
                alert("Working")
            },
            failure: function () {
                alert("Not Working")
            }
            });
  });
      
  });