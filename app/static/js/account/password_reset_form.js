import './../new_layout.js';

$(function() {
  'use strict';

  $('.PasswordResetForm form').validate({
      rules: {
          email: {
              email: true,
              required: true
          }
      }
  });
});
