from django import forms

class YourFilterForm(forms.Form):
    search_query = forms.CharField(required=False,label='',widget=forms.TextInput(attrs={'class': 'custom-css-class', 'placeholder': 'Tìm kiếm...'}))
    # # search_carowner = forms.CharField(required=False, label='Search Car Owner')
    # search_slot = forms.IntegerField(required=False)
    # search_start_location = forms.CharField(required=False)
    # search_end_location = forms.CharField(required=False)
    # # search_start_time = forms.TimeField(required=False, label='Search Start Time')
    # search_name_driver = forms.TimeField(required=False)
class ImageUploadForm(forms.Form):
    image_upload = forms.ImageField(required=True,label='',widget=forms.ClearableFileInput(attrs={'class': 'custom_image_upload'}))