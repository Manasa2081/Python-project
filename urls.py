
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView,LoginView
urlpatterns = [
    path('diseases/',views.diseaseform,name='diseases'),
    path('adddiseases/',views.adddisease,name='add-disease'),
    path('hospitals/',views.hospital_form,name='hospital'),
    path('add-hospitals',views.add_hospital_details,name='add-hospital-details'),
    path('healthform/',views.healthpolicy_form,name='health-form'),
    path('add-healthpolicy/',views.create_health_policy,name='add-healthpolicy'),
    path('areaform/',views.areaform,name='area-form'),
    path('add-area-details/',views.add_arae_details,name='add-area-details'),
    path('houseform/',views.house_policy,name='house-form'),
    path('premium/',views.premiumform,name='house'),
    path('count_premium/',views.count_premium,name='count-premium'),
    path('housepaymentform/',views.housepaymentform,name='housepaymentform'),
    path('house_payment_details/',views.house_payment_details,name='house_payment_details'),
    path('pending_house_policies/',views.pending_house_policies,name='pending_house_policies'),
    path('handle_house_polices/',views.handle_house_polices,name='handle_house_polices'),
    path('approved_house_policies/',views.approved_house_policies,name='approved_house_policies'),

    path('home/',views.home,name='home'),
    path('health-polices/',views.health,name='health'),
    path('register/',views.registerPage,name="register"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('getplan/<int:id>',views.getplan,name='getplan'),
    path('orderpage/',views.orderpage,name="orderpage"),
    path('orderdetails/<int:policy_id>',views.policy_orderdetails,name='orderdetails'),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('health-policy-customers/',views.healthpolicy_customers,name='health-policy-customers'),
    path('diseaseslist/',views.diseaseslist,name='diseaseslist'),
    path('hospitallist/',views.hospitalslist,name='hospitallist'),
    path('healthpolicieslist/',views.healthpolicieslist,name='healthpolicieslist'),
    path('adminlogin/', LoginView.as_view(template_name='admin_login.html'),name='adminlogin'),
    path('signupusers/',views.no_of_signupUsers,name="signupusers"),
    path('healthcustomerform/',views.health_policy_customerform,name='healthcustomerform'),
    path('add-health-policy-customer-details/',views.add_health_policy_customerdetails,name = 'add-health-policy-customer-details'),
    path('customer_dashboard/',views.customer_dashboard,name='customer_dashboard'),
    path('customer_apply/',views.customer_apply,name='customer_apply'),
    path('pending_policies/',views.pending_policies,name='pendingpolices'),
    path('handle-polcies', views.handle_polices, name='handle-policies'),
    path('approved_health_policies/',views.approved_health_policies,name='approved_health_policies')
]