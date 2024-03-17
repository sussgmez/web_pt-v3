import pandas, string
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from .models import Customer, Order, Technician
from .forms import CustomerForm, OrderForm, HSOrderForm, OrderAssignUpdateForm

# Create your views here.
# Home
class HomeView(TemplateView):
    template_name = "order_app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["technicians"] = Technician.objects.all()
        return context

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'order_app/add_customer.html'

    def get_success_url(self): return reverse('home')

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "order_app/update_customer.html"

    def get_success_url(self): return reverse('home')

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = "order_app/delete_customer.html"
    
    def get_success_url(self): return reverse('home')

class CustomerListView(ListView):
    model = Customer
    template_name = "order_app/customer_list.html"
    paginate_by = 12

    def get_queryset(self):

        text_search = self.request.GET['text_search']
        
        customers = Customer.objects.filter(contract_number__contains=text_search) | Customer.objects.filter(customer_name__contains=text_search) | Customer.objects.filter(address__contains=text_search)
        
        status_search = self.request.GET['status_search']
        if (status_search == 'or-to-assign'): customers = customers.filter(order__technician=None).filter(order__completed=False)
        elif (status_search == 'or-assigned'): customers = customers.exclude(order__technician=None).filter(order__completed=False)
        elif (status_search == 'or-completed'): customers = customers.filter(order__completed=True)
        

        technician_search = self.request.GET['technician_search']
        if technician_search != "--": customers = customers.filter(order__technician=technician_search)

        min_date = self.request.GET['min_date']
        if min_date == "": min_date = '1900-01-01'

        max_date = self.request.GET['max_date']
        if max_date == "": max_date = '2100-01-01'

        min_date += " 00:00"
        max_date += " 23:59"

        if min_date != "1900-01-01 00:00" or max_date != "2100-01-01 23:59": customers = customers.filter(order__date_assigned__range=[min_date, max_date])

        order_by = self.request.GET['order_by']

        return customers.order_by(order_by)
    
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "order_app/update_order.html"

    def get_success_url(self): return reverse('home')

# Schedule
class Schedule(TemplateView):
    template_name = "order_app/schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["technicians"] = Technician.objects.all()
        return context

class ScheduledCustomers(ListView):
    model = Customer
    template_name = "order_app/scheduled_customers.html"

    def get_queryset(self):
        customers = Customer.objects.filter(order__technician=self.request.GET['technician'])
        n = [int(x) for x in self.request.GET['date'].split('-')]
        if self.request.GET['date'] != "":
            customers = customers.filter(order__date_assigned=datetime(year=n[0], month=n[1], day=n[2]))
        return customers.order_by('order__time_assigned')

class CustomersToAssign(ListView):
    model = Customer
    template_name = "order_app/customers_to_assign.html"

    def get_queryset(self):
        
        text_search = self.request.GET['text_search']
        customers = Customer.objects.filter(contract_number__contains=text_search) | Customer.objects.filter(customer_name__contains=text_search) | Customer.objects.filter(address__contains=text_search)
        
        return customers.filter(order__technician=None).filter(order__completed=False)
    
class OrderHSUpdateView(UpdateView):
    model = Order
    template_name = "order_app/update_h_s_order.html"
    form_class = HSOrderForm

    def get_success_url(self): return reverse('schedule')

class OrderAssignUpdate(UpdateView):
    model = Order
    template_name = "order_app/udpate_assign_order.html"
    form_class = OrderAssignUpdateForm

    def get_success_url(self): return reverse('schedule')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["technicians"] = Technician.objects.all()
        return context

