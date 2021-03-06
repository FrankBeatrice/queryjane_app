// Dependencies
import './../new_layout.js';
import './../place/place_autocomplete.js';

$(function () {
    var quill = new Quill('#rich_editor_description', {
        theme: 'snow'
    }).on('text-change', function () {
        $('#id_description').val($('#rich_editor_description .ql-editor').html());
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
    $('.QjaneVentureJobOfferForm form').validate({
        ignore: [],
        rules: {
            title: {
                minlength: 3,
                maxlength: 80,
                required: true
            },
            description: {
                minlength: 40,
                required: true
            },
            industry_categories: {
                required: true
            }
        },
        errorPlacement: function(error, element) {
            if (element.attr('name') === 'country_search') {
                error.insertAfter('#id_QjaneVFcountryAutImg');
            } else if (element.attr('name') === 'industry_categories') {
                error.insertAfter('.qjane-industry-categories-list');
            }else if (element.attr('name') === 'description') {
                error.insertAfter('#rich_editor_description');
            } else {
                error.insertAfter(element);
            }
        }
    });
})
