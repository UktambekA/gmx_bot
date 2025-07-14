from django.contrib import admin
from .models import Pharmacy, Employee, Medicine

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('dorixona_nomi', 'manzil', 'inn', 'dorixona_egasi', 'kontrakt')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('ism_familiya', 'telefon_raqam', 'id')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('dori_nomi', 'narxi', 'ikpu')
