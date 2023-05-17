from django.shortcuts import render
import folium
from folium.plugins import FastMarkerCluster
from .models import EVChargingLocation


def ads(request):
    stations=EVChargingLocation.objects.all()

    #Create Folium maps
    m=folium.Map(location=(17.4067838,78.40936),zoom_start=9)

    for station in stations:
        coordinates=(station.latitude,station.longitude)
        folium.Marker(coordinates,popup=station.station_name).add_to(m)

    context = {
        'map': m._repr_html_()

    }
    return render(request, 'ads/ads.html', context)


    
"""     #add a marker to the map for each station
    for station in stations:
        coordinates=(station.latitude,station.longitude)
        folium.Marker(coordinates,popup=station.station_name).add_to(m)
    # use FaastMarkerCluster to generate the cclusters on the map
    # to this, we Pass list of all(lat,long) tuples in the data
    latitudes=[station.latitude for station in stations]
    longitudes=[station.longitude for station in stations]
    FastMarkerCluster(data=list(zip(latitudes,longitudes))).add_to(m)
 """    
