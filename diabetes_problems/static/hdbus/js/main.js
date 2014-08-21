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

var page = new Page();
$(document).ready(function(){
	$(".pane:first").forEach(function(){
		var pane = $(this);
		page.setPane(this, pane.data("type"));
	});
});