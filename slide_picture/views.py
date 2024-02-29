from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from slide_picture.models import Slide


# Create your views here.
class PictureListView(ListView):
    model = Slide
    paginate_by = 1
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PictureListView, self).get_context_data(*args, **kwargs)
        context['slide'] = Slide.objects.all()
        return context
