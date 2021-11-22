# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.gis.db import models

class Travel(models.Model):
    idViagem = models.AutoField(db_column='idViagem', primary_key=True)
    Pagamento_idPagamento = models.ForeignKey('Payment',models.DO_NOTHING,db_column='Pagamento_idPagamento')
    dataViagem = models.DateField
    turist_id = models.ForeignKey('User', models.DO_NOTHING, db_column='turist_id',related_name="turistID")
    horaInicio = models.DateField
    horaFim = models.DateField
    road_map_id = models.ForeignKey('RoadMap',models.DO_NOTHING,db_column='road_map_id')
    driver_id = models.ForeignKey('User', models.DO_NOTHING, db_column='driver_id',related_name="driverID")

    class Meta:
        db_table = 'Travel'

class Payment(models.Model):
    idPagamento = models.AutoField(db_column='idPagamento', primary_key=True)
    modo_pagamento = models.CharField(max_length=45)

    class Meta:
        db_table = "Payment"


class TravelSchedule(models.Model):
    idAgendaViagem = models.AutoField(db_column='idAgendaViagem', primary_key=True)  # Field name made lowercase.
    turist_id = models.ForeignKey('User', models.DO_NOTHING, db_column='turist_id',related_name="turist_id")
    dataAgenda = models.DateField()
    driver_id = models.ForeignKey('User', models.DO_NOTHING, db_column='driver_id',related_name="driver_id")
    road_map_id = models.ForeignKey('RoadMap', models.DO_NOTHING, db_column='road_map_id')

    class Meta:
        db_table = 'TravelSchedule'


class PointInterest(models.Model):
    idpercurso = models.AutoField(db_column='idPercurso', primary_key=True)  # Field name made lowercase.
    description = models.CharField(max_length=45, blank=True, null=True)
    location = models.GeometryField(blank=True, null=True)
    image = models.CharField(max_length=322, blank=True, null=True)

    class Meta:
        db_table = 'Point_Interest'


class User(models.Model):
    iduser = models.AutoField(db_column='idUser', primary_key=True)  # Field name made lowercase.
    email = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        db_table = 'User'

"""class EmergencyContactDrive:
    idEmergencyContactDrive = models.AutoField(db_column='idEmergencyContactDrive', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    relation = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'EmergencyContactDrive'

class Driver(models.Model):
    idDriver = models.AutoField(db_column='idDriver', primary_key=True)  # Field name made lowercase.
    email = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=4000, blank=True, null=True)
    specialNeedSuppport =  models.CharField(max_length=255, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True) #Falta ver como meter mais que 1
    vehiclesCanDrive = models.CharField(max_length=255, blank=True, null=True) #Falta ver como meter mais que 1
    availableHours = models.CharField(max_length=255, blank=True, null=True) #Falta ver como gerir esta info
    courseTaken = models.CharField(max_length=255, blank=True, null=True) #Falta ver como meter mais que 1
    emergencyContactDrive = models.ForeignKey("EmergencyContactDrive", models.DO_NOTHING, db_column='emergencyContactDrive')
    typeGuide = models.CharField(max_length=255, blank=True, null=True)
    about = models.CharField(max_length=4000, blank=True, null=True)
    video = models.CharField(max_length=4000, blank=True, null=True)
    startActivity = models.CharField(max_length=10, blank=True, null=True)


    class Meta:
        db_table = 'Driver'

class EmpresaDriver:
    idEmpresaDriver = models.AutoField(db_column='idEmpresaDriver', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    relation = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'EmpresaDriver'"""

class City(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'City'


class ItinearyRoute(models.Model):
    interest_points = models.ForeignKey(PointInterest, models.DO_NOTHING, db_column='interest_points')
    road_map = models.ForeignKey('RoadMap', models.DO_NOTHING)

    class Meta:
        db_table = 'itineary_route'
        unique_together = (('id', 'interest_points', 'road_map'),)


class ItinearyRouteInterestPoints(models.Model):
    id = models.BigAutoField(primary_key=True)
    itinearyroute_id = models.IntegerField()
    pointinterest_id = models.IntegerField()

    class Meta:
        db_table = 'itineary_route_interest_points'


class RoadMap(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=322, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    location = models.GeometryField(blank=True, null=True)
    city_id = models.OneToOneField(City, models.DO_NOTHING, db_column='city_id')

    class Meta:
        db_table = 'road_map'


class RoadVehicle(models.Model):
    road_map = models.ForeignKey(RoadMap, models.DO_NOTHING, db_column='road_map')
    vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='vehicle')

    class Meta:
        db_table = 'road_vehicle'
        unique_together = (('road_map', 'vehicle'),)


class Vehicle(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    max_cap = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'vehicle'

class Comments(models.Model):
    idComment = models.AutoField(db_column='id', primary_key=True)
    comment = models.CharField(max_length=350, blank=True, null=True, db_column='comment')
    pontuation = models.IntegerField(db_column='pontuation')
    road_map = models.ForeignKey(RoadMap, models.DO_NOTHING, db_column='id_road_map')
    username = models.CharField(max_length=350, blank=True, null=True, db_column='username')

    class Meta:
        db_table = 'comments'