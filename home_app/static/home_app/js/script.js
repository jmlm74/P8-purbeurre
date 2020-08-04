$(function() {
    $('#search_form').submit(function(e){
        if ($("#items_to_search").val().length < 5){
            return false;
        }
    });
    $("#items_to_search").autocomplete({
        source: "/autocomplete_search",
        minLength: 4,
        delay: 400,
        autoFocus: true
      });
});
