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
		if(!this.$el.is(':visible')) this.show();
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
		var view = this;
		this.hide(function(){
			if(callback) callback();
			Backbone.View.prototype.remove.apply(view);
		});
	},
	show: function(callback){
		this.$el.show().css({
			'position':'absolute',
			'top':this.$el.height(),
			'width':this.$el.parent().width(),
		}).animate({
			'top':this.$el.css("margin-top"),
		},{
			'always':function(){
				if(callback) callback();
			}
		});
		this.$('.form-actions').each(function(){
			var menu = $(this);
			menu.css({
				'bottom':0-menu.height(),
			}).animate({
				'bottom':0,
			});
		});
		return this;
	},
	hide: function(callback){
		this.$('.form-actions').each(function(){
			var menu = $(this);
			menu.animate({
				'bottom':0-menu.height(),
			});
		});
		this.$el.css({
			'position':'absolute',
			'top':this.$el.css("margin-top"),
			'width':this.$el.parent().width(),
			'opacity':1,
		}).animate({
			'opacity':0,
			'top':0-this.$el.height(),
		},{
			'always':function(){
				if(callback) callback();
			}
		});
		return this;
	}
});

