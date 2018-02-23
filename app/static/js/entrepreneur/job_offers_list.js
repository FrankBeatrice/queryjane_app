$(function () {
    'use strict';

    // Clean filter
    $('#id_QJCleanJOfilter').on('click', function () {
      $('#id_QJJOfilterForm')[0].reset();
      $('#id_category').val('');
      $('#id_job_type').val('');
      $('#id_QJJOfilterForm').submit();
    });

    // City autocomplete
    var venture_autocomplete_url = $('#id_QjaneVListAut').data('ax-ventury-autocomplete-url');

    var ventureSearch = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: venture_autocomplete_url,
      remote: {
        url: venture_autocomplete_url + '?q=%QUERY',
        wildcard: '%QUERY'
      }
    });

    $('#id_venture_search').typeahead({
        hint: true,
        highlight: true,
        minLength: 2
    }, {
      name: 'name',
      display: 'name',
      source: ventureSearch
    }).on('keypress', function (event, object) {
        if (event.which === 13) {
            return false;
        }
    }).on('typeahead:autocompleted typeahead:selected', function (event, object) {
        $('#id_venture_id').val(object.id);
    });
})
