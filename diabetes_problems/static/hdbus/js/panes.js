var panes = {};
var Pane = Backbone.View.extend({
	events:{
		'submit form':'load',
		'click a':'get',
	},
	initialize: function(){

	},
	render: function(){

	},
	load: function(event){
		event.preventDefault();
		var form = event.currentTarget;
		$.ajax({

		});
	},
	get: function(event){
		if(event.currentTarget.href.indexOf("#") >= 0) return;
		event.preventDefault;
		$.ajax({

		});
	},
});