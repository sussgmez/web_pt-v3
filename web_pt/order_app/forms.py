from typing import Any
from django import forms
from .models import Customer, Order, Onu, Router

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

    def __init__(self, *args, **kwargs):
        disabled_fields = kwargs.pop('disabled_fields', None)
        super(CustomerForm, self).__init__(*args, **kwargs)
        if disabled_fields != None:
            for field in disabled_fields:
                self.fields[field].widget.attrs['disabled'] = True

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['technician', 'date_assigned', 'time_assigned', 'onu', 'router', 'zone', 'olt', 'card', 'pon', 'box', 'port', 'box_power', 'house_power', 'drop_serial', 'drop_used', 'hook_used', 'fast_conn_used', 'completed', 'checked', 'not_assign']
        widgets = {
            'technician':forms.Select(attrs={'class':'form-input', 'placeholder':' '}),
            'date_assigned':forms.DateInput(format='%Y-%m-%d', attrs={'type':'date','class':'form-input only-superuser', 'placeholder':' '}),
            'time_assigned':forms.TimeInput(attrs={'type':'time', 'class':'form-input only-superuser', 'placeholder':' '}),
            'onu':forms.Select(attrs={'class':'form-input', 'placeholder':' '}),
            'router':forms.Select(attrs={'class':'form-input', 'placeholder':' '}),
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

            'completed': forms.HiddenInput(),
            'checked': forms.HiddenInput(),
            'not_assign': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        disabled_fields = kwargs.pop('disabled_fields', None)
        technician_id = kwargs.pop('technician_id', None)

        super(OrderForm, self).__init__(*args, **kwargs)
        if disabled_fields != None:
            for field in disabled_fields:
                self.fields[field].widget.attrs['disabled'] = True

        if technician_id != "":
            self.fields['onu'].queryset = Onu.objects.filter(technician=technician_id).filter(order__completed=False) | Onu.objects.filter(technician=technician_id).filter(order=None) | Onu.objects.filter(order=self.instance)
            self.fields['router'].queryset = Router.objects.filter(technician=technician_id).filter(order__completed=False) | Router.objects.filter(technician=technician_id).filter(order=None) | Router.objects.filter(order=self.instance)
        else:
            self.fields['onu'].queryset = Onu.objects.filter(order__completed=False) | Onu.objects.filter(order=None) | Onu.objects.filter(order=self.instance)
            self.fields['router'].queryset = Router.objects.filter(order__completed=False) | Router.objects.filter(order=None) | Router.objects.filter(order=self.instance)

    def clean_onu(self):
        data = self.cleaned_data["onu"]
        if data != None:
            try:
                aux_order = Order.objects.get(onu=data)
                aux_order.onu = None
                aux_order.save()
            except: pass
        return data

    def clean_router(self):
        data = self.cleaned_data["router"]
        if data != None:
            try:
                aux_order = Order.objects.get(router=data)
                aux_order.router = None
                aux_order.save()
            except: pass
        return data

class OnuForm(forms.ModelForm):

    class Meta:
        model = Onu
        fields = ("serial", 'technician')
        widgets = {
            'serial':forms.TextInput(attrs={'class':'form-input'}),
            'technician':forms.Select(attrs={'class':'form-input', 'disabled':True}),
        }

    def __init__(self, *args, **kwargs):
        super(OnuForm, self).__init__(*args, **kwargs)
        self.fields['order'] = forms.Field()
        self.fields['order'].widget.attrs = {'class':'form-input', 'disabled':True}
        self.fields['order'].required = False

class OnuUpdateForm(forms.ModelForm):

    class Meta:
        model = Onu
        fields = ('serial', 'technician', )
        widgets = {
            'serial':forms.TextInput(attrs={'class':'form-input', 'readonly':True}),
            'technician':forms.Select(attrs={'class':'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(OnuUpdateForm, self).__init__(*args, **kwargs)

        self.fields['order'] = forms.Field()
        self.fields['order'].widget.attrs = {'class':'form-input', 'list':'order_list'}
        self.fields['order'].required = False

        try:
            self.fields['order'].widget.attrs['value'] = self.instance.order.customer.pk
        except: pass

    def clean_order(self):
        contract_number = self.cleaned_data["order"]

        if contract_number != "":
            order =  Order.objects.get(customer__pk = contract_number)
            if order != None:
                try:
                    aux_order = Order.objects.get(onu=self.instance)
                    aux_order.onu = None
                    aux_order.save()
                except: pass
                order.onu = self.instance
                order.save()
        else:
            try:
                order =  Order.objects.get(onu = self.instance)
                order.onu = None
                order.save()
            except Exception as e: print(e)
        return contract_number

class RouterForm(forms.ModelForm):

    class Meta:
        model = Router
        fields = ("serial", 'technician')
        widgets = {
            'serial':forms.TextInput(attrs={'class':'form-input'}),
            'technician':forms.Select(attrs={'class':'form-input', 'disabled':True}),
        }

    def __init__(self, *args, **kwargs):
        super(RouterForm, self).__init__(*args, **kwargs)
        self.fields['order'] = forms.Field()
        self.fields['order'].widget.attrs = {'class':'form-input', 'disabled':True}
        self.fields['order'].required = False

class RouterUpdateForm(forms.ModelForm):

    class Meta:
        model = Router
        fields = ('serial', 'technician', )
        widgets = {
            'serial':forms.TextInput(attrs={'class':'form-input', 'readonly':True}),
            'technician':forms.Select(attrs={'class':'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(RouterUpdateForm, self).__init__(*args, **kwargs)

        self.fields['order'] = forms.Field()
        self.fields['order'].widget.attrs = {'class':'form-input', 'list':'order_list'}
        self.fields['order'].required = False

        try:
            self.fields['order'].widget.attrs['value'] = self.instance.order.customer.pk
        except: pass

    def clean_order(self):
        contract_number = self.cleaned_data["order"]

        if contract_number != "":
            order =  Order.objects.get(customer__pk = contract_number)
            if order != None:
                try:
                    aux_order = Order.objects.get(router=self.instance)
                    aux_order.router = None
                    aux_order.save()
                except: pass
                order.router = self.instance
                order.save()
        else:
            try:
                order =  Order.objects.get(router = self.instance)
                order.router = None
                order.save()
            except Exception as e: print(e)
        return contract_number

class HSOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("time_assigned", "customer_confirmation")

class OrderAssignUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("technician", "date_assigned", "time_assigned")

class OrderPreconfigUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['zone', 'olt', 'card', 'pon', 'box']
