    // register realty
    function updateCitiesRealtyRegister(pk) {
        if (pk.length == 0) {
            $("#update-realties.dynamic-city").html("");
            return
        }
        $.ajax({
            type: "GET",
            url: "/settings/get/cities/" + pk + "/",
            dataType: "json",
            beforeSend: function() {
                $("#update-realties").find(".dynamic-city").spin();
                $("#update-realties").find(".dynamic-city").html("");
            },
            success: function(content) {
                var json = $.parseJSON(content.object_list);
                $.each(json, function(index, value) {
                    $("#update-realties").find(".dynamic-city").append("\
                        <option value='" + value.pk + "'>" + value.fields.name + "</option>\
                        ");
                });
            },
            error: function(errormsg) {
                alert("Ocorreu um erro ao obter as cidades.");
            },
            complete: function() {
               $("#update-realties .dynamic-city").spin(false);
            }
        });
    }

    $("#update-realties .dynamic-state").change(function() {
        updateCitiesRealtyRegister(this.value);
    });
