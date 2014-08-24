var panes = {};
var Pane = Backbone.View.extend({
	events:{
		'submit form':'getForm',
		'click .btn-ajax':'getLink',
	},
	initialize: function(){
		this.render()
	},
	render: function(){
		// resize pane to display if needed
		
		// if div not visable
		this.show();
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
			done:function(){
				bttn.removeClass("loading");
			}
		});
	},
	remove: function(callback){
		this.hide(callback);
		Backbone.View.prototype.remove.apply(this);
	},
	show: function(callback){
		this.$el.show();
		if(callback) callback();
		return this;
	},
	hide: function(callback){
		this.$el.hide();
		if(callback) callback();
		return this;
	}
});