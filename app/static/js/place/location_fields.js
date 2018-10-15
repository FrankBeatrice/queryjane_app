$(function () {
    $("#id_country").on("change", function () {
        var selected_country = $("#id_country option:selected");
        // Update country flag.
        var country_flag_url = $("#id_country_flag").data("url");
        $.get(country_flag_url, {country_id: selected_country.val()}, function(response) {
            $('#id_country_flag').attr('src', response);
        });

        // Change options in state input.
        $("#id_state").empty();
        $("#id_city").empty();

        var state_options_url = $("#id_state_field_container").data('get-options-url');

        $.get(state_options_url, {country_id: selected_country.val()}, function(response) {
            var options_number = response.length;

            for (var i = 0; i < options_number; i++) {
                var state_dict = response[i]
                
                var option = $('<option></option>').attr("value", state_dict.id).text(state_dict.name);
                
                $("#id_state").append(option);
            }
        });
    })

    $("#id_state").on("change", function () {
        var selected_state = $("#id_state option:selected");

        $("#id_city").empty();

        var city_options_url = $("#id_city_field_container").data('get-options-url');

        $.get(city_options_url, {state_id: selected_state.val()}, function(response) {
            var options_number = response.length;

            for (var i = 0; i < options_number; i++) {
                var city_dict = response[i]
                
                var option = $('<option></option>').attr("value", city_dict.id).text(city_dict.name);
                
                $("#id_city").append(option);
            }
        });
    })
})
