var panes = {};
var Pane = Backbone.View.extend({
	events:{
		'submit form':'getForm',
		'click .btn-ajax':'getLink',
		'mouseenter .problem':'problemOver',
		'mouseleave .problem':'problemOut',
	},
	initialize: function(){
		this.render();
		

	},
	render: function(){
		var view = this;
		// resize pane to display if needed
		
		this.$(".navbar-fixed-bottom").each(function(){
			var paddingBottom = Number(view.$el.css("padding-bottom").replace("px",""));
			view.$el.css("padding-bottom",paddingBottom+$(this).outerHeight()+"px");
		});
		
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
		}).always(function(data, textStatus){
			form.removeClass("loading");
			if(data.responseJSON) data = data.responseJSON;
			if(data['content']){
				if(form.data("target") == "pane"){
					var pane = $(data['content']).insertAfter(view.$el);
					view.$el.remove();
					view.setElement(pane[0]);
					view.render();
				}else{
					$(data['content']).insertAfter(form);
					form.remove();
				}
			}
		});
	},
	getLink: function(event){
		event.preventDefault();
		var view = this;
		var bttn = $(event.currentTarget)
		bttn.addClass("loading")
		this.model.loadPage(bttn.attr("href")).always(function(){
			bttn.removeClass("loading");
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
	},
	problemOver: function(event){
		var problem = $(event.currentTarget);
		problem.addClass("problem-hover");
	},
	problemOut: function(event){
		var problem = $(event.currentTarget);
		problem.removeClass("problem-hover");
	}
});

var ProblemPane = Pane.extend({
	'events':function(){
      return _.extend({},Pane.prototype.events,{
		'change .problem input':'toggleProblem',
      });
	},
	toggleProblem:function(event){
		if(event.currentTarget.checked){
			$(event.currentTarget).parent().addClass("problem-selected");
		}else{
			$(event.currentTarget).parent().removeClass("problem-selected");
		}
	},
});
panes['problems'] = ProblemPane;
