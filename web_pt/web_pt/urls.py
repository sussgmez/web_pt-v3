from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import RedirectView
from order_app.views import HomeView, CustomerCreateView, CustomerListView, CustomerUpdateView, OrderUpdateView, CustomerDeleteView, Schedule, ScheduledCustomers, CustomersToAssign, OrderAssignUpdate, OrderHSUpdateView, Preconfig, PreconfigCustomers, OrderPreconfigUpdateView, import_xlsx, export_xlsx

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', RedirectView.as_view(pattern_name='home')),
    # Home
    path('home/', login_required(HomeView.as_view()), name='home'),
    path('add_customer/', login_required(CustomerCreateView.as_view()), name='add-customer'),
    path('update_customer/<int:pk>', login_required(CustomerUpdateView.as_view()), name='update-customer'),
    path('delete_customer/<int:pk>', login_required(CustomerDeleteView.as_view()), name='delete-customer'),
    path('update_order/<int:pk>', login_required(OrderUpdateView.as_view()), name='update-order'),
    path('customer_list/', login_required(CustomerListView.as_view()), name='customer-list'),
    path('import_xlsx/', login_required(import_xlsx), name='import-xlsx'),
    path('export_xlsx/', login_required(export_xlsx), name='export-xlsx'),
    # Schedule
    path('schedule/', login_required(Schedule.as_view()), name='schedule'),
    path('scheduled_customers/', login_required(ScheduledCustomers.as_view()), name='scheduled-customers'),
    path('update_h_s_order/<int:pk>', login_required(OrderHSUpdateView.as_view()), name='update-h-s-order'),
    path('customers_to_assign/', login_required(CustomersToAssign.as_view()), name='customers-to-assign'),
    path('update_assign_order/<int:pk>', login_required(OrderAssignUpdate.as_view()), name='update-assign-order'),
    # Preconfi
    path('preconfig/', login_required(Preconfig.as_view()), name='preconfig'),
    path('preconfig_customers/', login_required(PreconfigCustomers.as_view()), name='preconfig-customers'),
    path('update_preconfig_order/<int:pk>', login_required(OrderPreconfigUpdateView.as_view()), name='update-preconfig-order'),
    
]
