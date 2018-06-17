from dal import autocomplete

from .models import Country


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Country.objects.all().order_by("text")
        if self.q:
            qs = qs.filter(text__istartswith=self.q)
        return qs