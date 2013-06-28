$(function() {
    function split(val) {
        return val.split(/,\s*/);
    }

    function extractLast(term) {
        return split(term).pop();
    }

    $('input[name="tags"]').bind('keydown', function(event) {
        // Don't navigate away from the dropdown menu when it's in use:
        if (event.keyCode === $.ui.keyCode.TAB &&
                $(this).data('ui-autocomplete').menu.active) {
            event.preventDefault();
        }
    }).autocomplete({
        source: function(request, response) {
            $.post('/admin/tag_autocomplete/', {
                term: extractLast(request.term)
            }, response, 'json');
        },
        focus: function() {
           // Prevent the selected value from becoming the only value:
           return false;
        },
        select: function(event, ui) {
            var terms = split(this.value);
            terms.pop(); // remove the (potentially) incomplete input
            terms.push(ui.item.value); // add the selected tag
            this.value = terms.join(', ') + ', ';
            // Prevent the caret from scrolling off the edge of the input box:
            this.blur();
            this.focus();
            return false;
        }
    });
});
