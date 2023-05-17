from django.core.management.base import BaseCommand
from ads.models import  Countrycode,CityCode,LocationCode,SubLocationCode,CategoryCode



class Command(BaseCommand):
    help = 'Load Countrycode and City'

    def handle(self, *args, **kwargs):
        Countrycode.objects.all().delete()
        countrycode_names = [
            'India', 'USA', 'Pakistan', 'China'
        ]

        if not Countrycode.objects.count():
            for Countrycode_name in countrycode_names:
                Countrycode.objects.create(name=Countrycode_name)

        # Computer Science
        cs = Countrycode.objects.get(name='India')

        city_modules = [
            'Hyderabad',
            'Delhi',
            'Bangalore',
            'Chennai', 
            'Kolkatta'
        ]

        for module in city_modules:
            CityCode.objects.create(name=Countrycode, CityCode=cs)

        # Maths
        hyd = Countrycode.objects.get(name='Hyderabad')
        math_modules = [
            'Linear Algebra',
            'Differential Equations',
            'Graph Theory',
            'Topology',
            'Number Theory'
        ]

        for module in math_modules:
            Module.objects.create(name=module, course=hyd)

        # PHYSICS
        physics = Course.objects.get(name='Physics')
        physics_modules = [
            'Quantum Mechanics',
            'Optics',
            'Astronomy',
            'Solid State Physics',
            'Electromagnetic Theory'
        ] 
        for module in physics_modules:
            Module.objects.create(name=module, course=physics)

        # Film
        film = Course.objects.get(name='Film Studies')

        film_modules = [
            'Film Noir',
            'Silent Cinema',
            'American Independent Cinema',
            'Avant-Garde Cinema',
            'Scriptwriting'
        ]

        for module in film_modules:
            Module.objects.create(name=module, course=film)