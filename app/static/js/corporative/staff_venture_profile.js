$(function () {
    'use strict';

    // Hide company profile.
    $('.JSCompanyActions').on('click', '.js_hideCompany', function() {
        var hide_url = $(this).data('hide-url');
        var hide_button = $(this);
        $.confirm({
            title: 'Do you want to hide this company?',
            content: 'Company profile will be hidden for users.',
            buttons: {
                hide: {
                    btnClass: 'btn-primary',
                    action: function(){
                      $.post(hide_url, function (response) {
                          if (response === 'Hidden') {
                            $.alert({
                                title: 'Hidden!',
                                content: 'This company has been hidden.',
                            });
                            $('.js_hideCompany').hide();
                            $('.js_activateCompany').show();
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

    // Activate company profile.
    $('.JSCompanyActions').on('click', '.js_activateCompany', function() {
        var hide_url = $(this).data('activate-url');
        var activate_button = $(this);
        $.confirm({
            title: 'Do you want to activate this company?',
            content: 'Company profile will activated.',
            buttons: {
                activate: {
                    btnClass: 'btn-primary',
                    action: function(){
                      $.post(hide_url, function (response) {
                          if (response === 'Active') {
                            $.alert({
                                title: 'Activated!',
                                content: 'This company has been activated.',
                            });
                            $('.js_hideCompany').show();
                            $('.js_activateCompany').hide();
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

    // Share company on twitter and facebook.
    $('.JSCompanyActions').on('click', '.JSShareCompany', function() {
        var share_url = $(this).data('share-url');
        var share_button = $(this);
        $.confirm({
            title: 'Do you want to share this company?',
            content: 'Company profile will be shared on QJane Twitter and Facebook pages.',
            buttons: {
                share: {
                    btnClass: 'btn-primary',
                    action: function(){
                      $.post(share_url, function (response) {
                          if (response === 'success') {
                            $.alert({
                                title: 'Shared!',
                                content: 'Company has been successfully shared on Twitter and Facebook pages!',
                            });
                            share_button.remove();
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

    // Share job on twitter and facebook.
    $('.JSJobActions').on('click', '.JSShareJob', function() {
        var share_url = $(this).data('share-url');
        var share_button = $(this);
        $.confirm({
            title: 'Do you want to share this job offer?',
            content: 'Job offer detail will be shared on QJane Twitter and Facebook pages.',
            buttons: {
                share: {
                    btnClass: 'btn-primary',
                    action: function(){
                      $.post(share_url, function (response) {
                          if (response === 'success') {
                            $.alert({
                                title: 'Shared!',
                                content: 'Job offer has been successfully shared on Twitter and Facebook pages!',
                            });
                            share_button.remove();
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
