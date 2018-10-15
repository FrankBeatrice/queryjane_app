// Dependencies
import './../new_layout.js';

$(function () {
    'use strict';

    $('.QjaneShareGPSfigure, .QjaneShareGPStext').on('click', function() {
        getLocation();
    });


    $('#id_venture_contact_form').validate({
        ignore: [],
        rules: {
            email: {
                email: true
            },
            phone_number: {
                number: true,
                minlength: 6,
                maxlength: 15
            },
        }
    });

    $('#id_venture_contact_form').on('submit', function() {
        var formData = new FormData(this);

        if($(this).valid()) {
            $.ajax({
                url : $('#id_venture_contact_form').data('venture-contact-form-url'),
                type: "POST",
                data : formData,
                processData: false,
                contentType: false,
                success:function(response){
                    if (response === 'success') {
                        $('.QjaneVentureContactForm .alert').show();

                        setTimeout(function(){
                            $('.QjaneVentureContactForm .alert').hide();
                        }, 3000);
                    }
                },
            });
        }

        return false;
    });


    // Validate
    $('#id_venture_location_form').validate({
        ignore: [],
        rules: {
            country: {
                required: true
            },
            state: {
                required: true
            },
            city: {
                required: true
            }
        }
    });

    $('#id_venture_location_form').on('submit', function() {
        var formData = new FormData(this);

        if($(this).valid()) {
            $.ajax({
                url : $('#id_venture_location_form').data('venture-location-form-url'),
                type: "POST",
                data : formData,
                processData: false,
                contentType: false,
                success:function(response){
                    if (response === 'success') {
                        $('.QjaneVentureLocationForm .alert-success').show();

                        setTimeout(function(){
                            $('.QjaneVentureLocationForm .alert-success').hide();
                        }, 3000);
                    } else {
                        $('.QjaneVentureLocationForm .alert-danger').show();

                        setTimeout(function(){
                            $('.QjaneVentureLocationForm .alert-danger').hide();
                        }, 3000);
                    }
                },
            });
        }

        return false;
    });

    $('#id_venture_media_form').validate({
        ignore: [],
        rules: {
            url: {
                url: true
            },
            facebook_url: {
                facebookURL: true
            },
            twitter_url: {
                twitterURL: true
            },
            instagram_url: {
                instagramURL: true
            },
            linkedin_url: {
                linkedinURL: true
            },
            googleplus_url: {
                GPlusURL: true
            }
        }
    });

    $('#id_venture_media_form').on('submit', function() {
        var formData = new FormData(this);

        if($(this).valid()) {
            $.ajax({
                url : $('#id_venture_media_form').data('venture-media-form-url'),
                type: "POST",
                data : formData,
                processData: false,
                contentType: false,
                success:function(response){
                    if (response === 'success') {
                        $('.QJVentureMediaUpdate .alert').show();

                        setTimeout(function(){
                            $('.QJVentureMediaUpdate .alert').hide();
                        }, 3000);
                    }
                },
            });
        }

        return false;
    });
})
