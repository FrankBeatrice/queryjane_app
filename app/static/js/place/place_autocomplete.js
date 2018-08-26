$(function () {
    'use strict';
    // Country autocomplete
    var country_autocomplete_url = $('#id_QjaneVFcountryAut').data('country-autocomplete-url');

    var CountrySearch = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: country_autocomplete_url,
      remote: {
        url: country_autocomplete_url + '?q=%QUERY',
        wildcard: '%QUERY'
      }
    });

    $('#id_country_search').typeahead({
        hint: true,
        highlight: true,
        minLength: 2
    }, {
      name: 'name',
      display: 'name',
      source: CountrySearch
    }).on('keypress', function (event, object) {
        if (event.which === 13) {
            return false;
        }
    }).on('typeahead:autocompleted typeahead:selected', function (event, object) {
        $('#id_country_code').val(object.code);
        $('#id_QjaneVFcountryAutImg').attr('src', object.flag);

        $('#id_city_search').val('');
        $('#id_city_id').val('');
    });


    // City autocomplete
    var city_autocomplete_url = $('#id_QjaneVFcityAut').data('ax-city-autocomplete-url');

    var CitySearch = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: city_autocomplete_url,
      remote: {
        url: city_autocomplete_url + '?q=%QUERY',
        wildcard: '%QUERY'
      }
    });

    $('#id_city_search').typeahead({
        hint: true,
        highlight: true,
        minLength: 2
    }, {
      name: 'name',
      display: 'name',
      source: CitySearch
    }).on('keypress', function (event, object) {
        if (event.which === 13) {
            return false;
        }
    }).on('typeahead:autocompleted typeahead:selected', function (event, object) {
        $('#id_city_id').val(object.id);
    });
})
