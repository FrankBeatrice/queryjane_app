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
            country_search: {
                required: true
            },
            country_code: {
                required: true,
                maxlength: 2
            },
            city_search: {
                required: true
            },
            city_id: {
                maxlength: 10,
                required: true
            }
        },
        messages: {
            country_search: {
                required: 'Country is required.'
            },
            country_code: {
                required: 'Select a country from de list.'
            },
            city_search: {
                required: 'City is required.'
            },
            city_id: {
                required: 'Select a city from the list. If your city is not available, please allow us to get your location.'
            }
        },
        errorPlacement: function(error, element) {
            if (element.attr('name') === 'country_search') {
                error.insertAfter('#id_QjaneVFcountryAutImg');
            } else if (element.attr('name') === 'country_code') {
                error.insertAfter('#id_QjaneVFcountryAutImg');
            } else if (element.attr('name') === 'city_search') {
                error.insertAfter('.QjaneShareGPSfigure');
            } else if (element.attr('name') === 'city_id') {
                error.insertAfter('.QjaneShareGPSfigure');
            } else {
                error.insertAfter(element);
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
})
