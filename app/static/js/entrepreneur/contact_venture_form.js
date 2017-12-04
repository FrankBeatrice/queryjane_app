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
        },
        messages: {
            email: {
                email: 'Ingresa un correo electrónico válido.'
            },
            phone_number: {
                number: 'Ingresa un número válido.',
                minlength: 'Ingresa al menos 6 caracteres',
                maxlength: 'Ingresa máximo 15 caracteres'
            }
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
                required: 'El país es requerido.'
            },
            country_code: {
                required: 'Selecciona un país de la lista por favor.'
            },
            city_search: {
                required: 'La ciudad es requerida.'
            },
            city_id: {
                required: 'selecciona una ciudad de la lista por favor. Si tu ciudad no está registrada, por favor permitenos obtener tu ubicación.'
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
