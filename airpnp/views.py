from rest_framework.views import APIView
from .models import Listing, Special_price
from .serializer import ListingSerializer, Price_dateSerializer
from rest_framework.response import Response
from slugify import slugify
from datetime import datetime, timedelta
from django.db.models import Sum

#api/listings/
class CreateAndShow(APIView):
    def get(self, request):
        listings = Listing.objects.all()
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        owner = request.user.pk
        name = data['name']
        slug = slugify(name)
        description = data['description']
        adults = data['adults']
        children = data['children']
        is_pets_allowed = data['is_pets_allowed']
        base_price = data['base_price']
        cleaning_fee = data['cleaning_fee']
        image_url = data['image_url']
        weekly_discount = data['weekly_discount']
        monthly_discount = data['monthly_discount']
        newlisting = Listing(name=name, owner_id=owner, slug=slug, description=description, adults=adults, children=children, is_pets_allowed=is_pets_allowed,
                             base_price=base_price, cleaning_fee=cleaning_fee, image_url=image_url, weekly_discount=weekly_discount, monthly_discount=monthly_discount)
        try:
            newlisting.save()
            pk = newlisting.pk
            listing = Listing.objects.get(pk=pk)
            serializer = ListingSerializer(listing, many=False)
            return Response(serializer.data)
        except:
            return Response('Data not valid')
#api/listings/<int:pk>/
class ListingCRUD(APIView):
    def get(self, request, pk):
        listings = Listing.objects.get(pk=pk)
        serializer = ListingSerializer(listings, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        data = request.data
        listingToUpdate = Listing.objects.get(pk=pk)
        listingToUpdate.name = data['name']
        listingToUpdate.slug = slugify(listingToUpdate.name)
        listingToUpdate.description = data['description']
        listingToUpdate.adults = data['adults']
        listingToUpdate.children = data['children']
        listingToUpdate.is_pets_allowed = data['is_pets_allowed']
        listingToUpdate.base_price = data['base_price']
        listingToUpdate.cleaning_fee = data['cleaning_fee']
        listingToUpdate.image_url = data['image_url']
        listingToUpdate.weekly_discount = data['weekly_discount']
        listingToUpdate.monthly_discount = data['monthly_discount']
        listingToUpdate.save()
        serializer = ListingSerializer(listingToUpdate, many=False)
        return Response(serializer.data)

    def delete(self, request, pk):
         listings = Listing.objects.get(pk=pk)
         result = [{'id': listings.id}]
         listings.delete()
         return Response(result)
#api/listings/<int:pk>/special-prices
class SpecialPrice(APIView):
    def get(self, request, pk):
        special_prices = Special_price.objects.filter(listing_id=pk)
        serializer = Price_dateSerializer(special_prices, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        data = request.data
        date = data['date']
        checkIfExist = Special_price.objects.filter(listing_id=pk, date=date).count()
        if checkIfExist != 0:
            return Response('there is already a special price for this date')
        price = data['price']
        newSpecialPrice = Special_price(listing_id=pk, date=date, price=price)
        newSpecialPrice.save()
        serializer = Price_dateSerializer(newSpecialPrice, many=False)
        return Response(serializer.data)
#api/listings/<int:pk>/special-prices/<int:pk2>
class SpecialPriceDelete(APIView):
    def get(self, request, pk, pk2):
        special_prices = Special_price.objects.get(pk=pk2)
        serializer = Price_dateSerializer(special_prices, many=False)
        return Response(serializer.data)

    def delete(self, request, pk, pk2):
         special_prices = Special_price.objects.get(pk=pk2)
         result = [{'id': special_prices.id}]
         special_prices.delete()
         return Response(result)
#api/listings/<int:pk>/checkout
class CheckOut(APIView):
    def post(self, request, pk):
        data = request.data
        checkin = datetime.strptime(data['checkin'], '%Y-%m-%d')
        checkout = datetime.strptime(data['checkout'], '%Y-%m-%d')
        nights_count = (checkout - checkin).days
        if checkin < datetime.now():
            return Response('Checkin Date cant be a past date')
        if checkout <= checkin:
            return Response('Checkout date must be at least 1 day after Checkin date')
        if nights_count > 28:
            return Response('You cant book a listing for more than 28 days')
        listing = Listing.objects.get(pk=pk)
        cleaning_fee = listing.cleaning_fee
        #check out date is not considered because doesnt spend that night there
        special_prices_nights = Special_price.objects.filter(listing_id=pk, date__range=(checkin, checkout - timedelta(days=1))).count()
        if special_prices_nights > 0:
            total_special_prices = Special_price.objects.filter(listing_id=pk, date__range=(checkin, checkout - timedelta(days=1))).aggregate(Sum('price'))['price__sum']
        else:
            total_special_prices = 0
        regular_nights = nights_count - special_prices_nights
        total_regular_price = regular_nights * listing.base_price
        nights_cost = total_regular_price + total_special_prices
        if nights_count == 28:
            discount = listing.monthly_discount
        elif nights_count > 7:
            discount = listing.weekly_discount
        else:
            discount = 0
        dis = nights_cost * discount
        total = nights_cost * (1- discount) + cleaning_fee
        result = [{'nights_count': nights_count, 'regular_nights': regular_nights, 'special_nights':special_prices_nights, 'total_regular_price' :total_regular_price,
                   'total_special_prices':total_special_prices, 'total_nights_cost': nights_cost, 'discount': dis, 'cleaning_fee':cleaning_fee,'total':total,
                   }]
        return Response(result)
