from rest_framework import generics, viewsets
from .models import Lawyer,Booking,Review
from mouhami_api.models import Language, Lawyer, Specialities
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import random
from .serializers import LawyerSerializer,BookingSerializer,ReviewSerializer,LanguageSerializer, SpecialitiesSerializer
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Lawyer
from .serializers import LawyerSerializer



@api_view(['POST'])
def lawyerData(request):
    with open('cabinets.json', 'r', encoding='utf-8') as json_file:
        cabinets_data = json.load(json_file)
    all_languages=[]
    if request.method == 'POST':
        Language.objects.create(name='arabic')
        Language.objects.create(name='french')
        Language.objects.create(name='english')
        for data in cabinets_data:
            specialities_data = data.get('categories', [])
            for language in Language.objects.all():
                all_languages.append(language)

            num_languages_to_select = random.randint(1, min(2, len(Language.objects.all())))
            languages_data = random.sample(all_languages, num_languages_to_select)
            language_instances = []
            for lang in languages_data:
                
                language_instance= Language.objects.get(name=lang.name)
                language_instances.append(language_instance)

            speciality_instances = []
            for speciality_name in specialities_data:
                speciality_instance, created = Specialities.objects.get_or_create(name=speciality_name)
                speciality_instances.append(speciality_instance)

            lawyer_data = {
                'name': f"{data.get('name', '')} {data.get('fname', '')}",
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'photo': data.get('avocat_image', ''),
                'location': data.get('address', ''),
                'lng': data.get('longitude', 0.0),
                'lat': data.get('latitude', 0.0),
                'rating': data.get('rating', 0.0),
            }

            lawyer_instance = Lawyer.objects.create(**lawyer_data)

            lawyer_instance.languages.set(language_instances)
            lawyer_instance.specialities.set(speciality_instances)

        return Response({"data inserted to the database successfully!!"})
 
@api_view(['POST'])
def searchLawyer(request):
    if request.method == 'POST':
        name = request.data.get('lawyerName', '')
        wilaya = request.data.get('wilaya', '')
        langue = request.data.get('language', '')
        categories_str = request.data.get('specialities', '') 
        categories = [category.strip() for category in categories_str.split(',') if category.strip()]
        lawyer_list = Lawyer.objects.all()
        lawyer_list = lawyer_list.filter(
            Q(name__icontains=name) &
            Q(languages__name__icontains=langue)
        )

        # Check if wilaya is "Alger"
        if wilaya.lower() == 'alger':
            lawyer_list = lawyer_list.exclude(location__icontains='Algérie')
        else:
            # Filter lawyers based on the provided wilaya
            lawyer_list = lawyer_list.filter(location__icontains=wilaya)

        # Filter Lawyer objects by each category using the "and" condition
        for category in categories:
            lawyer_list = lawyer_list.filter(specialities__name=category)

        # Serialize the queryset of Lawyer objects
        serializer = LawyerSerializer(lawyer_list.distinct(), many=True)

        # Return serialized data as a response
        return Response(serializer.data)




