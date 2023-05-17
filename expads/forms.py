from django import forms
from .validators import allow_only_images_validator
from .models import Category, Expatad, Contactme, Interested,Countrycode,CityCode


class CategoryForm(forms.ModelForm):
    thumbnail = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = Category
        fields = '__all__'



class ExpatadForm(forms.ModelForm):
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    Description = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}))
    class Meta:
        model = Expatad
        fields = '__all__'
        widgets = {'countrycode': forms.Select(attrs={ 'class': 'form-select' }),
            'citycode': forms.Select(attrs={ 'class': 'form-select' }),
            'cover_photo' : forms.FileInput(attrs={'class':'form-control mb-3'})
        }    

    def __init__(self, *args, **kwargs):
        super(ExpatadForm, self).__init__(*args, **kwargs)
        self.fields['areameasurement'].widget.attrs['placeholder'] = 'Square feet,Square Yards,Acre,Cent'
        #self.fields['areameasurement'].initial= ['Square Feet','Square Yards','Acre','cent']
        #self.fields['countrycode'].initial = 'Saudi Arabia'
        self.fields['citycode'].queryset = CityCode.objects.none()
        if 'countrycode' in self.data:
            try:
                countrycode = self.data.get('countrycode')
                self.fields['citycode'].queryset = CityCode.objects.filter(countrycode_id=countrycode).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk and self.instance.countrycode:
            #print(self.instance.id)
            #print(self.instance.countrycode)
            #print(self.instance.citycode)
            self.fields['citycode'].queryset = CityCode.objects.filter(countrycode_id=self.instance.countrycode).order_by('name')



class ContactmeForm(forms.ModelForm):
    class Meta:
        model = Contactme
        fields = ['user','fullname', 'contactno', 'email','Description']




class InterestedForm(forms.ModelForm):
    class Meta:
        model = Interested
        fields = ['user','fullname', 'contactno', 'email','Description']