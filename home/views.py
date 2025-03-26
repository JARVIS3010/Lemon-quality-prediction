from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    # return HttpResponse("This is our home page")
    return render(request, 'index.html')

def about(request):
    # return HttpResponse("This is our about page")
    return render(request, 'about.html')

def prediction(request):
    # return HttpResponse("This is our prediction page")
    return render(request, 'prediction.html')

def contact(request):
    # return HttpResponse("This is our contact page")
    return render(request, 'contact.html')

def login(request):
    # return HttpResponse("This is our login page")
    return render(request, 'login.html')

def registration(request):
    # return HttpResponse("This is our registration page")
    return render(request, 'registration.html')






from django.shortcuts import render
from django.http import JsonResponse
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import os
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

#LOAD MODEL
MODEL_PATH = os.path.join(os.path.dirname(__file__), "lemon.keras")
model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(img_path):
    img = load_img(img_path, target_size=(300, 300))  # Match model training size
    img_array = img_to_array(img)

    print("Before normalization:", np.max(img_array), np.min(img_array))  # Debugging

    img_array = np.expand_dims(img_array, axis=0)

    # Check if model expects normalization
    # img_array /= 255.0  # If images were normalized in training
    print("After normalization:", np.max(img_array), np.min(img_array))  # Debugging

    return img_array


@csrf_exempt  # This temporarily disables CSRF for this view (not recommended for production)
def prediction(request):
    if request.method == "POST" and request.FILES.get("image"):
        uploaded_file = request.FILES["image"]
        file_path = default_storage.save("temp.jpg", uploaded_file)
        full_path = os.path.join(default_storage.location, file_path)

        # Preprocess Image
        img_array = preprocess_image(full_path)

        # Get Predictions
        prediction = model.predict(img_array)

        # Debugging: Print full class probabilities
        print("Raw model output (probabilities):", prediction)  

        predicted_class = np.argmax(prediction, axis=1)[0]  # Get highest probability class

        # Print confidence score for debugging
        print("Confidence score:", prediction[0][predicted_class])

        # Check probability values
        print("Predicted class index:", predicted_class)

        # Define class labels (Make sure these are correct)
        class_labels = ['bad_quality', 'empty_background', 'good_quality']
        print("Mapped class:", class_labels[predicted_class])

        result = class_labels[predicted_class]

        return JsonResponse({"prediction": result})  # Ensures JSON response

    return render(request, "prediction.html", {"prediction": None})

