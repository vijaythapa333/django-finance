from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages

# Create your views here.

def index(request):
    # Check whether preference is set or not
    preference_exist = UserPreference.objects.filter(user=request.user).exists()
    # Preference not set
    user_preference = None
    # Preference is set, so get the current preference
    if preference_exist:
        user_preference = UserPreference.objects.get(user=request.user)
    
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
        # To Open currencies.json file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        for key,value in data.items():
            currency_data.append({'name':key, 'value':value})

    # Python Debugger (Pause program herre)
    # import pdb
    # pdb.set_trace()
    context = {
        'currencies': currency_data,
        'user_preference': user_preference,
    }

    if request.method == 'GET':
        return render(request, 'preferences/index.html', context)
    
    elif request.method == 'POST':
        currency = request.POST['currency']

        if user_preference:
            # Update Preference
            user_preference.currency = currency
            user_preference.save()
        else:
            # Save new Preference
            UserPreference.objects.create(user=request.user, currency=currency)

        messages.success(request, "Preferences Saved.")
        return render(request, 'preferences/index.html', context)


