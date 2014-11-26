__author__ = 'Alex'
import datetime
import operator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db.models import Q
from django.utils.decorators import method_decorator

import six

VALID_STRING_LOOKUPS = (
    'iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith',
    'iendswith', 'search', 'regex', 'iregex')


class LoginRequired(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequired, self).dispatch(request, *args, **kwargs)

class SearchableListMixin(object):
    """
    Filter queryset like a django admin search_fields does, but with little more intelligence:
    if self.search_split is set to True (by default) it will split query to words (by whitespace)
    Also tries to convert each word to date with self.search_date_formats and then search each word in separate field
    e.g. with query 'foo bar' you can find object with obj.field1__icontains='foo' and obj.field2__icontains=='bar'

    To provide custom lookup just set one of the search_fields to tuple,
    e.g. search_fields = [('field1', 'iexact'), 'field2', ('field3', 'startswith')]

    This class is designed to be used with django.generic.ListView

    You could specify query by overriding get_search_query method
    by default this method will try to get 'q' key from request.GET (this can be disabled with search_use_q=False)
    """
    search_fields = ['id']
    search_date_fields = None
    search_date_formats = ['%d.%m.%y', '%d.%m.%Y']
    search_split = True
    search_use_q = True
    check_lookups = True

    def get_context_data(self, **kwargs):
        context = super(SearchableListMixin, self).get_context_data(**kwargs)
        qs = self.model.objects.order_by('-pk')
        total_objects = qs.count()
        query = self.get_search_query()
        is_filter = False
        if query:
            is_filter = True
            w_qs = []
            search_pairs = self.get_search_fields_with_filters()
            for word in self.get_words(query):
                filters = [Q(**{'%s__%s' % (pair[0], pair[1]): word}) for pair in search_pairs]
                if self.search_date_fields:
                    dt = self.try_convert_to_date(word)
                    if dt:
                        filters.extend([Q(**{field_name: dt}) for field_name in self.search_date_fields])
                w_qs.append(reduce(operator.or_, filters))
            qs = qs.filter(reduce(operator.and_, w_qs))
            qs = qs.distinct()
        paginator = Paginator(qs, 10)
        page = self.request.GET.get('page')
        try:
            qs = paginator.page(page)
        except PageNotAnInteger:
            qs = paginator.page(1)
        except EmptyPage:
            qs = paginator.page(paginator.num_pages)
        context.update({'object_list': qs, 'is_filter': is_filter, 'total_objects': total_objects})
        return context

    def get_words(self, query):
        if self.search_split:
            return query.split()
        return [query]

    def get_search_fields_with_filters(self):
        fields = []
        for sf in self.search_fields:
            if isinstance(sf, six.string_types):
                fields.append((sf, 'icontains', ))
            else:
                if self.check_lookups and sf[1] not in VALID_STRING_LOOKUPS:
                    raise ValueError('Invalid string lookup - %s' % sf[1])
                fields.append(sf)
        return fields

    def try_convert_to_date(self, word):
        """
        Tries to convert word to date(datetime) using search_date_formats
        Return None if word fits no one format
        """
        for frm in self.search_date_formats:
            try:
                return datetime.datetime.strptime(word, frm).date()
            except ValueError:
                pass
        return None

    def get_search_query(self):
        """
        Get query from request.GET 'q' parameter when search_use_q is set to True
        Override this method to provide your own query to search
        """
        return self.search_use_q and self.request.GET.get('q', '') or None


