import './../new_layout.js';

$(function () {
  'use strict';

    $('#id_qjLogInForm').validate({
        rules: {
            username: {
                email: true,
                required: true
            },
            password: {
                required: true
            }
        }
    });
})
