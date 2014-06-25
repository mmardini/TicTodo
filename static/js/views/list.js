var TasksView = Backbone.View.extend({

    events: {
        'update-order': 'updateOrder',
        'update-done': 'updateDone',
        'mark-complete': 'markComplete' // Not used. Included for completeness.
    },

    initialize: function () {
        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(this.collection, 'add', this.render);
        this.collection.fetch({reset: true});
    },

    render: function() {
        this.$el.children().remove();
        this.updateDone();
        this.collection.each(this.renderTaskView, this);
        return this;
    },

    renderTaskView: function(model) {
        var el = new TaskView({model: model}).render().el;
        this.$el.append(el);
    },

    updateOrder: function(event, moved_model, new_position) {
        // We need to re-order only the models between the old position of the
        // moved model and the new one.
        var updatedOrders = {};
        var old_position = moved_model.get("order");
        var min_position = Math.min(old_position, new_position);
        var max_position = Math.max(old_position, new_position);

        // Remove the moved model, change its order, and re-add it at the new
        // position.
        this.collection.remove(moved_model);
        moved_model.set('order', new_position);
        updatedOrders[moved_model.get("id")] = new_position;
        this.collection.add(moved_model, {at: new_position});

        // Set order attribute of each model according to its new index in
        // collection, but don't change the order of the moved model since it's
        // already been set.
        this.collection.each(function (model, index) {
            if (index >= min_position && index <= max_position && index != new_position) {
                model.set('order', index);
                updatedOrders[model.get("id")] = index;
            }
        });

        // Update reordered models on the server. The submitted data has been
        // manually created to make it as short as possible.
        $.ajax({
            url: "/api/tasks/order/",
            type: 'PUT',
            data: updatedOrders
        });

        this.render();
    },

    updateDone: function() {
        var remaining_num = 0;
        this.collection.each(function (model) {
            if (model.get("done") == false) remaining_num += 1;
        });

        $("#remaining-num").text(String(remaining_num));
    },

    markComplete: function() {
        this.collection.each(function (model) {
            if (model.get("done") == false) {
                model.save({'done': true}, {patch: true});
            }
        });

        this.render();
    }
});