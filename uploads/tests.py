from django.test import TestCase
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

# Create your tests here.


class UploadFileTest(TestCase):

    def test_upload_valid_file(self):
        """
        Test that an image file uploaded returns a JSONResponse
        """
        myClient = Client()
        # mock the image upload
        image = SimpleUploadedFile(name='test_image.png', content=open(
            'mock_data/XYP_FR_XY89.png', 'rb'
        ).read(), content_type='image/png')

        # set up form data
        form_data = {'image': image}

        response = myClient.post(reverse('file_upload'), form_data, follow=True)

        # get the json response and verify it succeeds.
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"success": True, "result": ""})

    def test_upload_invalid_file(self):
        """
        Test that a file other than an image can't be uploaded.
        """
        myClient = Client()
        # mock the image upload
        image = SimpleUploadedFile(name='test_image.png', content=open(
            'mock_data/bad_file.PDF', 'rb'
        ).read())

        # set up form data
        form_data = {'image': image}

        response = myClient.post(reverse('file_upload'), form_data, follow=True)

        # assert that "upload a valid image" is in the httpresponse
        self.assertIn(b"Upload a valid image.", response.content)
