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
                            hide_button.closest('.JSCompanyActions').find('.js_activateCompany').show();
                            hide_button.closest('.JSCompanyActions').find('.JSShareCompany').hide();
                            hide_button.hide();
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
                            activate_button.closest('.JSCompanyActions').find('.JSShareCompany').show();
                            activate_button.closest('.JSCompanyActions').find('.js_hideCompany').show();
                            activate_button.hide();
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

    // Hide job offer detail.
    $('.JSJobActions').on('click', '.js_hideJobOffer', function() {
        var hide_url = $(this).data('hide-url');
        var hide_button = $(this);
        $.confirm({
            title: 'Do you want to hide this job offer?',
            content: 'Job offer will be hidden for users.',
            buttons: {
                hide: {
                    btnClass: 'btn-primary',
                    action: function(){
                      $.post(hide_url, function (response) {
                          if (response === 'Hidden') {
                            $.alert({
                                title: 'Hidden!',
                                content: 'This job offer has been hidden.',
                            });
                            hide_button.closest('.JSJobActions').find('.js_activateJobOffer').show();
                            hide_button.closest('.JSJobActions').find('.JSShareJob').hide();
                            hide_button.hide();
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

    // Activate Job offer.
    $('.JSJobActions').on('click', '.js_activateJobOffer', function() {
        var hide_url = $(this).data('activate-url');
        var activate_button = $(this);
        $.confirm({
            title: 'Do you want to activate this job offer?',
            content: 'Job offer will activated.',
            buttons: {
                activate: {
                    btnClass: 'btn-primary',
                    action: function(){
                      $.post(hide_url, function (response) {
                          if (response === 'Active') {
                            $.alert({
                                title: 'Activated!',
                                content: 'This job offer has been activated.',
                            });

                            activate_button.closest('.JSJobActions').find('.JSShareJob').show();
                            activate_button.closest('.JSJobActions').find('.js_hideJobOffer').show();
                            activate_button.hide();
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