def import_xlsx(request):
    if request.POST:
        df = pandas.read_excel(request.FILES['excel_file'])
        df.columns = ['contract_number', 'customer_name', 'type', 'seller', 'na1', 'phone_1', 'phone_2', 'address', 'email', 'plan', 'assigned_company', 'comment']

        df = df.fillna('')
    
        file_name = request.FILES['excel_file'].name
        date_received = datetime.now()
        received_date_txt = ""
        for char in file_name: 
            if char.isnumeric(): received_date_txt+=char
        try:
            date_received = datetime(day=int(received_date_txt[0:2]), month=int(received_date_txt[2:4]), year=int(received_date_txt[4:8]))
        except: pass

        for id, values in df.iterrows():
            try:
                for i in range(0,11): values.iloc[i]
                obj, created = Customer.objects.get_or_create(contract_number=values['contract_number'])
            except: continue

            if created:
                try:
                    printable = set(string.printable+'ñÑ')
                    obj.customer_name = ''.join(filter(lambda x: x in printable, values['customer_name'])).title()
                    obj.address = ''.join(filter(lambda x: x in printable, values['address'])).title().title().replace('Calle Calle', 'Calle').replace('Urb. Urb.', 'Urb.').replace('Ii', 'II')

                    aux_phone_1 = str(int(values['phone_1']))
                    obj.phone_2 = ""
                    if values['phone_2'] != "": 
                        aux_phone_2 = str(int(values['phone_2']))
                        obj.phone_2 = "0" + aux_phone_2 if aux_phone_2[0] == "4" else aux_phone_2
                    obj.phone_1 = "0" + aux_phone_1 if aux_phone_1[0] == "4" else aux_phone_1

                    aux_plan = values['plan'].upper()
                    if aux_plan == 'BASICO' or aux_plan == 'BÁSICO':
                        obj.plan = 'BA'
                    elif aux_plan == 'BASICO PLUS' or aux_plan == 'BÁSICO PLUS':
                        obj.plan = 'BP'
                    elif aux_plan == 'BRONCE':
                        obj.plan = 'BR'
                    elif aux_plan == 'PLATA':
                        obj.plan = 'PL'
                    elif aux_plan == 'ORO':
                        obj.plan = 'OR'
                    elif aux_plan == 'EMPRENDEDOR':
                        obj.plan = 'EM'
                    elif aux_plan == 'PRODUCTIVO':
                        obj.plan = 'PR'
                    elif aux_plan == 'PRODUCTIVO PRO':
                        obj.plan = 'PP'
                    elif aux_plan == 'VISIONARIO PRO':
                        obj.plan = 'VP'
                    else: obj.plan = 'SD'

                    aux_category = "INS"
                    if 'MIGRACION' in values['comment'].upper() or 'MIGRACION' in values['seller'].upper() or 'MIGRACIÓN' in values['comment'].upper() or 'MIGRACIÓN' in values['seller'].upper(): aux_category = 'MIG'
                    elif 'MUDANZA' in values['comment'].upper() or 'MUDANZA' in values['seller'].upper(): aux_category = 'MUD'
                    obj.category = aux_category

                    if 'FIBRA RESIDENCIAL' in values['type'].upper(): aux_type = 'FR'
                    elif 'FIBRA PYME' in values['type'].upper(): aux_type = 'FP'
                    else: aux_type = 'OT'
                    obj.customer_type = aux_type

                    obj.date_received = date_received

                    obj.comment = values['comment'].title()

                    obj.save()

                except:
                    obj.delete()
            
    return redirect('home')

def export_xlsx(request):
    text_search = request.GET['text_search']
        
    customers = Customer.objects.filter(contract_number__contains=text_search) | Customer.objects.filter(customer_name__contains=text_search) | Customer.objects.filter(address__contains=text_search)
    
    status_search = request.GET['status_search']
    if (status_search == 'or-to-assign'): customers = customers.filter(order__technician=None).filter(order__completed=False)
    elif (status_search == 'or-assigned'): customers = customers.exclude(order__technician=None).filter(order__completed=False)
    elif (status_search == 'or-completed'): customers = customers.filter(order__completed=True)
    
    min_date = request.GET['min_date']
    if min_date == "": min_date = '1900-01-01'

    max_date = request.GET['max_date']
    if max_date == "": max_date = '2100-01-01'

    min_date += " 00:00"
    max_date += " 23:59"

    if min_date != "1900-01-01 00:00" or max_date != "2100-01-01 23:59": customers = customers.filter(order__date_assigned__range=[min_date, max_date])

    df = pandas.DataFrame()

    for customer in customers: 

        df_aux = pandas.DataFrame([[
            customer.order.date_assigned.strftime('%A') if customer.order.date_assigned != None else "",
            1,
            customer.order.date_assigned.strftime('%d/%m/%Y') if customer.order.date_assigned != None else "",
            customer.contract_number, 
            customer.customer_name, 
            customer.address[:50],
            customer.order.drop_used if customer.order.drop_used != None and customer.order.drop_used > 250 else "",
            customer.order.hook_used,
            customer.order.drop_used,
            customer.order.drop_serial,
            customer.order.onu_serial,
            customer.order.router_serial,
            customer.order.technician,
        ]])  
        df = pandas.concat([df, df_aux])

    df = df.rename(columns={0:'DIA', 1:'ITEM', 2:'FECHA', 3:'CONTRATO', 4:'NOMBRE CLIENTE', 5:'DIRECCION', 6:'+ DE 250M', 7:'TENSORES', 8:'MTS DROP', 9:'SN. DROP', 10:'SERIAL ONU', 11:'SERIAL ROUTER', 12:'TÉCNICO'})

    with BytesIO() as b:
        with pandas.ExcelWriter(b) as writer:
            df.to_excel(writer, sheet_name='DATA 1', index=False)
        filename = f'{str(datetime.now().strftime("%d-%m-%Y %H%M%S"))}.xlsx'
        res = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        res['Content-Disposition'] = f'attachment; filename={filename}'
        return res

    
