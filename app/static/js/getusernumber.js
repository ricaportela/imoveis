function getNumber(pk, state) {
    console.log('state')
    $.ajax({
        type: "GET",
        url: "/" + state + "/imoveis/user/get/number/" + pk + "/",
        dataType: "json",
        beforeSend: function() {
            $("#realty-panel-details").spin();
        },
        success: function(content) {
            var json = $.parseJSON(content.advertiser_number);
            $.each(json, function(index, value) {
                $("#phone-number").html(value);
            });
        },
        error: function(errormsg) {
            alert("Ocorreu um erro ao obter o número de telefone.");
        },
        complete: function() {
           $("#realty-panel-details").spin(false);
        }
    });
}
