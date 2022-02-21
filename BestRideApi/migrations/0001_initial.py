# Generated by Django 3.2.7 on 2022-02-21 19:21

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'City',
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('idDriver', models.AutoField(db_column='idDriver', primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.CharField(blank=True, max_length=4000, null=True)),
                ('specialNeedSuppport', models.CharField(blank=True, max_length=255, null=True)),
                ('languages', models.CharField(blank=True, max_length=255, null=True)),
                ('vehiclesCanDrive', models.CharField(blank=True, max_length=255, null=True)),
                ('availableHours', models.CharField(blank=True, max_length=255, null=True)),
                ('courseTaken', models.CharField(blank=True, max_length=255, null=True)),
                ('typeGuide', models.CharField(blank=True, max_length=255, null=True)),
                ('about', models.CharField(blank=True, max_length=4000, null=True)),
                ('video', models.CharField(blank=True, max_length=4000, null=True)),
                ('startActivity', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'Driver',
            },
        ),
        migrations.CreateModel(
            name='EmergencyContactDriver',
            fields=[
                ('idEmergencyContactDrive', models.AutoField(db_column='idEmergencyContactDrive', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('relation', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'EmergencyContactDriver',
            },
        ),
        migrations.CreateModel(
            name='EmpresaDriver',
            fields=[
                ('idEmpresaDriver', models.AutoField(db_column='idEmpresaDriver', primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'db_table': 'EmpresaDriver',
            },
        ),
        migrations.CreateModel(
            name='ItinearyRouteInterestPoints',
            fields=[
                ('id', models.BigAutoField(db_column='id', primary_key=True, serialize=False)),
                ('itinearyroute_id', models.IntegerField()),
                ('pointinterest_id', models.IntegerField()),
            ],
            options={
                'db_table': 'itineary_route_interest_points',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('idPagamento', models.AutoField(db_column='idPagamento', primary_key=True, serialize=False)),
                ('modo_pagamento', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'Payment',
            },
        ),
        migrations.CreateModel(
            name='PointInterest',
            fields=[
                ('idpercurso', models.AutoField(db_column='idPercurso', primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=45, null=True)),
                ('location', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
                ('image', models.CharField(blank=True, max_length=322, null=True)),
            ],
            options={
                'db_table': 'Point_Interest',
            },
        ),
        migrations.CreateModel(
            name='RoadMap',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('price', models.CharField(blank=True, max_length=100, null=True)),
                ('duration', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.CharField(blank=True, max_length=322, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('location', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
                ('arquivado', models.CharField(blank=True, max_length=100, null=True)),
                ('city_id', models.ForeignKey(db_column='city_id', on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.city')),
                ('driver', models.ForeignKey(db_column='driver', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.driver')),
                ('enterprise', models.ForeignKey(db_column='enterprise', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.empresadriver')),
            ],
            options={
                'db_table': 'road_map',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('iduser', models.AutoField(db_column='idUser', primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.CharField(blank=True, max_length=4000, null=True)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('seats', models.IntegerField(db_column='seats')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.CharField(blank=True, max_length=4000, null=True)),
                ('registration', models.CharField(blank=True, max_length=255)),
                ('arquivado', models.CharField(blank=True, max_length=100, null=True)),
                ('enterprise', models.ForeignKey(db_column='enterprise', on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.empresadriver')),
            ],
            options={
                'db_table': 'vehicle',
            },
        ),
        migrations.CreateModel(
            name='TravelSchedule',
            fields=[
                ('idAgendaViagem', models.AutoField(db_column='idAgendaViagem', primary_key=True, serialize=False)),
                ('dataAgenda', models.DateField()),
                ('driver_id', models.ForeignKey(db_column='driver_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='driver_id', to='BestRideApi.user')),
                ('road_map_id', models.ForeignKey(db_column='road_map_id', on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.roadmap')),
                ('turist_id', models.ForeignKey(db_column='turist_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='turist_id', to='BestRideApi.user')),
            ],
            options={
                'db_table': 'TravelSchedule',
            },
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('idViagem', models.AutoField(db_column='idViagem', primary_key=True, serialize=False)),
                ('Pagamento_idPagamento', models.ForeignKey(db_column='Pagamento_idPagamento', on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.payment')),
                ('driver_id', models.ForeignKey(db_column='driver_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='driverID', to='BestRideApi.driver')),
                ('road_map_id', models.ForeignKey(db_column='road_map_id', on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.roadmap')),
                ('turist_id', models.ForeignKey(db_column='turist_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='turistID', to='BestRideApi.user')),
            ],
            options={
                'db_table': 'Travel',
            },
        ),
        migrations.CreateModel(
            name='FKDriverEnterprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Driver', models.ForeignKey(db_column='driver', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.driver')),
                ('Enterprise', models.ForeignKey(db_column='enterprise', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.empresadriver')),
            ],
            options={
                'db_table': 'FKDriverEnterprise',
            },
        ),
        migrations.AddField(
            model_name='driver',
            name='emergencyContact_id',
            field=models.ForeignKey(db_column='emergencyContact_id', on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.emergencycontactdriver'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('idComment', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('comment', models.CharField(blank=True, db_column='comment', max_length=350, null=True)),
                ('pontuation', models.IntegerField(db_column='pontuation')),
                ('username', models.CharField(blank=True, db_column='username', max_length=350, null=True)),
                ('road_map', models.ForeignKey(db_column='id_road_map', on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.roadmap')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='RoadVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('road_map', models.ForeignKey(db_column='road_map', on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.roadmap')),
                ('vehicle', models.ForeignKey(db_column='vehicle', on_delete=django.db.models.deletion.DO_NOTHING, to='BestRideApi.vehicle')),
            ],
            options={
                'db_table': 'road_vehicle',
                'unique_together': {('road_map', 'vehicle')},
            },
        ),
    ]
