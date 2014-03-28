$(function() {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load
$(function() {

    $(window).bind("load", function() {
        console.log($(this).width())
        if ($(this).width() < 768) {
            $('div.sidebar-collapse').addClass('collapse')
        } else {
            $('div.sidebar-collapse').removeClass('collapse')
        }
    })
})

//Collapses the sidebar on window resize
$(function() {

    $(window).bind("resize", function() {
        console.log($(this).width())
        if ($(this).width() < 768) {
            $('div.sidebar-collapse').addClass('collapse')
        } else {
            $('div.sidebar-collapse').removeClass('collapse')
        }
    })
})



// Manejo del dropdwon de tareas


$(function () {
    $('.dropdown.keep-open').on({
        "shown.bs.dropdown": function() {
            $(this).data('closable', true);
        },
        "click": function() {
            $(this).data('closable', false);
        },
        "hide.bs.dropdown": function() {
            return $(this).data('closable');
        }
    });
});