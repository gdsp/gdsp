/*! Some custom scripts */

/*! Simple Tabs */
$(document).ready(function() {
    $(".tabs-menu a").click(function(event) {
        event.preventDefault();
        $(this).parent().addClass("current");
        $(this).parent().siblings().removeClass("current");
        var tab = $(this).attr("href");
        $(".tab-content").not(tab).css("display", "none");
        $(tab).fadeIn();
    });
});


$(document).ready(function() {
	$('.bxslider-utfordring').bxSlider({
	  pagerCustom: '#bx-pager-utfordring',
	  infiniteLoop: false
	});
});
