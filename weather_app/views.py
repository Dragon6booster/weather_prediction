from django.shortcuts import render
from django.conf import settings
import requests
from .models import City
from .forms import CityForm
from datetime import datetime, timedelta


COUNTRY_NAMES = {
    "IN": "India",
    "US": "United States",
    "UK": "United Kingdom",
    "AE": "United Arab Emirates",
    "AU": "Australia",
    "CA": "Canada",
    "GB": "United Kingdom",
    "FR": "France",
    "DE": "Germany",
    "IT": "Italy",
    "JP": "Japan",
    "SG": "Singapore",
    "CN": "China",
    "BR": "Brazil",
    "RU": "Russia",
    "SA": "Saudi Arabia",
    "ZA": "South Africa",
    "KR": "South Korea",
    "MX": "Mexico",
    "ES": "Spain",
    "PT": "Portugal",
    "AR": "Argentina",
    "TR": "Turkey",
}

def home(request):

    API_KEY = settings.OPENWEATHER_API_KEY
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

    # If form submitted (POST) → save city
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()

    form = CityForm()

    cities = City.objects.all().order_by('-id')[:3]
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name, API_KEY)).json()

        # error handling: skip invalid cities
        if r.get("cod") != 200:
            continue  

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'country': COUNTRY_NAMES.get(r['sys']['country'],r['sys']['country']),
        }
        timezone_offset = r.get('timezone', 0)
        local_time = datetime.utcfromtimestamp(r['dt'] + timezone_offset)
        city_weather['time'] = local_time.strftime('%Y-%m-%d %H:%M:%S')


        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, "weather_app/home.html", context)




