from django import forms


class SearchView(forms.Form):
    """
        Serch form --> in the middle of the homepage : The form in the navbar is managed
        in the navbar
    """
    items_to_search = forms.CharField(label="", max_length=50, min_length=5, required=True)

    def __init__(self, *args, **kwargs):
        super(SearchView, self).__init__(*args, **kwargs)
        self.fields['items_to_search'].widget.attrs = {'id': "items_to_search",
                                                       'placeholder': "Search - min 5 chars"}
