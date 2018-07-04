$(function () {
  'use strict';

  $.validator.addMethod("valid_password", function(value, element) {
      return this.optional(element) || /^(?=.*\d)(?!.*\s)(?=.*[a-zA-Z]).{8,}$/.test(value);
  }, "La contraseña debe tener al menos una letra y un número. Los caracteres no pueden ser todos iguales.");

  $('#id_qjSignUpForm').validate({
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
          password: {
              minlength: 8,
              valid_password: true,
              required: true
          }
      }
  });
})
