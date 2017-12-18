function getLocation() {
    if (navigator.geolocation) {
        $('.QjaneShareGPSloading').show();
        $('.QjaneShareGPSfigure').hide();
        navigator.geolocation.getCurrentPosition(function(position) {
            showPosition(position);
        }, function() {
            $('.QjaneShareGPSloading').hide();
            $('.QjaneShareGPSfigure').show();
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

(function () {
    $.validator.addMethod("valid_password", function(value, element) {
        return this.optional(element) || /^(?=.*\d)(?!.*\s)(?=.*[a-zA-Z]).{8,}$/.test(value);
    }, "La contraseña debe tener al menos una letra y un número. Los caracteres no pueden ser todos iguales");


    $.validator.addMethod(
        'filesize',
        function (value, element, param) {
            return this.optional(element) || (element.files[0].size <= param)
        },
        'El tamaño del archivo debe ser inferior a 4MB'
    );

    var mqDetector;

    mqDetector = new MediaQueryDetector({
        $target: $('#mq-detector')
    });

     $.ajaxSetup({
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                         if (cookie.substring(0, name.length + 1) == (name + '=')) {
                             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                             break;
                         }
                     }
                 }
                 return cookieValue;
             }
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         }
    });

    // Login inline validations
    $('.qjane-login-form').validate({
        rules: {
            'login_form-email': {
                minlength: 2,
                maxlength: 40,
                email: true,
                required: true
            },
            'login_form-password': {
                minlength: 8,
                valid_password: true,
                required: true,

            }
        },
        messages: {
            'login_form-email': {
                email: 'Ingresa una dirección de email válida',
                required: 'Este campo es requerido'
            },
            'login_form-password': {
                required: 'Este campo es requerido',
                minlength: 'Ingresa al menos 8 caracteres'
            }
        }
    });

    // Ajax_login form submit
    $('.qjane-navbar-login-container').on('submit', '.qjane-login-form', function () {
        'use strict';

        var url = $('.qjane-login-form').data('login-form-url');

        $.post(url, $('.qjane-login-form').serialize(), function (response) {
            if (response === 'fail') {
                $('.qjane-login-forms-error-message')
                    .show()
                    .addClass('mb-xs')
                    .text('We do not recognize this email address.');
                return;
            }  else if (response === 'data_error') {
                $('.qjane-login-forms-error-message')
                    .show()
                    .addClass('mb-xs')
                    .text('Contraseña incorrecta.');
                return;
            } else if (response === 'inactive_account') {
                $('.qjane-login-forms-error-message')
                    .show()
                    .addClass('mb-xs')
                    .text('The account associated with this email is inactive.');
                return;
            } else if (response === 'successful_login') {
                window.location.href = $('.qjane-login-form').data('redirect-url');
                return;
            }
        });

        return false;
    });

  $('#id-qjane-home-signup-form').validate({
      rules: {
          first_name: {
              minlength: 2,
              maxlength: 40,
              required: true
          },
          last_name: {
              minlength: 2,
              maxlength: 40,
              required: true
          },
          email: {
              email: true,
              required: true
          },
          valid_password: {
              required: true,
              minlength: 8
          }
      }
  });

    // Populate general message modal with notifications messages.
    $('.notification-list').on('click', '.qjane-notification-link', function () {
        var notification_url = $(this).data('notification-url');
        $.post(notification_url).done(function (response) {
            if (response != 'fail') {
                $('#generalModalMessage .modal-content').html(response.content);
            }
        });
    });

    // Set global methods
    qjGlobal.mqDetector = mqDetector;
})();
