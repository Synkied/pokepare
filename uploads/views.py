from django.views.generic import CreateView
from django.shortcuts import render
from .forms import ImageForm
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

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

        # specifying host for docker container,
        # the host must be the name of the docker container
        es = Elasticsearch(hosts=[{"host": settings.ELASTICSEARCH_HOST}])
        ses = SignatureES(es, distance_cutoff=0.3)

        try:

            if form.is_valid():
                form.save()

                image = Image.objects.latest('uploaded_at')

                search = ses.search_image(image.image.path)

                # print(search)

                if search:
                    for result in search:
                        image_name_ext = result['path'].split('/')[-1::]
                        image_name = "".join(image_name_ext).split('.')[-2::][0]
                        # print(image_name)

                    if image_name:
                        card = Card.objects.get(unique_id=image_name)
                        res = card.unique_id

                else:
                    res = ''

            else:
                # print("Form not valid.")
                return render(request, self.template_name, {'form': form})

        except ObjectDoesNotExist:
            res = ''

        context = {
            "success": True,
            "result": res,
        }

        return(JsonResponse(context))
