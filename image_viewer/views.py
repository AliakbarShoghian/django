# image_viewer/views.py

import base64
import glob
import os
import cv2
from django.shortcuts import render, get_object_or_404
from django.core.files.base import ContentFile
from django.http import HttpResponse
from .models import Image
from .forms import ImageForm
from django.conf import settings

def image_list(request):
    images = Image.objects.all()
    return render(request, 'image_viewer/image_list.html', {'images': images})

def image_detail(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, 'image_viewer/image_detail.html', {'image': image})

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
        
        # Convert the manipulated image to an in-memory file
        _, buffer = cv2.imencode('.png', manipulated_img)
        io_buf = ContentFile(buffer)

        # Convert to base64
        encoded_image = base64.b64encode(io_buf.read()).decode('utf-8')
        
        # Return the manipulated image as a base64 string
        return HttpResponse(f"data:image/png;base64,{encoded_image}")
    except Image.DoesNotExist:
        return HttpResponse("Image not found", status=404)

# def image_slideshow(request):
#     media_root = settings.MEDIA_ROOT
#     images = []

#     # Get a list of all files in the media directory
#     image_files = [f for f in glob.glob(os.path.join(media_root, 'images') + "/*.png")]
#     print('*' * 20)
#     print(len(image_files))
#     for filename in image_files:
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
#             images.append(filename)

#     return render(request, 'image_viewer/image_slideshow.html', {'images': images})

# def image_slideshow(request):
#     media_root = settings.MEDIA_ROOT
#     images = []

#     # Get a list of all files in the media/images directory
#     images_directory = os.path.join(media_root, 'images')

#     for filename in os.listdir(images_directory):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
#             images.append(os.path.join(images_directory, filename))

#     return render(request, 'image_viewer/image_slideshow_direct.html', {'images': images})

def image_slideshow(request):
    media_root = settings.MEDIA_ROOT
    images = []

    # Get a list of all files in the media/images directory
    images_directory = os.path.join(media_root, 'images')

    for filename in os.listdir(images_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = os.path.join(images_directory, filename)
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                images.append({'path': image_path, 'encoded': encoded_image})

    return render(request, 'image_viewer/image_slideshow_base64.html', {'images': images})