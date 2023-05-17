from urllib.parse import uses_relative
from accounts.models import UserProfile
#from vendor.models import Vendor
from django.conf import settings

def get_owner(request):
    try:
        owner = owner.objects.get(user=request.user)
    except:
        owner = None
    return dict(owner=owner)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)



def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}


def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID}