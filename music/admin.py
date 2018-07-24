from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.contrib.admin import AdminSite
from .models import Album, Song

# Register your models here.
class CustomAdminView(AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('my_view/', self.admin_view(self.my_view))
        ]
        urls = my_urls + urls
        print(urls)
        return urls


    def my_view(self, request):
        return HttpResponse("Hello, world.")


custom_admin = CustomAdminView()
admin.site.register(Album)
admin.site.register(Song)