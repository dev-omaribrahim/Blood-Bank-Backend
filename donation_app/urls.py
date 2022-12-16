from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'donators', views.DonorProfileViewSet, basename="donors")
router.register(r'institutes', views.InstituteProfileViewSet, basename="institutes")

app_name = "donation_app"

urlpatterns = [
    path("filters/", views.MultiFilterAPIView.as_view(), name="donations_view"),
    path("search/", views.SearchAPIView.as_view(), name="search_view"),
    path("create/", views.DonationCreateAPIView.as_view(), name="donation_create_view"),
    path("details/<serial_number>/", views.DonationDetailAPIView.as_view(), name="donation_detail_view"),
    path("damage_action/", views.DamageActionAPIView.as_view(), name="damage_action_view"),
    path("test_action/", views.TestActionAPIView.as_view(), name="test_action_view"),
    path("separation/", views.SeparationAPIView.as_view(), name="separation_view"),
    path("profiles/", include(router.urls))
]