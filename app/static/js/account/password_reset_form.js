import './../new_layout.js';

// CSS
import './../../sass/password_reset_form.scss';

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
