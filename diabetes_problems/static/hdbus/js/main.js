$(document).ready(function(){
	$('form').delegate('.problem input','click',function(){
		if(this.checked){
			$(this).parents('.problem').addClass("problem-selected");
		}else{
			$(this).parents('.problem').removeClass("problem-selected");
		}
	});
});