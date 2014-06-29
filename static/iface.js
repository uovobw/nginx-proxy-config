$(document).ready(function() {
    $('.ssl-inputs').hide();
    $('.enable-ssl').click(function () {
        if($(this).is(':checked')){
           $('.ssl-inputs').show();
        }else{
           $('.ssl-inputs').hide();
        }
    });
    if (typeof(do_show) !== "undefined") {
        $('.ssl-inputs').show();
    }
});

$(".remover").click(
    function () {
        $(this).closest("table").remove();
    }
);

