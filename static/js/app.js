var AppRouter = Backbone.Router.extend({
	initialize: function  () {
		this.tasks = new Tasks();

		this.tasksView = new TasksView({
		    el: '#tasks-view',
		    collection: this.tasks
		});
	},
});

var app = new AppRouter();

$(function() {
	$("#tasks-view").sortable({
		update: function(event, ui) {
            ui.item.trigger('reordered', ui.item.index());
        }
	});
	Backbone.history.start();
});

$("#new-task-button").click(function() {
	if ($('#new-task-text').val() != "") {

		// Create a new task using the entered text and and an order number
		// that puts the task at the end of tasks queue.
		var new_task = new Task({
			text: $('#new-task-text').val(),
			order: app.tasks.length,
			done: false
		});

		new_task.save();
		app.tasks.add(new_task);

		$('#new-task-text').val("");
	}
});

$('#new-task-text').keyup(function(e){
	if(e.keyCode == 13)
	{
	  $("#new-task-button").trigger("click");
	}
});

$("#mark-items").click(function() {
	app.tasksView.markComplete();
});