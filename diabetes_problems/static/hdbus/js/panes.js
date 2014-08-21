var panes = {};
var Pane = Backbone.View.extend({
	events:{
		'submit form':'getForm',
		'click .btn-ajax':'getLink',
	},
	initialize: function(){

	},
	render: function(){

	},
	getForm: function(event){
		event.preventDefault();
		var form = $(event.currentTarget);
		$.ajax({
			type:form.attr("method"),
			url:form.attr("action"),
			data:form.serialize(),
		});
	},
	getLink: function(event){
		event.preventDefault();
		var bttn = $(event.currentTarget)
		$.ajax({
			url:bttn.attr("href"),
		});
	},
});