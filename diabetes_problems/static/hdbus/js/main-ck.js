$(document).ready(function(){$("form").delegate(".problem input","click",function(){this.checked?$(this).parents(".problem").addClass("problem-selected"):$(this).parents(".problem").removeClass("problem-selected")});$(".form-actions .container").prepend('<div class="selected-count"></div>');var e=function(){var e=$("form .problem input:checked").length,t=$("form .problem").length,n=$(".form-actions .selected-count");e==0?n.html("Please select a problem"):n.html(e+" of "+t+" problems")};$("form").delegate(".problem input","click",e);e()});