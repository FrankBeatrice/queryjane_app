$(function () {
    $('.QjaneShareGPSfigure, .QjaneShareGPStext').on('click', function() {
        getLocation();
    });

    var initial_country_code = $('#id_country_code').val();
    if (initial_country_code) {
      var flag_url = '/static/flags/' + initial_country_code.toLowerCase() + '.gif';

      $('#id_QjaneVFcountryAutImg').attr('src', flag_url);
    }

    // Professional areas posts
    var CategorieItems;

    $(".qjane-industry-categories-list").on('click', '.btn', function () {
        if ( $( this ).hasClass( "btn-ghost-purple" ) ) {
            $( this ).removeClass( "btn-ghost-purple" );
            $( this ).addClass( "btn-primary" );
        } else {
            $( this ).addClass( "btn-ghost-purple" );
            $( this ).removeClass( "btn-primary" );
        }

        CategorieItems = $('.qjane-industry-categories-list .btn-primary').length;

        if (CategorieItems > 0) {
            var professional_categories_list = new Array();

            $('.qjane-industry-categories-list .btn-primary').each(function (index, value) {
                professional_categories_list.push("" + $(value).data('category-id'));
            });

            $("#id_industry_categories").val(professional_categories_list);
        }

        return false;
    });

    // Validate
    $('.QjaneVFContainer form').validate({
        ignore: [],
        rules: {
            name: {
                minlength: 3,
                maxlength: 50,
                required: true
            },
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
            },
            description_es: {
                minlength: 40,
                required: true
            },
            industry_categories: {
                required: true
            },
        },
        messages: {
            name: {
                minlength: 'Ingrese al menos 3 caracteres.',
                maxlength: 'Ingrese máximo 50 caracteres.',
                required: 'Este campo es requerido.'
            },
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
            },
            description_es: {
                required: 'Ingresa una breve descripción de tu empresa por favor.',
                minlength: 'Por favor, ingresa una descripción breve sobre tu empresa de al menos 40 caracteres.'
            },
            industry_categories: {
                required: 'por favor, selecciona los sectores de la industria de tu empresa.'
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
            } else if (element.attr('name') === 'industry_categories') {
                error.insertAfter('.qjane-industry-categories-list');
            } else {
                error.insertAfter(element);
            }
        }
    });
})
