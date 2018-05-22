from django import forms

from .models import RawData

class DateForm(forms.ModelForm):

    class Meta:
        model = RawData
        fields = ('doc_date', 'received_date' )

        widgets = {
            'doc_date': forms.DateInput(attrs={'class':'form-control date1', 'placeholder':'Search...',}),
            'received_date': forms.DateInput(attrs={'class':'form-control date1', 'placeholder':'Search...',}),
        }

class SearchDateForm(forms.Form):
	start_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control date1', 'placeholder':'Search...',}))
	end_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control date1', 'placeholder':'Search...',}))
