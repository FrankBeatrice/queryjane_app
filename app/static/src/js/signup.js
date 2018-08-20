import './new_layout.js';

$(function () {
  'use strict';

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
