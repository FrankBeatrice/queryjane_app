// Dependencies
import './../new_layout.js';
import './../place/place_autocomplete.js';

// Images
import './../../img/venture_default_logo.svg';

$(function () {
    'use strict';

    // Clean filter
    $('#id_QJCleanVfilter').on('click', function () {
      $('#id_QJVfilterForm')[0].reset();
      $('#id_category').val('');
      $('#id_QJVfilterForm').submit();
    });

    // City autocomplete
    var company_autocomplete_url = $('#id_QjaneVListAut').data('ax-company-autocomplete-url');

    var companySearch = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: company_autocomplete_url,
      remote: {
        url: company_autocomplete_url + '?q=%QUERY',
        wildcard: '%QUERY'
      }
    });

    $('#id_company_search').typeahead({
        hint: true,
        highlight: true,
        minLength: 2
    }, {
      name: 'name',
      display: 'name',
      source: companySearch
    }).on('keypress', function (event, object) {
        if (event.which === 13) {
            return false;
        }
    }).on('typeahead:autocompleted typeahead:selected', function (event, object) {
        $('#id_company_id').val(object.id);
    });
})
