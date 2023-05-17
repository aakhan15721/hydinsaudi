import json
from .forms import ExpatadForm,ContactmeForm,InterestedForm
from django.shortcuts import render, redirect,get_object_or_404,redirect,HttpResponseRedirect
from .models import Expatad, Category,ExpatImage,Contactme,Countrycode,CityCode,Interested,Purpose #ReviewRating, ProductGallery
from django.contrib.auth.models import User
from main.filters import Expatadfilter

from django.db.models import Q


from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.utils import send_mail,send_notification
from django.contrib.sites.shortcuts import get_current_site

from django.db import transaction

from main.filters import Expatadfilter
def expads(request, slug=None):
    categories = None
    expatads = None
    if slug != None:
        categories = get_object_or_404(Category, slug=slug)
        #print(categories)
        #expatads = Expatad.objects.filter(category=categories, is_active=True)
        expatad_filter = Expatadfilter(request.GET, queryset=Expatad.objects.all().filter(category=categories,is_active=True))
        expatads = expatad_filter.qs
        paginator = Paginator(expatads, 10)
        page = request.GET.get('page')
        paged_expatads = paginator.get_page(page)
        expatad_count = expatads.count()
    else:
        expatad_filter = Expatadfilter(request.GET, queryset=Expatad.objects.all().filter(is_active=True))
        expatads = expatad_filter.qs
        paginator = Paginator(expatads, 10)
        page = request.GET.get('page')
        paged_expatads = paginator.get_page(page)
        expatad_count = expatads.count()
    context = {
        'expatads': paged_expatads,
        'expatad_count': expatad_count,
        'form' : expatad_filter.form,
        'expatads_list': expatad_filter.qs,
    }
    return render(request, 'home.html', context)

