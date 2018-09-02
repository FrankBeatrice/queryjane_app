import './../new_layout.js';

// CSS
import './../../sass/login.scss';

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
