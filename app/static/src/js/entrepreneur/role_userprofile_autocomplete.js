$(function () {
    $.ajaxSetup({ 
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');

                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        } 
    });

    // User autocomplete
    var autocomplete_url = $('.qjane-userprofile-autocomplete-form').data('profile-autocomplete-url');
    var membership_line_url = $('.qjane-userprofile-autocomplete-form').data('membership-line-url');

    var profileSearch = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: autocomplete_url,
      remote: {
        url: autocomplete_url + '?q=%QUERY',
        wildcard: '%QUERY'
      }
    });

    var venture_slug = $('.qjane-venture-settings').data('venture-slug');

    $('#id_role-userprofile').typeahead({
        hint: true,
        highlight: true,
        minLength: 2
    }, {
      name: 'name',
      display: 'name',
      source: profileSearch
    }).on('keypress', function (event, object) {
        if (event.which === 13) {
            return false;
        }
    }).on('typeahead:autocompleted typeahead:selected', function (event, object) {
        $.post(membership_line_url, {'profile_id': object.id, 'venture_slug': venture_slug,}, function (response) {
            $('.qjane-venture-new-role-list-to-confirm').html(response.content);
            $('.qjane-cancel-role-search').removeClass('hide');

            return false;
        });
    });

    $('#id_role-userprofile').on('focus', function () {
        $('.qjane-add-membership-error').text('');
        $('.qjane-cancel-role-search').addClass('hide');
    });

    $('.qjane-role-search').on('click', '.qjane-cancel-role-search', function () {
        $('.qjane-venture-new-role-list-to-confirm').html('');
        $('#id_role-userprofile').val('').focus();
    });

    var send_role_inivtation_url = $('.qjane-userprofile-autocomplete-form').data('send-role-invitation-url');

    $('.qjane-venture-new-role-list-to-confirm').on('submit', '.qjane-send-membership-form', function () {
        $.post(send_role_inivtation_url, $(this).serialize(), function (response) {
            if (response === "fail") {
                $('.qjane-cancel-role-search').removeClass('hide');
                $('.qjane-add-membership-error').text('New search.');
                $('.qjane-venture-new-role-list-to-confirm').html('');
            } else if (response === "registered-membership") {
                $('.qjane-cancel-role-search').removeClass('hide');
                $('.qjane-add-membership-error').text('Membership previously created.');
                $('.qjane-venture-new-role-list-to-confirm').html('');
            } else {
                $('.qjane-venture-roles-list').append(response.content);
                $('.qjane-venture-new-role-list-to-confirm').html('');
                $('.qjane-cancel-role-search').addClass('hide');
                $('#id_role-userprofile').val('').focus();
            }
        });

        return false;
    });
})
