$(document).ready(function(){
	$('form').delegate('.problem input','click',function(){
		if(this.checked){
			$(this).parents('.problem').addClass("problem-selected");
		}else{
			$(this).parents('.problem').removeClass("problem-selected");
		}
	});

	$('.form-actions .container').prepend('<div class="selected-count navbar-text pull-left"></div>');
	var selected_count_update = function(){
		var selected = $('form .problem input:checked').length;
		var total =  $('form .problem').length;
		var update_div = $('.form-actions .selected-count');
		update_div.html(selected+" of "+total+" problems");
	};
	$('form').delegate('.problem input','click',selected_count_update);
	selected_count_update();

	$(".sortable").each(function(){
		var list = $(this);
		var reposition = function(){
			$('input.position',list).each(function(index){
				$(this).val(index+1);
			});
		}
		list.sortable();
		list.on('sortupdate',function(event, ui){
			reposition();
		});
	});

});