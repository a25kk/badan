(function($) {
$(document).ready(function() {

$( ".jCarouselLite").jCarouselLite({
	visible:1, 
	btnNext: ".jCarouselLite  .next", 
	btnPrev: ".jCarouselLite .prev",
	circular: false,  
	afterEnd: function(a)
        {
            var index = $(a[0]).index() + 1;
            $('.carousel-info #current').html(index);
        }
});
});
}(jQuery));