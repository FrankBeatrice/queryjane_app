from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from .models import CorporativeInfo


class CorporativeInfoDetail(DetailView):
    model = CorporativeInfo
    template_name = 'corporative/corporative_info_detail.html'

    def get_object(self, queryset=None):
        _object = get_object_or_404(
            CorporativeInfo,
            slug=self.kwargs['slug'],
        )

        return _object
