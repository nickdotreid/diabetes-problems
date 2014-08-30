var Page = Backbone.Model.extend({
	initialize: function(){
		var model = this;
		$(document).ajaxComplete(function(event, request, settings){
			var data = request.responseJSON;
			if(data['messages']){
				_.forEach(data['messages'],function(message){
					new Message({
						text:message.text,
						messageType:message.type,
					});
				});
			}
			if(data['redirect']){
				model.loadPage(data['redirect']);
			}
		});
	},
	loadPage: function(url){
		var model = this;
		var jqhxr = $.ajax({
			url:url,
		}).done(function(data){
			if(data['content']){
				var pane = $(data['content']).insertAfter($(".pane:last"));
				pane.hide();
				model.setPane(pane[0],pane.data("type"));
			}
		});
		return jqhxr;
	},
	setPane: function(div, type){
		var oldPane = this.get("currentPane");
		if(oldPane){
			var page = this;
			oldPane.remove(function(){
				page.set("currentPane", false);
				page.setPane(div, type);
			});
			return this;
		}

		var paneView = Pane;
		if(type && panes[type]) paneView = panes[type];
		var pane = new paneView({
			model:this,
			el:div,
		});
		this.set('currentPane', pane);
		this.listenTo(pane, 'pane-added', this.setPane);
		return this;
	}
});

var Message = Backbone.View.extend({
	events:{
		'click .close-btn':'handleClose',
	},
	initialize: function(options){
		this.text = options.text;
		this.messageType = options.messageType;
		this.render();
	},
	render: function(){
		var view = this;
		var messageDiv = $('<div class="alert alert-'+this.messageType+'">'+this.text+'<a href="#" class="close-btn close glyphicon glyphicon-remove"><span class="hidden">Close</span></a></div>').prependTo($('#alerts'));
		this.setElement(messageDiv);

		setTimeout(function(){
			view.hide();
		},5000);
		return this;
	},
	handleClose: function(event){
		event.preventDefault();
		this.hide();
	},
	hide: function(){
		var view = this;
		this.$el.animate({
			opacity:0
		},{
			always: function(){
				view.remove();
			}
		})
	}
});