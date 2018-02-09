/*
 *
 * login-register modal
 * Autor: Creative Tim
 * Web-autor: creative.tim
 * Web script: http://creative-tim.com
 *
 */
function showRegisterForm(){
    $('.loginBox').fadeOut('fast',function(){
        $('.registerBox').fadeIn('fast');
        $('.login-footer').fadeOut('fast',function(){
            $('.register-footer').fadeIn('fast');
        });
        $('.modal-title').html('Register');
    });
    $('.error').removeClass('alert alert-danger').html('');

}
function showLoginForm(){
    $('#loginModal .registerBox').fadeOut('fast',function(){
        $('.loginBox').fadeIn('fast');
        $('.register-footer').fadeOut('fast',function(){
            $('.login-footer').fadeIn('fast');
        });

        $('.modal-title').html('Login with');
    });
     $('.error').removeClass('alert alert-danger').html('');
}

function openLoginModal(){
    showLoginForm();
    setTimeout(function(){
        $('#loginModal').modal('show');
    }, 230);

}
function openRegisterModal(){
    showRegisterForm();
    setTimeout(function(){
        $('#loginModal').modal('show');
    }, 230);

}

function loginAjax(e){
    e.preventDefault();
var datastring = $("#login-form").serialize();
 $.ajax({
      url: "sso/alogin/",
      type:"POST",
      data: datastring,
      success: function(data){
        if(data != "fail")
        {
          window.location.replace(data);
        }
        else{
          shakeModal();
        }
      },
      error: function(xhr, errmsg, err)
      {
        alert(xhr.status + ": " + xhr.responseText);
      }
    });

}

function registerAjax(e){
    e.preventDefault();
    var datastring = $("#register-form").serialize();
 $.ajax({
      url: "sso/aregister/",
      type:"POST",
      data: datastring,
      success: function(data){
        if(data=="success")
        {
            $('registerBox').remove();
            $('.error').addClass('alert alert-success').append("Registration Success! An email verification has been sent, kindly verify your email to activate your account.");
        }
        else {
            $('#loginModal .modal-dialog').addClass('shake');
            $('.error').empty();   //reset error message

            $('.error').addClass('alert alert-danger').append("Invalid " + data);

            $('input[type="password"]').val('');
            setTimeout( function(){
            $('#loginModal .modal-dialog').removeClass('shake');
          }, 1000 );
        }
      },
      error: function(xhr, errmsg, err)
      {
        alert(xhr.status + ": " + xhr.responseText);
      }
    });
}

function shakeModal(){
    $('#loginModal .modal-dialog').addClass('shake');
             $('.error').addClass('alert alert-danger').html("Invalid email/password combination");
             $('input[type="password"]').val('');
             setTimeout( function(){
                $('#loginModal .modal-dialog').removeClass('shake');
    }, 1000 );
}
