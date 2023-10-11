from django.db import models
from django.conf import settings
import uuid

#допустимые наборы команд
WINDOWS = (('open', 'open'), 
            ('close', 'close'),
            ('half', 'half'))
WIPER = (('off', 'off'), 
         ('one', 'one'), 
         ('slow', 'slow'), 
         ('medium', 'medium'),
         ('fast', 'fast'))
TRANSFER = (('drive', 'drive'), 
            ('sport', 'sport'), 
            ('neutral', 'neutral'), 
            ('back', 'back'), 
            ('park', 'park'), 
            ('brake', 'brake'))
LIGHTS = (('near', 'near'), 
          ('antifog', 'antifog'), 
          ('far', 'far'), 
          ('drive', 'drive'), 
          ('off', 'off'))
WARNINGS = (('accept', 'accept'), 
            ('decline', 'decline'))
CALL = (('call', 'call'), 
        ('accept', 'accept'), 
        ('decline', 'decline'))
LINES = (('left', 'left'), 
         ('right', 'right'))
TIRES = (('normal', 'normal'), 
         ('flat', 'flat'), 
         ('half', 'half'))


class Car(models.Model): #автомобиль
    name = models.CharField(max_length=64, unique=True, default="ATOM_number_1")
    vim = models.UUIDField(default=uuid.uuid4, primary_key=True)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    is_on = models.BooleanField(default=False)
    secure_system = models.BooleanField(default=False)
    radio = models.BooleanField(default=False) 
    station = models.IntegerField(default = 950)
    sound = models.IntegerField(default = 50)
    is_cruise_on = models.BooleanField(default=False)
    cruise = models.IntegerField(default = 40)
    transfer = models.CharField(max_length=8, default='neutral', choices=TRANSFER)
    warnings = models.CharField(max_length=8, default='off', choices=WARNINGS)
    lights = models.CharField(max_length=8, default='drive', choices=LIGHTS)
    tires = models.CharField(max_length=8, default='normal', choices=TIRES)
    last_transfer_change_time = models.TimeField(null=True)
    last_wash_lights_time = models.TimeField(null=True)
    last_wash_glass_time = models.TimeField(null=True)
    last_call_date = models.DateTimeField(null=True)
    last_call_command = models.CharField(max_length=8, blank=True, choices=CALL)
    last_invite_time = models.TimeField(null=True)
    last_parking_time = models.TimeField(null=True)
    last_lines_change_time = models.TimeField(null=True)
    last_lines_change_command = models.CharField(max_length=8, blank=True, choices=LINES)
    last_gps_date = models.DateTimeField(null=True)
    last_beep_time = models.TimeField(null=True)
    last_thanks_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.vim


class Climate(models.Model): #климат контроль
    position = models.CharField(max_length=8, primary_key=True)
    temperature = models.IntegerField(default = 25)
    is_on = models.BooleanField(default=True)
    car = models.ForeignKey(Car, on_delete = models.CASCADE)


class Door(models.Model): #боковые двери
    position = models.CharField(max_length=32, primary_key=True)
    is_locked = models.BooleanField(default=True)
    car = models.ForeignKey(Car, on_delete = models.CASCADE)


class Window(models.Model): #боковые стёкла
    position = models.CharField(max_length=32, primary_key=True)
    mode = models.CharField(max_length=8, choices=WINDOWS, default='close')
    car = models.ForeignKey(Car, on_delete = models.CASCADE)


class Wiper(models.Model): #очистители стёкол
    position = models.CharField(max_length=16, primary_key=True)
    mode = models.CharField(max_length=8, choices=WIPER, default='off')
    car = models.ForeignKey(Car, on_delete = models.CASCADE)


class Seat(models.Model): #подогрев сидений
    position = models.CharField(max_length=16, primary_key=True)
    temperature = models.IntegerField(default=30)
    is_on = models.BooleanField(default=False)
    car = models.ForeignKey(Car, on_delete = models.CASCADE)


class Glass(models.Model): #лобовое и здание стёкла
    position = models.CharField(max_length=16, primary_key=True)
    is_on = models.BooleanField(default=False)
    car = models.ForeignKey(Car, on_delete = models.CASCADE)


class Place(models.Model): #люк и крышка зарядки
    position = models.CharField(max_length=16, primary_key=True)
    is_opened = models.BooleanField(default=False)
    car = models.ForeignKey(Car, on_delete = models.CASCADE)


class Trunk(models.Model): #багажник
    position = models.CharField(max_length=8, primary_key=True)
    is_opened = models.BooleanField(default=False)
    car = models.ForeignKey(Car, on_delete = models.CASCADE)