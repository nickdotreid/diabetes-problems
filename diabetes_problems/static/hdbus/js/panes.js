var panes = {};
var Pane = Backbone.View.extend({
	events:{
		'submit form':'getForm',
		'click .btn-ajax':'getLink',
	},
	initialize: function(){
		this.paneShow();
		

	},
	render: function(){
		
	},
	getForm: function(event){
		event.preventDefault();
		var view = this;
		var form = $(event.currentTarget);
		form.addClass("loading");
		$.ajax({
			type:form.attr("method"),
			url:form.attr("action"),
			data:form.serialize(),
			error: function(jqXHR){

			},
			done: function(){
				form.removeClass("loading");
			},
		});
	},
	getLink: function(event){
		event.preventDefault();
		var view = this;
		var bttn = $(event.currentTarget)
		bttn.addClass("loading")
		$.ajax({
			url:bttn.attr("href"),
			success:function(data){

			},
			done:function(){
				bttn.removeClass("loading");
			}
		});
	},
	paneRemove: function(){
		this.$el.addClass("");

		var view = this;
		//view.remove();
		// setTimeout(function(){
		// view.remove();
		// }, 1500);
	},
	paneShow: function(){
		this.$el.show();
	}
});