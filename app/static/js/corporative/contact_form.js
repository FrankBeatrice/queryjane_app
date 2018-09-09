import './../new_layout.js';

$(function() {
  'use strict';

  $('#idContactForm').validate({
      rules: {
          subject: {
              maxlength: 200,
              required: true
          },
          name: {
              minlength: 4,
              required: true
          },
          email: {
              email: true,
              required: true
          },
          message: {
              minlength: 10,
              required: true
          }
      }
  });
});
