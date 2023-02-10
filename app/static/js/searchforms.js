$(document).ready(function() {
  $(".income-field").mask("000.000.000.000.000,00", { reverse: true })
  $("#id_installment").mask("000.000.000.000.000,00", { reverse: true })
  $("#id_min_value").mask("000.000.000.000.000,00", { reverse: true })
  $("#id_max_value").mask("000.000.000.000.000,00", { reverse: true })

  Array.prototype.slice
    .call(document.getElementsByClassName("birthday-field"))
    .forEach(function(element) {
      Array.prototype.slice.call(element).forEach(function(value) {
        value.innerText = value.innerText.replace(".", "")
      })
    })
})
