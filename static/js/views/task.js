var TaskView = Backbone.View.extend({

    tagName: 'li',
    className: 'task-view',
    events: {
        'click [type="checkbox"]': 'doneChanged',
        'reordered' : 'reordered'
    },

    // When the user changes the order of a task item, it makes sense to notify
    // both TaskView and TasksView, so each one (the individual task and the
    // whole list) can do the appropriate action.
    reordered: function(event, index) {
        this.$el.trigger('update-order', [this.model, index]);
    },

    // Also, if the checkbox of an individual task is changed, TasksView needs
    // to know that to update the number of "items left".
    doneChanged: function(event) {
        this.model.save({'done': this.$("input")[0].checked}, {patch: true});
        this.$el.trigger('update-done');
        this.render();
    },

    render: function() {
        var done_attr;
        // Add "checked" only if the task id done.
        this.model.get('done') ? done_attr = 'checked' : done_attr = '';
        this.model.get('done') ? $(this.el).addClass("done-line") : $(this.el).removeClass("done-line");
        var task_html = '<input type="checkbox" class="form-checkbox" ' + done_attr + '/>'
                      + this.model.get('text')
                      + '<img id="move-icon" src="static/img/order.png" />';
        $(this.el).html(task_html);
        return this;
    }
});