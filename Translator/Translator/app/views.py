"""
Definition of views.
"""
from googletrans import Translator
import requests
from pathlib import Path
import os
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )



def image(request):
    assert isinstance(request, HttpRequest)
    message = "Please upload an image."
    message2 = ""
    imag = ""
    if request.method == 'POST':
        uploaded_file = request.FILES['document']

        imag = "C:/Users/wade2/Desktop/"
        caption = getCaption(imag + uploaded_file.name)
        message = "Original Message: " + caption 
        lang = request.POST["language"]
        message2 = "Translated Message: " + convertString(caption, lang)


    return render(
        request,
        'app/image.html',
        {
            'title':'Image Description',
            'message': message,
            'message2': message2,
            'imag': imag,
            'year':datetime.now().year,
        }
    )


def pdf(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/pdf.html',
        {
            'title':'Pdf',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def output(request):
    
    subscription_key = "6b323e78db8c44818721272ad3e37a73"
    assert subscription_key
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
    analyze_url = vision_base_url + "analyze"
    image_path = "C:/Users/wade2/Desktop/alej.jpg"

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                  'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()

    print(analysis)
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()

    # Display the image and overlay it with the caption.
    image = Image.open(BytesIO(image_data))
    plt.imshow(image)
    plt.axis("off")
    _ = plt.title(image_caption, size="x-large", y=-0.1)
    return render(
        'app/image.html',
        {
            'title':'About',
            'message': "test",#analysis,
            'year':datetime.now().year,
        }
    )



def getCaption(file):
    subscription_key = "6b323e78db8c44818721272ad3e37a73"
    assert subscription_key

    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"

    analyze_url = vision_base_url + "analyze"

    # Set image_path to the local path of an image that you want to analyze.
    image_path = file

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                  'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    print(analysis)
    image_caption = analysis["description"]["captions"][0]["text"]#.capitalize()

    # Display the image and overlay it with the caption.
    image = Image.open(BytesIO(image_data))
    plt.imshow(image)
    plt.axis("off")
    _ = plt.title(image_caption, size="x-large", y=-0.1)
    return image_caption
   
def convertString(original_str, desired_lang):
    translator = Translator()
    translated_text = str(translator.translate(original_str, src ='en',
                          dest=desired_lang).text)
    return translated_text