def expataddetail(request,id):
    expatads = get_object_or_404(Expatad,id=id) 
    expatImage_list =ExpatImage.objects.filter(expatads=expatads).prefetch_related('expatads')
    #print(request.user)
    #print(expatads.user)
    if request.user==expatads.user:
        uservalue=True
    else:
        uservalue=False
    #ExpatImage.objects.filter(ExpatImage=Expatad)
    #ExpatImage.objects.filter(ExpatImage=Expatad).prefetch_related('vehiclepart_set')
    #expatImage_list = ExpatImage.objects.filter(id=expatads.id)
    #print(expatImage_list.images)
    #print(expatads.id)
    #print(uservalue)
    context = {'expatads':expatads,'expatImage_list': expatImage_list,'uservalue':uservalue}
    return render(request, 'expads/expataddetail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            expads = Expatad.objects.order_by('-created').filter(Q(Description__icontains=keyword) | Q(fullname__icontains=keyword))
            expad_count = expads.count()
            print("Found")
    context = {
        'expatads': expads,
        'expatad_count': expad_count,
    }
    return render(request, 'home.html', context)


def contactme(request):
    context = {

        }
    return render(request, 'expads/contactme.html', context)

def contactyou(request):
    context = {

        }    
    return render(request, 'expads/contactyou.html', context)

def contactmes(request):
#    obj = get_object_or_404(Contactme, id = id)
    form = ContactmeForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = ContactmeForm(request.POST)
        email = form.data['email']
        request.POST._mutable = True
        #user = User.objects.get(id=request.data['user']) # that is if you are sending the use Id from the frontend
        form.data['user']=request.user
        form.data['is_followed']=False
        if form.is_valid():
            form.save()
            mail_subject = 'We have received your Email'
            email_template = 'accounts/emails/contactusconfirm.html'
            #send_confirm_email(request, contactus, mail_subject, email_template)
            print(Contactme)
            send_mail(mail_subject,'We received Your message Here is acknowledgment Thanks','aakhan1572@gmail.com',[email],fail_silently=False,)
            messages.success(request, 'We have received your message sucessfully!')
            return redirect('contactmes')

    if not request.user.is_authenticated:
        messages.success(request, 'Please login')
        return render(request, 'accounts/login.html')
    context = {'form': form}
    return render(request, 'expads/contactmes.html', context)

def interested(request,id):
    expatads = get_object_or_404(Expatad,id=id) 
    form = InterestedForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = InterestedForm(request.POST)
        email = form.data['email']
        mobilenumber=expatads.contactno
        citycodet=expatads.citycode
        locationcodet=expatads.locationcode
        sublocationcodet=expatads.sublocationcode
        landmarkt=expatads.landmark
        pricet=expatads.price

        request.POST._mutable = True
        form.data['user']=request.user
        form.data['is_followed']=False
        context={'user': request.user,
                 'locationcode' : locationcodet,
                 'sublocationcode' : sublocationcodet,
                 'landmark' : landmarkt,
                 'price' : pricet,
                 'citycode':citycodet,
                 'fromemail': request.user.email,
                 'to_email':email,
                 'mobilenumber': mobilenumber,
                 'domain':get_current_site(request)}
        if form.is_valid():
            form.save()
            mail_subject = 'We have received your Email '
            email_template = 'accounts/emails/Sendnotification_to_customer.html'
          
            send_notification(mail_subject, email_template, context)
            #send_mail(mail_subject,'We received Your message Here is acknowledgment Thanks','aakhan1572@gmail.com',[email],fail_silently=False,)
            messages.success(request, 'We have received your message sucessfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if not request.user.is_authenticated:
        messages.success(request, 'Please login')
        return render(request, 'accounts/login.html')
    context = {'form': form}
    return render(request, 'expads/interested.html', context)

@login_required(login_url='login')
def addads(request):
    form=ExpatadForm()
    if request.method == "POST":
        form= ExpatadForm(request.POST,request.FILES)
        images_list = request.FILES.getlist('images')
        request.POST._mutable = True
        form.data['user']=request.user
        form.data['is_active']=True
        if form.is_valid():
            newform=form.save()
            expatad = Expatad.objects.get(id=newform.id)
            for image in images_list:
                Expatad_images = ExpatImage.objects.create(
                    expatads= expatad,
                    images = image

                )
            messages.success(request, 'Your Ad added successfully.')
            return redirect('expataddetail',id=expatad.id)
        #else:
            #messages.error(request,'Enter Valid Data')
            #return redirect(request.META['HTTP_REFERER'])
            #return HttpResponse('Form Not Valid')
    else:
        form = ExpatadForm()
    countrycodes=Countrycode.objects.all()
    context = {'form':form,'countrycodes':countrycodes}
    return render(request, 'expads/addads.html',context)

# AJAX
def load_cities(request):
    country_id = request.GET.get('countrycode')
    cities = CityCode.objects.filter(countrycode_id=country_id).all()
    return render(request, 'expads/city_dropdown_list_options.html', {'cities': cities})

def placeads(request):
    if request.method == "POST":
        fullname1 = request.POST['fullname']
        city = request.POST['cityname']
        measurements = request.POST['measurements']
        print(fullname1, city, measurements) 
    countrycodes=Countrycode.objects.all()
    context = {'countrycodes':countrycodes}
    return render(request, 'expads/placeads.html',context)

@login_required(login_url='login')
def deletead(request,id):
    if request.method =='POST':
        messages.success(request, 'Your Posted Ad Delete Successfully')
        print(id)
        pi=Expatad.objects.get(id=id)
        pi.delete()
        messages.success(request, 'Your Posted Ad Delete Successfully')
    else:
        messages.success(request, 'Your not owner of this Ad')
    return redirect('home')

@login_required(login_url='login')
def delete_ad(request, id):
    expatad = get_object_or_404(Expatad, id=id)
    print(id)
    expatad.delete()
    messages.success(request, 'Your Ad has been deleted successfully!')
    return redirect('home')

@login_required(login_url='login')
def updatead(request,id):
    pi = get_object_or_404(Expatad,id=id)
    if request.method == 'POST':
        pi = Expatad.objects.get(id=id)
        fm = ExpatadForm(request.POST,request.FILES,instance=pi)
        images_list = request.FILES.getlist('images')
        request.POST._mutable = True
        fm.data['user']=request.user
        fm.data['is_active']=True
        if fm.is_valid():
            expatad = Expatad.objects.get(id=id)
            exp=Expatad.objects.get(id=id)
            exp.delete()
            fm.save()
            for image in images_list:
                Expatad_images = ExpatImage.objects.create(
                    expatads= expatad,
                    images = image
                )
            messages.success(request, 'Your Ad Updated successfully.')
            return redirect('updatead',id=id)
        else:
            print('invalid form')
            print(fm.errors)
            # Get the current instance object to display in the template
            #img_obj = fm.instance
            #print(img_obj)
            #return render(request, 'expads/updatead.html', {'form': fm, 'img_obj': img_obj})
    else:
        #pi = get_object_or_404(Expatad,id=id) 
        imlist =ExpatImage.objects.filter(expatads=pi).prefetch_related('expatads')
        fm=ExpatadForm(instance=pi)
        #print(pi.cover_photo)
    context={'form':fm,'pi':pi,'imlist':imlist}
    return render(request, 'expads/updatead.html',context)


@login_required(login_url='login')
def edit_ad(request, id):
    expatad = get_object_or_404(Expatad, id=id)
    if request.method == 'POST':
        form = ExpatadForm(request.POST, request.FILES, instance=expatad)
        images_list = request.FILES.getlist('images')
        if form.is_valid():
            expatad = form.save(commit=False)
            expatad.user=request.user
            expatad.is_active=True
            form.save()
            for image in images_list:
                Expatad_images = ExpatImage.objects.create(
                    expatads= expatad,
                    images = image
                )
            messages.success(request, 'Your Ad updated successfully!')
            return redirect('expataddetail', expatad.id)
        else:
            print(form.errors)

    else:
        form = ExpatadForm(instance=expatad)
        #form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'expatad':expatad,
    }
    return render(request, 'expads/edit_ad.html', context)




def countries(request):
    countries = Countrycode.objects.all()
    context = {'countries': countries}
    return render(request, 'university.html', context)


def cities(request):
    countrycode = request.GET.get('cities')
    cities = CityCode.objects.filter(countrycode=countrycode)
    context = {'cities': cities}
    return render(request, 'expads/partials/cities.html', context)




  

""" def home(request):
    expatad_filter = Expatadfilter(request.GET, queryset=Expatad.objects.all().filter(is_active=True))
    context = {
        'form' : expatad_filter.form,
        'expatads': expatad_filter.qs
    } 
    print(context)
    return render(request, 'home.html', context)

ef expads(request, slug=None):
    categories = None
    expatads = None

    if slug != None:
        categories = get_object_or_404(Category, slug=slug)
        print(categories)
        expatads = Expatad.objects.filter(category=categories, is_active=True)
        paginator = Paginator(expatads, 3)
        page = request.GET.get('page')
        paged_expatads = paginator.get_page(page)
        expatad_count = expatads.count()
    else:
        expatads = Expatad.objects.all().filter(is_active=True).order_by('id')
        paginator = Paginator(expatads, 3)
        page = request.GET.get('page')
        paged_expatads = paginator.get_page(page)
        expatad_count = expatads.count()

    context = {
        'expatads': paged_expatads,
        'expatad_count': expatad_count,
    }
    return render(request, 'home.html', context)

 def addads(request):
    form=ExpatadForm()
    if request.method == "POST":
        form= ExpatadForm(request.POST or None, request.FILES or None)
        images_list = request.FILES.getlist('images')
        request.POST._mutable = True
        form.data['user']=request.user
        form.data['is_active']=True
        #print(form)
        if form.is_valid():
            user = form.cleaned_data['user']
            is_active = form.cleaned_data['is_active']
            category = form.cleaned_data['category']
            fullname = form.cleaned_data['fullname']
            countrycode = form.cleaned_data['countrycode']
            purpose = form.cleaned_data['purpose']
            citycode = form.cleaned_data['citycode']
            locationcode = form.cleaned_data['locationcode']
            landmark = form.cleaned_data['landmark']
            area = form.cleaned_data['area']
            areameasurement  = form.cleaned_data['areameasurement']
            contactno = form.cleaned_data['contactno']
            zipcode = form.cleaned_data['zipcode']
            price = form.cleaned_data['price']
            Description = form.cleaned_data['Description']
            cover_photo = form.cleaned_data['cover_photo']

            expatad_obj = Expatad.objects.create(user=user,category=category,fullname=fullname,countrycode=countrycode,purpose=purpose,citycode=citycode,
            locationcode=locationcode,landmark=landmark,area=area,areameasurement=areameasurement,contactno=contactno,zipcode=zipcode,price=price,
            Description=Description,is_active=is_active,cover_photo=cover_photo)
            print(images_list)
            for i in images_list:
                ExpatImage.objects.create(expatads=expatad_obj,images=i)
            messages.success(request, 'Your Ad added successfully.')
            return redirect('home')
        else:
            print(form.errors)
            return HttpResponse('Form Not Valid')
    else:
        form = ExpatadForm()

    context = {'form':form}
    return render(request, 'expads/addads.html',context)
 """
