
# url an parameters for the open food fact API
url = 'https://fr-en.openfoodfacts.org/cgi/search.pl'
params_off = {'search_simple': 1,
              'action': 'process',
              'json': 1,
              'page_size': 300,
              'page': 1,
              'tagtype_0': 'categories',
              'tag_contains_0': 'contains',
              'tag_0': 'cat',
              'tagtype_1': 'countries',
              'tag_contains_1': 'contains',
              'tag_1': 'france',
              'sort_by': 'unique_scans_n'
              }

# categories to fetch 
categories = ['biscuits',
              'Crepes',
              'desserts',
              'sweetened-beverages', ]
# brands to fecth to have well known products
brands = {'coca cola',
          'ferrero',
          'pepsi'}
# items per page for the paginator
NB_ITEMS_PAGE = 12
