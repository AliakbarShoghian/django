# image_viewer/views.py

import base64
import glob
import os
import cv2
from django.shortcuts import render, get_object_or_404
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
from .models import Image
from .forms import ImageForm
from django.conf import settings

def home(request):
    return render(request, 'image_viewer/home.html')

def manipulate_image(request, image_id):
    try:
        image_instance = Image.objects.get(pk=image_id)
        # Read the image
        image_path = image_instance.image.path
        img = cv2.imread(image_path)
        
        # Manipulate the image (example: convert to grayscale)
        manipulated_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Convert the original image to an in-memory file
        _, orig_buffer = cv2.imencode('.png', img)
        orig_io_buf = ContentFile(orig_buffer)
        original_encoded_image = base64.b64encode(orig_io_buf.read()).decode('utf-8')

        # Convert the manipulated image to an in-memory file
        _, mani_buffer = cv2.imencode('.png', manipulated_img)
        mani_io_buf = ContentFile(mani_buffer)
        manipulated_encoded_image = base64.b64encode(mani_io_buf.read()).decode('utf-8')

        # Prepare a dictionary with both images
        response_data = {
            'original_image': f"data:image/png;base64,{original_encoded_image}",
            'manipulated_image': f"data:image/png;base64,{manipulated_encoded_image}",
        }

        # Return the response with both images
        return JsonResponse(response_data)
    except Image.DoesNotExist:
        return HttpResponse("Image not found", status=404)


def image_slideshow(request):
    images = []
    return render(request, 'image_viewer/image_slideshow_base64.html', {'images': images})