var Task = Backbone.Model.extend({
	defaults: {
		order: 0,
		text: '',
        done: false
	},
    urlRoot: '/api/tasks/',
});