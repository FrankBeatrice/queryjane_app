(function () {
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

    $.validator.addMethod("valid_password", function(value, element) {
        return this.optional(element) || /^(?=.*\d)(?!.*\s)(?=.*[a-zA-Z]).{8,}$/.test(value);
    }, "La contraseña debe tener al menos una letra y un número. Los caracteres no pueden ser todos iguales.");


    $.validator.addMethod(
        'filesize',
        function (value, element, param) {
            return this.optional(element) || (element.files[0].size <= param)
        },
        'El tamaño del archivo debe ser inferior a 4MB.'
    );

    $.validator.addMethod(
        'facebookURL',
        function (value, element) {
            return this.optional(element) || /^(https?:\/\/)?((w{3}\.)?)facebook.com\/.*/i.test(value);
        },
        'Please enter a valid Facebook url.'
    );

    $.validator.addMethod(
        'twitterURL',
        function (value, element) {
            return this.optional(element) || /^(https?:\/\/)?((w{3}\.)?)twitter.com\/.*/i.test(value);
        },
        'Please enter a valid Twitter url.'
    );

    $.validator.addMethod(
        'instagramURL',
        function (value, element) {
            return this.optional(element) || /^(https?:\/\/)?((w{3}\.)?)instagram.com\/.*/i.test(value);
        },
        'Please enter a valid Instagram url.'
    );

    $.validator.addMethod(
        'linkedinURL',
        function (value, element) {
            return this.optional(element) || /^(https?:\/\/)?((w{3}\.)?)linkedin.com\/.*/i.test(value);
        },
        'Please enter a valid Linkedin url.'
    );

    $.validator.addMethod(
        'GPlusURL',
        function (value, element) {
            return this.optional(element) || /^(https?:\/\/)?((w{3}\.)?)plus.google.com\/.*/i.test(value);
        },
        'Please enter a valid Google Plus url.'
    );
})();
