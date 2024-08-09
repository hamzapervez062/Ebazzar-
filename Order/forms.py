from django import forms   
from Order.models import Shippinginfo

class BillingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''  # This removes the colon from all labels
    # Modify the widget for order_note
        # self.fields['order_note'].widget = forms.Textarea(attrs={
        #     'rows': 2, 
        #     'placeholder': 'Enter order note here',
        #     'class': 'form-control'
        # })
    class Meta:
        model = Shippinginfo
        fields = '__all__'
        labels = {
                  'first_name':'First Name*',
                  'last_name:':'Last Name*',
                  'email':'Email*',
                  'phone':'Phone*',
                  'address_line_1':'Address Line 1*',
                  'city':'City*',
                  'state':'State',
                  'country':'Country*',
                  'order_note':'Order Note',
                  }
        
        widgets = {'first_name':forms.TextInput(attrs={'placeholder':'Enter firstname here', 'class':'form-control required-field' ,}),
                   'last_name':forms.TextInput(attrs={'placeholder':'Enter lastname here', 'class':'form-control'}),
                   'email':forms.TextInput(attrs={'placeholder':'Enter email here', 'class':'form-control', }),
                   'phone':forms.TextInput(attrs={'placeholder':'Enter phone here', 'class':'form-control'}),
                   'address_line_1':forms.TextInput(attrs={'placeholder':'Enter address here', 'class':'form-control'}),
                   'city':forms.TextInput(attrs={'placeholder':'Enter city here', 'class':'form-control'}),
                   'state':forms.TextInput(attrs={'placeholder':'Enter state here', 'class':'form-control'}),
                   'country':forms.TextInput(attrs={'placeholder':'Enter country here', 'class':'form-control'}),
                   'order_note':forms.Textarea(attrs={'placeholder':'Enter order note here', 'class':'form-control', 'rows': 2, }),
                   }