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

/*
$('.dropdown-menu').click(function(event){
     event.stopPropagation();
 });
*/

$('.dropdown.keep-open').on('hide.bs.dropdown', function () {
    return false;
});

$(document).click(function() {
	$(".dropdown.keep-open").toggleClass('open')
});

$(".dropdown-menu.dropdown-tasks").click(function(event) {
    event.stopPropagation();
});