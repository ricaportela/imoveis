$(document).ready(function() {

    // Simulators on sidebar
    function updateCitiesSidebar(pk) {
        if (pk.length == 0) {
            $("#simuladores").find(".dynamic-city").html("");
            return
        }
        $.ajax({
            type: "GET",
            url: "/settings/get/cities/" + pk + "/",
            dataType: "json",
            beforeSend: function() {
                $("#simuladores").find(".dynamic-city").spin();
                $("#simuladores").find(".dynamic-city").html("");
            },
            success: function(content) {
                var json = $.parseJSON(content.object_list);
                $.each(json, function(index, value) {
                    $("#simuladores").find(".dynamic-city").append("\
                        <option value='" + value.pk + "'>" + value.fields.name + "</option>\
                        ");
                });
            },
            error: function(errormsg) {
                alert("Ocorreu um erro ao obter as cidades.");
            },
            complete: function() {
               $("#simuladores").find(".dynamic-city").spin(false);
            }
        });
    }

    $("#simuladores").find(".dynamic-state").change(function() {
        updateCitiesSidebar(this.value);
    });

    setTimeout(function () {
        var state = $('#simuladores').find('.dynamic-state').find(":selected").attr('value');
        updateCitiesSidebar(state);
    }, 100);
    setTimeout(function() {
        var city = getURLParameter('city');
        if (city != null) {
            $('#simuladores').find('.dynamic-city').find('option[value=' + city + ']').attr('selected', true);
        }
    }, 1000);



    // Simulator on page

    function updateCitiesPage(pk) {
        if (pk.length == 0) {
            $("#page-simulator.dynamic-city").html("");
            return
        }
        $.ajax({
            type: "GET",
            url: "/settings/get/cities/" + pk + "/",
            dataType: "json",
            beforeSend: function() {
                $("#page-simulator .dynamic-city").spin();
                $("#page-simulator .dynamic-city").html("");
            },
            success: function(content) {
                var json = $.parseJSON(content.object_list);
                $.each(json, function(index, value) {
                    $("#page-simulator .dynamic-city").append("\
                        <option value='" + value.pk + "'>" + value.fields.name + "</option>\
                        ");
                });
            },
            error: function(errormsg) {
                alert("Ocorreu um erro ao obter as cidades.");
            },
            complete: function() {
               $("#page-simulator .dynamic-city").spin(false);
            }
        });
    }

    $("#page-simulator .dynamic-state").change(function() {
        updateCitiesPage(this.value);
    });

});
