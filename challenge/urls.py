
from django.contrib import admin
from django.urls import path
from airpnp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/listings/',                                  views.CreateAndShow.as_view(),        name='listings'),
    path('api/listings/<int:pk>/',                         views.ListingCRUD.as_view(),          name='listingCRUD'),
    path('api/listings/<int:pk>/special-prices',           views.SpecialPrice.as_view(),         name='specialprice'),
    path('api/listings/<int:pk>/special-prices/<int:pk2>', views.SpecialPriceDelete.as_view(),   name='specialpriceDelete'),
    path('api/listings/<int:pk>/checkout',                 views.CheckOut.as_view(),             name='CheckOut'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

