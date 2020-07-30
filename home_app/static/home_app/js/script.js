$(function() {
    console.log("loaded !!");
    $('#search_form').submit(function(e){
        if ($("#items_to_search").val().length < 5){
            return false;
        }
    });
});
