
$(document).ready(function() {

    // Use a timeout to auto-close alert messages after 3 seconds
    setTimeout(function() {
        // Find any alert message and close it
        $(".alert").each(function() {
            $(this).alert('close');
        });
    }, 3000);

    // Search functionality
    $('input[type="search"]').on('input', function() {
        var query = $(this).val().toLowerCase();
        $('table tbody tr').each(function() {
            var rowText = $(this).text().toLowerCase();
            if (rowText.indexOf(query) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});
