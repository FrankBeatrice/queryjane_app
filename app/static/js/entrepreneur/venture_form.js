// Dependencies
import './../new_layout.js';

$(function () {
    var quill_en = new Quill('#rich_editor_description_en', {
        theme: 'snow'
    }).on('text-change', function () {
        $('#id_description_en').val($('#rich_editor_description_en .ql-editor').html());
    });

    var quill_es = new Quill('#rich_editor_description_es', {
        theme: 'snow'
    }).on('text-change', function () {
        $('#id_description_es').val($('#rich_editor_description_es .ql-editor').html());
    });

    $('.QjaneShareGPSfigure, .QjaneShareGPStext').on('click', function() {
        getLocation();
    });

    var initial_country_code = $('#id_country_code').val();
    if (initial_country_code) {
      var flag_url = '/static/img/flags/' + initial_country_code.toLowerCase() + '.png';

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
            description_en: {
                required: false,
                minlength: 40
            },
            description_es: {
                required: false,
                minlength: 40
            },
            industry_categories: {
                required: true
            },
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
            } else if (element.attr('name') === 'description_en') {
                error.insertAfter('#rich_editor_description_en');
            } else if (element.attr('name') === 'description_es') {
                error.insertAfter('#rich_editor_description_es');
            } else {
                error.insertAfter(element);
            }
        }
    });
})
