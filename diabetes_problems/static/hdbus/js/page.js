var Page = Backbone.Model.extend({
	initialize: function(){
		var model = this;
		$(document).ajaxComplete(function(event, request, settings){
			var data = request.responseJSON;
			if(data['messages']){
				// show any messages that got collected
			}
			if(data['redirect']){
				// set loading to true
				$.ajax({
					url:data['redirect']
				});
			}
			if(data['content']){
				var pane = $(data['content']).insertAfter($(".pane:last"));
				pane.hide();
				model.setPane(pane[0],pane.data("type"));
			}
		});
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