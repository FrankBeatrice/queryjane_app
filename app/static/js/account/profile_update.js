$(function () {
    'use strict';

    $('.QjaneShareGPSfigure, .QjaneShareGPStext').on('click', function() {
        getLocation();
    });

    // Update professional profile category
    var pp_category_url = $('.qjane-industry-categories-list').data('update-professional-profile-category-url');

    $(".qjane-industry-categories-list").on('click', '.btn', function () {
        var category_id = $(this).data('category-id');
        var new_status;

        if ( $( this ).hasClass( "btn-ghost-purple" ) ) {
            // Add category
            $( this ).removeClass( "btn-ghost-purple" );
            $( this ).addClass( "btn-primary" );
            new_status = true
        } else {
            // Remove category
            $( this ).addClass( "btn-ghost-purple" );
            $( this ).removeClass( "btn-primary" );
            new_status = false
        }

        $.post(pp_category_url, {'category_id': category_id, 'new_status': new_status}, function (response) {
            console.log("response");
        });
    });
})
