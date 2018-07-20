from django.views.generic import CreateView
from django.shortcuts import render
from .forms import ImageForm
from django.http import JsonResponse

from .models import Image
from cards.models import Card

from elasticsearch import Elasticsearch
from image_match.elasticsearch_driver import SignatureES

# Create your views here.


class UploadFileView(CreateView):
    template_name = "model_form_upload.html"
    form_class = ImageForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        es = Elasticsearch()
        ses = SignatureES(es, distance_cutoff=0.3)

        if form.is_valid():
            form.save()

            image = Image.objects.latest('uploaded_at')

            search = ses.search_image(image.image.path)

            print(search)

            if search:
                for result in search:
                    image_name_ext = result['path'].split('/')[-1::]
                    image_name = "".join(image_name_ext).split('.')[-2::][0]
                    print(image_name)

                if image_name:
                    card = Card.objects.get(unique_id=image_name)
                    res = card.unique_id

            else:
                res = ''

            context = {
                "result": res,
            }

            # compute from elasticsearch, return card page or error page

            return(JsonResponse(context))

        else:
            print("no")
            return render(request, self.template_name, {'form': form})
