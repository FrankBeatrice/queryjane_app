function showPosition(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;

    var city_name = null;
    var state_long_name = null;
    var country_short_name = null;
    var location_dict = {};

    var ax_city_create_url = $('#id_QjaneVFcityAut').data('ax-city-create-url');


    $.ajax({
        type: 'GET',
        dataType: "json",
        url: "https://maps.googleapis.com/maps/api/geocode/json?latlng="+latitude+","+longitude+"&sensor=false",
        data: {},
        success: function(data) {
            var status = data['status'];
            var results = data['results'][0];

            if (status === "OK") {
                $.each(results['address_components'], function(i, val) {
                    if (val['types'] == "administrative_area_level_2,political") {
                        if (val['long_name']!="") {
                            city_name = val['long_name'];
                        }
                    }

                    if (city_name == null) {
                        if (val['types'] == "locality,political") {
                            if (val['long_name']!="") {
                                city_name = val['long_name'];
                            }
                        }
                    }

                    if (val['types'] == "administrative_area_level_1,political") {
                        if (val['long_name']!="") {
                            state_long_name = val['long_name'];
                        }
                    }

                    if (val['types'] == "country,political") {
                        if (val['short_name']!="") {
                            country_short_name = val['short_name'];
                        }
                    }
                });

                var coordinates = latitude + ',' + longitude;

                location_dict = {
                    'formatted_address': results['formatted_address'],
                    'city_name': city_name,
                    'state_long_name': state_long_name,
                    'country_short_name': country_short_name,
                    'coordinates': coordinates,
                }

                $.ajax({
                    url : ax_city_create_url,
                    type: "POST",
                    data: location_dict,
                    success:function(response){
                        if (response.status == 'success') {
                            var city_dict = response.city_dict;
                            $('#id_country_search').val(city_dict['country_name']);
                            $('#id_country_code').val(city_dict['country_code']);
                            $('#id_QjaneVFcountryAutImg').attr('src', city_dict['country_gif']);
                            $('#id_city_search').val(city_dict['city_name']);
                            $('#id_city_id').val(city_dict['city_id']);
                            $('#id_coordinates').val(location_dict['coordinates']);

                            var split_addres = location_dict['formatted_address'].split(',');
                            if(split_addres.length > 0) {
                                $('#id_address').val(split_addres[0]);
                            }

                            $('.QjaneShareGPSloading').hide();
                            $('.QjaneShareGPSfigure').show();
                        }
                    },
                });
            }
        },
        error: function () { console.log('error'); }
    });
}
