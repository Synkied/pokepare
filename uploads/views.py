import os

from cards.models import Card

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView

from elasticsearch import Elasticsearch

from image_match.elasticsearch_driver import SignatureES

from uploads.forms import ImageForm
from uploads.models import Image


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

                if search:
                    for result in search:
                        image_name_ext = result['path'].split('/')[-1::]
                        image_name = "".join(
                            image_name_ext
                        ).split('.')[-2::][0]
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

    def add_to_es(self, img_dir=""):

        es = Elasticsearch(hosts=[{"host": settings.ELASTICSEARCH_HOST}])
        ses = SignatureES(es, distance_cutoff=0.3)

        dirlist = os.listdir(img_dir)

        for file in dirlist:
            file_ext = "".join(file.split('.')[-1::])
            img_path = img_dir + file
            if file_ext in ('png', 'jpg'):
                print(img_path, 'added.')
                ses.add_image(img_path)
