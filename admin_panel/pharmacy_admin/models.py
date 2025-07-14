from django.db import models

class Pharmacy(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='id')
    inn = models.CharField(max_length=50, db_column='inn')
    dorixona_nomi = models.CharField(max_length=255, db_column='dorixona_nomi')
    manzil = models.CharField(max_length=255, db_column='manzil')
    kontrakt = models.CharField(max_length=50, db_column='kontrakt')
    dorixona_egasi = models.CharField(max_length=255, db_column='dorixona_egasi')
    mfo = models.CharField(max_length=50, db_column='mfo')
    rs = models.CharField(max_length=50, db_column='rs')
    dagovor = models.CharField(max_length=50, db_column='dagovor')

    class Meta:
        db_table = 'dorixonalar'

    def __str__(self):
        return self.dorixona_nomi

class Employee(models.Model):
    id = models.CharField(max_length=50, primary_key=True, db_column='id')
    telefon_raqam = models.CharField(max_length=50, db_column='telefon_raqam')
    ism_familiya = models.CharField(max_length=255, db_column='ism_familiya')

    class Meta:
        db_table = 'xodimlar'

    def __str__(self):
        return self.ism_familiya

class Medicine(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    dori_nomi = models.CharField(max_length=255, db_column='dori_nomi')
    narxi = models.FloatField(db_column='narxi')
    ikpu = models.CharField(max_length=50, db_column='ikpu')
    rasm = models.CharField(max_length=255, blank=True, null=True, db_column='rasm')
    image_file_id = models.CharField(max_length=255, blank=True, null=True, db_column='image_file_id')
    info = models.TextField(blank=True, null=True, db_column='info')

    class Meta:
        db_table = 'dorilar'

    def __str__(self):
        return self.dori_nomi
