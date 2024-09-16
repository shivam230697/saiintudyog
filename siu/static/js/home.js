
$(document).ready(function() {

    setTimeout(function() {
        $(".alert").each(function() {
            $(this).alert('close');
        });
    }, 3000);


});
