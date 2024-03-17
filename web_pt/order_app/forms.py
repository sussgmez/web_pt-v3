from django import forms
from .models import Customer, Order

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['contract_number', 'customer_name', 'address', 'plan', 'customer_type', 'category', 'phone_1', 'phone_2', 'email', 'assigned_company', 'seller', 'date_received', 'comment']
        widgets = {
            'contract_number':forms.NumberInput(attrs={'class':'form-input', 'min':'1000000', 'max':'1099999', 'placeholder':' ', 'onkeyup':'check_contract_number(this.value)'}),
            'customer_name':forms.TextInput(attrs={'class':'form-input', 'placeholder':' '}),
            'address':forms.Textarea(attrs={'rows':'2','class':'form-input form-input-textarea','type':'textarea', 'placeholder':' '}),
            'phone_1':forms.TextInput(attrs={'class':'form-input', 'placeholder':' '}),
            'phone_2':forms.TextInput(attrs={'class':'form-input', 'placeholder':' '}),
            'email':forms.TextInput(attrs={'class':'form-input', 'placeholder':' ','type':'email'}),
            'plan':forms.Select(attrs={'class':'form-input', 'placeholder':' '}),
            'customer_type':forms.Select(attrs={'class':'form-input', 'placeholder':' '}),
            'category':forms.Select(attrs={'class':'form-input', 'placeholder':' '}),
            'assigned_company':forms.TextInput(attrs={'class':'form-input', 'placeholder':' '}),
            'seller':forms.TextInput(attrs={'class':'form-input', 'placeholder':' '}),
            'date_received':forms.DateTimeInput(format='%Y-%m-%d', attrs={'type':'date', 'class':'form-input', 'placeholder':' '}),
            'comment':forms.Textarea(attrs={'rows':'2','class':'form-input form-input-textarea', 'placeholder':' '}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['technician', 'date_assigned', 'time_assigned', 'onu_serial', 'router_serial', 'zone', 'olt', 'card', 'pon', 'box', 'port', 'box_power', 'house_power', 'drop_serial', 'drop_used', 'hook_used', 'fast_conn_used', 'completed']
        widgets = {
            'technician':forms.Select(attrs={'class':'form-input', 'placeholder':' '}),
            'date_assigned':forms.DateInput(format='%Y-%m-%d', attrs={'type':'date','class':'form-input', 'placeholder':' '}),
            'time_assigned':forms.TimeInput(attrs={'type':'time', 'class':'form-input', 'placeholder':' '}),
            'onu_serial':forms.TextInput(attrs={'class':'form-input', 'placeholder':' '}),
            'router_serial':forms.TextInput(attrs={'class':'form-input', 'placeholder':' '}),
            'zone':forms.NumberInput(attrs={'class':'form-input', 'placeholder':' '}),
            'olt':forms.NumberInput(attrs={'class':'form-input', 'placeholder':' '}),
            'card':forms.NumberInput(attrs={'class':'form-input', 'placeholder':' '}),
            'pon':forms.NumberInput(attrs={'class':'form-input', 'placeholder':' '}),
            'box':forms.NumberInput(attrs={'class':'form-input', 'placeholder':' '}),
            'port':forms.NumberInput(attrs={'class':'form-input', 'placeholder':' '}),

            'box_power':forms.NumberInput(attrs={'class':'form-input', 'step':'0.01' , 'placeholder':' '}),
            'house_power':forms.NumberInput(attrs={'class':'form-input', 'step':'0.01' , 'placeholder':' '}),
            
            'drop_serial':forms.NumberInput(attrs={'class':'form-input', 'placeholder':' '}),
            'drop_used':forms.NumberInput(attrs={'class':'form-input', 'placeholder':' '}),
            'hook_used':forms.NumberInput(attrs={'class':'form-input', 'placeholder':' '}),
            'fast_conn_used':forms.NumberInput(attrs={'class':'form-input', 'placeholder':' '}),

            'completed': forms.HiddenInput()
        }

class HSOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ("time_assigned", "customer_confirmation")
        widgets = {
            'date_assigned':forms.DateTimeInput(format='%H:%M', attrs={'type':'time', 'class':'form-input', 'placeholder':' '}),
        }

class OrderAssignUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ("technician", "date_assigned")
