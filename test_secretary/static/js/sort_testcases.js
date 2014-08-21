$('.sortable').sortable();

$('.sortable').sortable().bind('sortupdate', function() {
    //Triggered when the user stopped sorting and the DOM position has changed.
    alert('updated');
});
