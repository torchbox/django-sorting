try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


def get_field(self):
    try:
        get = self.GET
        if 'sort' in get:
            field = get['sort']
        else:
            post = self.POST
            if 'sort' in post:
                field = post['sort']
            else:
                field = ''
    except AttributeError:
        field = ''
    return (self.direction == 'desc' and '-' or '') + field

def get_direction(self):
    try:
        get = self.GET
        if 'dir' in get:
            return get['dir']
        else:
            post = self.POST
            if 'dir' in post:
                return post['sort']
            else:
                return 'desc'
    except AttributeError:
        return 'desc'

class SortingMiddleware(MiddlewareMixin):
    """
    Inserts a variable representing the field (with direction of sorting)
    onto the request object if it exists in either **GET** or **POST** 
    portions of the request.
    """
    def process_request(self, request):
        request.__class__.field = property(get_field)
        request.__class__.direction = property(get_direction)
