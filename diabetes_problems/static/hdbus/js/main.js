$(document).ready(function(){
	$('form').delegate('.problem input','click',function(){
		if(this.checked){
			$(this).parents('.problem').addClass("problem-selected");
		}else{
			$(this).parents('.problem').removeClass("problem-selected");
		}
	});

	$('.form-actions .container').prepend('<div class="selected-count"></div>');
	var selected_count_update = function(){
		var selected = $('form .problem input:checked').length;
		var total =  $('form .problem').length;
		var update_div = $('.form-actions .selected-count');
		if(selected==0){
			update_div.html("Please select a problem");
		}else{
			update_div.html(selected+" of "+total+" problems");
		}
	}
	$('form').delegate('.problem input','click',selected_count_update);
	selected_count_update();

});