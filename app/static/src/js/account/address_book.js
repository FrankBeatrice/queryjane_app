$(function () {
    'use strict';

    // remove contact from address book.
    $('#id_remove_user_from_address_book').on('click', function () {
        var user_for_remove_name = $(this).data('user-for-remove-name');
        var remove_url = $(this).data('remove-user-from-address-book-url');

        $.confirm({
            title: 'Address Book',
            content: 'Do you want to remove this contact from your address book?',
            buttons: {
                remove: {
                    btnClass: 'btn-danger',
                    action: function(){
                        $.post(remove_url, function (response) {
                            if (response === 'success') {
                                $('#id_remove_user_from_address_book').hide();

                                $.alert({
                                    title: 'Well done!',
                                    content: user_for_remove_name + ' has been removed from your address book.',
                                });
                            } else {
                                $.alert({
                                    title: 'Error!',
                                    content: 'something is wrong. Please reload and try again.',
                                });
                            }
                        });
                    }
                },
                cancel: function () {}
            }
        });
    });

    // remove company from address book.
    $('#id_remove_company_from_address_book').on('click', function () {
        var company_for_remove_name = $(this).data('company-for-remove-name');
        var remove_company_url = $(this).data('remove-company-from-address-book-url');

        $.confirm({
            title: 'Address Book',
            content: 'Do you want to remove this company from your address book?',
            buttons: {
                remove: {
                    btnClass: 'btn-danger',
                    action: function(){
                        $.post(remove_company_url, function (response) {
                            if (response === 'success') {
                                $('#id_remove_company_from_address_book').hide();

                                $.alert({
                                    title: 'Well done!',
                                    content: company_for_remove_name + ' has been removed from your address book.',
                                });
                            } else {
                                $.alert({
                                    title: 'Error!',
                                    content: 'something is wrong. Please reload and try again.',
                                });
                            }
                        });
                    }
                },
                cancel: function () {}
            }
        });
    });
})
