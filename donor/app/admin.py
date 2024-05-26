from django.contrib import admin
from .models import DonationArea, Donor, Donation, Gallery, Volunteer

@admin.register(DonationArea)
class DonationAreaAdmin(admin.ModelAdmin):
    list_display = ['id','areaname', 'description','creationdate']

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['id','user','contact','address','regdate']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['id','donor','volunteer','collectionloc','donationame']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id','donation','deliverypic','creationdate']

    


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['id','user','contact','address','regdate']
