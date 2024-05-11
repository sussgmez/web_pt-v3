from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import RedirectView
from order_app.views import HomeView, CustomerCreateView, CustomerListView, CustomerUpdateView, OrderUpdateView, CustomerDeleteView, Schedule, ScheduledCustomers, CustomersToAssign, OrderAssignUpdate, OrderHSUpdateView, Preconfig, PreconfigCustomers, OrderPreconfigUpdateView, InventoryOnuPage, OnuCreateView, OnuUpdateView, OnuDeleteView,  OnuListView, InventoryRouterPage, RouterCreateView, RouterUpdateView, RouterDeleteView, RouterListView,  import_xlsx, export_xlsx, onu_export_xlsx, router_export_xlsx

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
    # Preconfig
    path('preconfig/', login_required(Preconfig.as_view()), name='preconfig'),
    path('preconfig_customers/', login_required(PreconfigCustomers.as_view()), name='preconfig-customers'),
    path('update_preconfig_order/<int:pk>', login_required(OrderPreconfigUpdateView.as_view()), name='update-preconfig-order'),
    # Inventory ONU
    path('inventory/onu/', login_required(InventoryOnuPage.as_view()), name='inventory-onu'),
    path('inventory/add_onu/', login_required(OnuCreateView.as_view()), name='add-onu'),
    path('inventory/update_onu/<slug:pk>', login_required(OnuUpdateView.as_view()), name='update-onu'),
    path('inventory/delete_onu/<slug:pk>', login_required(OnuDeleteView.as_view()), name='delete-onu'),
    path('inventory/onu_list/', login_required(OnuListView.as_view()), name='onu-list'),
    path('inventory/onu_export_xlsx/', login_required(onu_export_xlsx), name='onu-export-xlsx'),
    # Inventory Router
    path('inventory/router/', login_required(InventoryRouterPage.as_view()), name='inventory-router'),
    path('inventory/add_router/', login_required(RouterCreateView.as_view()), name='add-router'),
    path('inventory/update_router/<slug:pk>', login_required(RouterUpdateView.as_view()), name='update-router'),
    path('inventory/delete_router/<slug:pk>', login_required(RouterDeleteView.as_view()), name='delete-router'),
    path('inventory/router_list/', login_required(RouterListView.as_view()), name='router-list'),
    path('inventory/router_export_xlsx/', login_required(router_export_xlsx), name='router-export-xlsx'),
]
