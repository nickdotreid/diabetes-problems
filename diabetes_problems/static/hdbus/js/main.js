var Page = Backbone.Model.extend({
	setPane: function(div, type){
		var paneView = Pane;
		if(type && panes[type]) paneView = panes[type];
		var pane = new Pane({
			model:this,
			el:div,
		});
		this.set('currentPane', pane);
	}
});