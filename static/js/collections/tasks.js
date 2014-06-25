var Tasks = Backbone.Collection.extend({
	comparator: 'order',
	model: Task,
	url: '/api/tasks/'
});