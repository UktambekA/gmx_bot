import csv
import os
from django.core.management.base import BaseCommand
from pharmacy_admin.models import Pharmacy, Employee, Medicine
from django.conf import settings

class Command(BaseCommand):
    help = 'Import data from CSV files into the database'

    def handle(self, *args, **kwargs):
        base_dir = settings.BASE_DIR.parent  # Project root directory where CSV files are located

        # File paths
        xodimlar_path = os.path.join(base_dir, 'xodimlar.csv')
        dorilar_path = os.path.join(base_dir, 'dorilar.csv')
        dorixonalar_path = os.path.join(base_dir, 'dorixona.csv')

        # Clear existing data
        self.stdout.write('Deleting existing data...')
        Medicine.objects.all().delete()
        Employee.objects.all().delete()
        Pharmacy.objects.all().delete()

        # Import Pharmacies
        self.stdout.write('Importing pharmacies...')
        with open(dorixonalar_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            pharmacies = []
            for row in reader:
                pharmacies.append(Pharmacy(
                    id=row['id'],
                    inn=row['inn'],
                    dorixona_nomi=row['dorixona_nomi'],
                    manzil=row['manzil'],
                    kontrakt=row['kontrakt'],
                    dorixona_egasi=row['dorixona_egasi'],
                    mfo=row['mfo'],
                    rs=row['rs'],
                    dagovor=row['dagovor']
                ))
            Pharmacy.objects.bulk_create(pharmacies)

        # Import Employees
        self.stdout.write('Importing employees...')
        with open(xodimlar_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            employees = []
            for row in reader:
                employees.append(Employee(
                    id=row['id'],
                    telefon_raqam=row['telefon_raqam'],
                    ism_familiya=row['ism_familiya']
                ))
            Employee.objects.bulk_create(employees)

        # Import Medicines
        self.stdout.write('Importing medicines...')
        with open(dorilar_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            medicines = []
            for row in reader:
                medicines.append(Medicine(
                    id=row['id'],
                    dori_nomi=row['nomi'],
                    narxi=float(row['narxi']),
                    ikpu=row['ikpu'],
                    rasm=row.get('rasm', ''),
                    image_file_id=row.get('image_file_id', ''),
                    info=row.get('info', '')
                ))
            Medicine.objects.bulk_create(medicines)

        self.stdout.write(self.style.SUCCESS('Data import completed successfully.'))
