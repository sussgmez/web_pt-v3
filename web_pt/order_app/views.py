import pandas, string, math
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from .models import Customer, Order, Technician, Onu, Router
from .forms import CustomerForm, OrderForm, HSOrderForm, OrderAssignUpdateForm, OrderPreconfigUpdateForm, OnuForm, OnuUpdateForm, RouterForm, RouterUpdateForm


# Home
class HomeView(TemplateView):
    template_name = "order_app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff: context["technicians"] = Technician.objects.all()
        else: context["technicians"] = [self.request.user.technician]

        return context

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'order_app/add_customer.html'

    def get_success_url(self): 
        messages.success(self.request, "Se ha añadido al cliente correctamente.")
        return reverse('home')

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "order_app/update_customer.html"

    def get_success_url(self): return reverse('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not self.request.user.has_perm('order_app.change_customer'):
            kwargs['disabled_fields'] = ['contract_number', 'customer_name', 'address', 'plan', 'customer_type', 'category', 'phone_1', 'phone_2', 'email', 'assigned_company', 'seller', 'date_received', 'comment']
        return kwargs

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
        if (status_search == 'or-to-assign'): customers = customers.filter(order__technician=None).filter(order__completed=False).filter(order__not_assign=False)
        elif (status_search == 'or-assigned'): customers = customers.exclude(order__technician=None).filter(order__completed=False).filter(order__not_assign=False)
        elif (status_search == 'or-completed'): customers = customers.filter(order__completed=True)
        elif (status_search == 'or-not-assign'): 
            customers = customers.filter(order__not_assign=True).filter(order__completed=False)
            not_assing_reason = self.request.GET['not_assign_reason']
            if not_assing_reason != '-1':
                customers = customers.filter(order__not_assign_reason=int(not_assing_reason))

        elif (status_search == 'or-checked'): customers = customers.filter(order__checked=True)
        elif (status_search == 'or-not-checked'): customers = customers.exclude(order__technician=None).filter(order__checked=False)
        
        technician_search = self.request.GET['technician_search']
        if technician_search != "--": customers = customers.filter(order__technician=technician_search)

        min_date = self.request.GET['min_date']
        if min_date == "": min_date = '1900-01-01'

        max_date = self.request.GET['max_date']
        if max_date == "": max_date = '2100-01-01'

        if min_date != "1900-01-01" or max_date != "2100-01-01": customers = customers.filter(order__date_assigned__range=[min_date, max_date])



        order_by = self.request.GET['order_by']

        return customers.order_by(order_by)
    
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "order_app/update_order.html"

    def get_success_url(self): return reverse('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['technician_id'] = ""
        if not self.request.user.has_perm('order_app.change_order'):
            kwargs['disabled_fields'] = ['technician', 'date_assigned', 'time_assigned', 'onu', 'router', 'zone', 'olt', 'card', 'pon', 'box', 'port', 'box_power', 'house_power', 'drop_serial', 'drop_used', 'hook_used', 'fast_conn_used', 'completed']
        if not self.request.user.is_staff or self.get_object().not_assign:
            kwargs['disabled_fields'] = ['technician', 'date_assigned', 'time_assigned']
        try: 
            kwargs['technician_id'] = self.request.user.technician.pk
        except: pass 
        
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["onus"] = Onu.objects.filter(order__completed=False) | Onu.objects.filter(order=None)
        return context
    
# Schedule
class Schedule(TemplateView):
    template_name = "order_app/schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff: context["technicians"] = Technician.objects.all()
        else: context["technicians"] = [self.request.user.technician]
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["technician"] = Technician.objects.get(pk=self.request.GET['technician'])
        date = self.request.GET['date'].split('-')
        context["date"] = date[2] + "/" + date[1] + "/" + date[0]
        
        return context
    
class CustomersToAssign(ListView):
    model = Customer
    template_name = "order_app/customers_to_assign.html"

    def get_queryset(self):
        
        text_search = self.request.GET['text_search']
        customers = Customer.objects.filter(contract_number__contains=text_search) | Customer.objects.filter(customer_name__contains=text_search) | Customer.objects.filter(address__contains=text_search)
        
        return customers.filter(order__technician=None).filter(order__completed=False).filter(order__not_assign=False).order_by('date_received')
    
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

# Preconfig
class Preconfig(TemplateView):
    template_name = "order_app/preconfig.html"

class PreconfigCustomers(ListView):
    model = Customer
    template_name = "order_app/preconfig_customers.html"

    def get_queryset(self):
        n = [int(x) for x in self.request.GET['date'].split('-')]
        if self.request.GET['date'] != "":
            customers = Customer.objects.filter(order__date_assigned=datetime(year=n[0], month=n[1], day=n[2]))
            return customers.order_by('order__time_assigned')

class OrderPreconfigUpdateView(UpdateView):
    model = Order
    template_name = "order_app/update_preconfig_order.html"
    form_class = OrderPreconfigUpdateForm

    def get_success_url(self): return reverse('preconfig')

# Inventory ONU
class InventoryOnuPage(TemplateView):
    template_name = "order_app/inventory_onu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["technicians"] = Technician.objects.all()
        return context
    
class OnuCreateView(CreateView):
    model = Onu
    form_class = OnuForm
    template_name = "order_app/add_onu.html"

    def get_success_url(self): 
        messages.success(self.request, "Se ha añadido el serial correctamente.")
        return reverse('inventory-onu')
    
class OnuUpdateView(UpdateView):
    model = Onu
    form_class = OnuUpdateForm
    template_name = "order_app/update_onu.html"

    def get_success_url(self): 
        messages.success(self.request, "Se ha modificado el serial correctamente.")
        return reverse('inventory-onu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(completed=False)
        return context
    
class OnuDeleteView(DeleteView):
    model = Onu
    template_name = "order_app/delete_onu.html"
    
    def get_success_url(self): return reverse('home')

class OnuListView(ListView):
    model = Onu
    template_name = "order_app/onu_list.html"
    paginate_by = 50

    def get_queryset(self):
        text_search = self.request.GET['text_search']
        status_search = self.request.GET['status_search']
        assigned_search = self.request.GET['assigned_search']
        
        min_date = self.request.GET['min_date']
        if min_date == "": min_date = '1900-01-01'

        max_date = self.request.GET['max_date']
        if max_date == "": max_date = '2100-01-01'

        onus = Onu.objects.filter(serial__contains=text_search) | Onu.objects.filter(order__customer__pk__contains=text_search)
    
        if assigned_search == "of":
            onus = onus.filter(technician=None)
        elif assigned_search != "sd":
            onus = onus.filter(technician=assigned_search)

        if status_search == "1":
            onus = onus.filter(order__completed=False) | onus.filter(order=None)
        elif status_search == "2":
            onus = onus.filter(order__completed=True)

        if min_date != "1900-01-01" or max_date != "2100-01-01": onus = onus.filter(date_updated__range=[min_date, max_date])

        return onus.order_by('-date_updated')

# Inventory Router
class InventoryRouterPage(TemplateView):
    template_name = "order_app/inventory_router.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["technicians"] = Technician.objects.all()
        return context

class RouterCreateView(CreateView):
    model = Router
    form_class = RouterForm
    template_name = "order_app/add_router.html"

    def get_success_url(self): 
        messages.success(self.request, "Se ha añadido el serial correctamente.")
        return reverse('inventory-router')
    
class RouterUpdateView(UpdateView):
    model = Router
    form_class = RouterUpdateForm
    template_name = "order_app/update_router.html"

    def get_success_url(self): 
        messages.success(self.request, "Se ha modificado el serial correctamente.")
        return reverse('inventory-router')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(completed=False)
        return context
    
class RouterDeleteView(DeleteView):
    model = Router
    template_name = "order_app/delete_router.html"
    
    def get_success_url(self): return reverse('home')

class RouterListView(ListView):
    model = Router
    template_name = "order_app/router_list.html"
    paginate_by = 50

    def get_queryset(self):
        text_search = self.request.GET['text_search']
        status_search = self.request.GET['status_search']
        assigned_search = self.request.GET['assigned_search']
        
        min_date = self.request.GET['min_date']
        if min_date == "": min_date = '1900-01-01'

        max_date = self.request.GET['max_date']
        if max_date == "": max_date = '2100-01-01'

        routers = Router.objects.filter(serial__contains=text_search) | Router.objects.filter(order__customer__pk__contains=text_search)
    
        if assigned_search == "of":
            routers = routers.filter(technician=None)
        elif assigned_search != "sd":
            routers = routers.filter(technician=assigned_search)

        if status_search == "1":
            routers = routers.filter(order__completed=False) | routers.filter(order=None)
        elif status_search == "2":
            routers = routers.filter(order__completed=True)

        if min_date != "1900-01-01" or max_date != "2100-01-01": routers = routers.filter(date_updated__range=[min_date, max_date])

        return routers.order_by('-date_updated')

# Others
def import_xlsx(request):
    if request.POST:
        df = pandas.read_excel(request.FILES['excel_file'])
        try: 
            df.columns = ['contract_number', 'customer_name', 'type', 'seller', 'na1', 'phone_1', 'phone_2', 'address', 'email', 'plan', 'assigned_company', 'comment']
        except: pass

        df = df.fillna('')
    
        file_name = request.FILES['excel_file'].name
        date_received = datetime.now()
        received_date_txt = ""
        for char in file_name: 
            if char.isnumeric(): received_date_txt+=char
        try:
            date_received = datetime(day=int(received_date_txt[0:2]), month=int(received_date_txt[2:4]), year=int(received_date_txt[4:8]))
        except: pass

        added_customers = []

        for id, values in df.iterrows():
            try:
                for i in range(0,11): values.iloc[i]
                obj, created = Customer.objects.get_or_create(contract_number=values['contract_number'])
            except: continue


            if created:
                try:
                    printable = set(string.printable+'ñÑáÁéÉíÍóÓúÚ')
                    obj.customer_name = ''.join(filter(lambda x: x in printable, values['customer_name'])).title()
                    obj.address = ''.join(filter(lambda x: x in printable, values['address'])).title().title().replace('Calle Calle', 'Calle').replace('Urb. Urb.', 'Urb.').replace('Ii', 'II')

                    aux_phone_1 = str(math.trunc(float(values['phone_1'])))
                    obj.phone_2 = ""
                    if values['phone_2'] != "": 
                        aux_phone_2 = str(math.trunc(float(values['phone_2'])))
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
                    added_customers.append(obj.contract_number) 

                except: obj.delete()
            
        if len(added_customers) == 0: messages.error(request, "No se encontraron clientes para añadir. Favor subir el archivo con el siguiente formato [Nro. De Contrato, Nombre Cliente, Tipo, Vendedor, Dia De Pago, Teléfono 1, Teléfono 2, Dirección, Email, Plan, Asignado a, Observaciones]")
        else: 
            message = "Clientes añadidos:"
            for customer in added_customers:
                message+= " C" + str(customer)
            messages.success(request, message)

    return redirect('home')

def export_xlsx(request):
    text_search = request.GET['text_search']
        
    customers = Customer.objects.filter(contract_number__contains=text_search) | Customer.objects.filter(customer_name__contains=text_search) | Customer.objects.filter(address__contains=text_search)
    
    status_search = request.GET['status_search']
    if (status_search == 'or-to-assign'): customers = customers.filter(order__technician=None).filter(order__completed=False).filter(order__not_assign=False)
    elif (status_search == 'or-assigned'): customers = customers.exclude(order__technician=None).filter(order__completed=False)
    elif (status_search == 'or-completed'): customers = customers.filter(order__completed=True)
    elif (status_search == 'or-not-assign'): customers = customers.filter(order__not_assign=True).filter(order__completed=False)
    elif (status_search == 'or-checked'): customers = customers.filter(order__checked=True)
    elif (status_search == 'or-not-checked'): customers = customers.exclude(order__technician=None).filter(order__checked=False)
        
    technician_search = request.GET['technician_search']
    if technician_search != "--": customers = customers.filter(order__technician=technician_search)

    min_date = request.GET['min_date']
    if min_date == "": min_date = '1900-01-01'

    max_date = request.GET['max_date']
    if max_date == "": max_date = '2100-01-01'

    if min_date != "1900-01-01" or max_date != "2100-01-01": customers = customers.filter(order__date_assigned__range=[min_date, max_date])

    df = pandas.DataFrame()

    for customer in customers: 

        df_aux = pandas.DataFrame([[
            customer.order.date_assigned.strftime('%A') if customer.order.date_assigned != None else "",
            1,
            customer.date_received.strftime('%d/%m/%Y') if customer.date_received != None else "",
            customer.order.date_assigned.strftime('%d/%m/%Y') if customer.order.date_assigned != None else "",
            customer.contract_number, 
            customer.customer_name, 
            customer.address[:50],
            customer.order.drop_used if customer.order.drop_used != None and customer.order.drop_used > 250 else "",
            customer.order.hook_used,
            customer.order.drop_used,
            customer.order.drop_serial,
            customer.order.onu.serial if customer.order.onu != None else "",
            customer.order.router.serial if customer.order.router != None else "",
            customer.order.technician,
        ]])  
        df = pandas.concat([df, df_aux])

    df = df.rename(columns={0:'DIA', 1:'ITEM', 2:'FECHA RECIBIDA', 3:'FECHA ASIGNADA', 4:'CONTRATO', 5:'NOMBRE CLIENTE', 6:'DIRECCION', 7:'+ DE 250M', 8:'TENSORES', 9:'MTS DROP', 10:'SN. DROP', 11:'SERIAL ONU', 12:'SERIAL ROUTER', 13:'TÉCNICO'})

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


def onu_export_xlsx(request): 
    text_search = request.GET['text_search']
    status_search = request.GET['status_search']
    assigned_search = request.GET['assigned_search']
    
    min_date = request.GET['min_date']
    if min_date == "": min_date = '1900-01-01'

    max_date = request.GET['max_date']
    if max_date == "": max_date = '2100-01-01'

    onus = Onu.objects.filter(serial__contains=text_search) | Onu.objects.filter(order__customer__pk__contains=text_search)

    if assigned_search == "of":
        onus = onus.filter(technician=None)
    elif assigned_search != "sd":
        onus = onus.filter(technician=assigned_search)

    if status_search == "1":
        onus = onus.filter(order__completed=False) | onus.filter(order=None)
    elif status_search == "2":
        onus = onus.filter(order__completed=True)

    if min_date != "1900-01-01" or max_date != "2100-01-01": onus = onus.filter(date_updated__range=[min_date, max_date])

    df = pandas.DataFrame()

    for onu in onus:
        contract_number = None
        
        try: contract_number = onu.order.customer.contract_number
        except: pass
        
        df_aux = pandas.DataFrame([[
            onu.serial,
            contract_number,
            onu.technician if onu.technician != None else "",
            onu.date_updated.strftime("%d/%m/%Y, %H:%M")
        ]])
        df = pandas.concat([df, df_aux])


    df = df.rename(columns={0:'SERIAL', 1:'NRO. DE CONTRATO', 2:'TÉCNICO', 3:'ÚLTIMA MODIFICACIÓN'})

    with BytesIO() as b:
        with pandas.ExcelWriter(b) as writer:
            df.to_excel(writer, sheet_name='DATA 1', index=False)
        filename = f'{str(datetime.now().strftime("ONU-LIST %d-%m-%Y %H%M%S"))}.xlsx'
        print(filename)
        res = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        res['Content-Disposition'] = f'attachment; filename={filename}'
        return res


def router_export_xlsx(request): 
    text_search = request.GET['text_search']
    status_search = request.GET['status_search']
    assigned_search = request.GET['assigned_search']
    
    min_date = request.GET['min_date']
    if min_date == "": min_date = '1900-01-01'

    max_date = request.GET['max_date']
    if max_date == "": max_date = '2100-01-01'

    routers = Router.objects.filter(serial__contains=text_search) | Router.objects.filter(order__customer__pk__contains=text_search)

    if assigned_search == "of":
        routers = routers.filter(technician=None)
    elif assigned_search != "sd":
        routers = routers.filter(technician=assigned_search)

    if status_search == "1":
        routers = routers.filter(order__completed=False) | routers.filter(order=None)
    elif status_search == "2":
        routers = routers.filter(order__completed=True)

    if min_date != "1900-01-01" or max_date != "2100-01-01": routers = routers.filter(date_updated__range=[min_date, max_date])

    df = pandas.DataFrame()

    for router in routers:
        contract_number = None
        
        try: contract_number = router.order.customer.contract_number
        except: pass
        
        df_aux = pandas.DataFrame([[
            router.serial,
            contract_number,
            router.technician if router.technician != None else "",
            router.date_updated.strftime("%d/%m/%Y, %H:%M")
        ]])
        df = pandas.concat([df, df_aux])


    df = df.rename(columns={0:'SERIAL', 1:'NRO. DE CONTRATO', 2:'TÉCNICO', 3:'ÚLTIMA MODIFICACIÓN'})

    with BytesIO() as b:
        with pandas.ExcelWriter(b) as writer:
            df.to_excel(writer, sheet_name='DATA 1', index=False)
        filename = f'{str(datetime.now().strftime("ROUTER-LIST %d-%m-%Y %H%M%S"))}.xlsx'
        print(filename)
        res = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        res['Content-Disposition'] = f'attachment; filename={filename}'
        return res
