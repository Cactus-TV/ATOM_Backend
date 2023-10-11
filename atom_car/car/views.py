from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from car.models import *
from car.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_condition import Or
from datetime import datetime, time
import random


#CAR
class CarAdminAPICreate(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (
        IsAdminUser,
    )


class CarAdminAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (
        IsAdminUser,
    )


class CarAPIGet(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (
        Or(AllowAny,
           IsAuthenticated, 
           IsAdminUser),
    )


class CarUpdateAPI(APIView):
    permission_classes = [IsAuthenticated|
                          IsAdminUser|
                          AllowAny]
    
    def post(self, request):
        try:
            available_commands = [
                'car', 
                'secure', 
                'radio', 
                'sound', 
                'station', 
                'call', 
                'trans', 
                'control', 
                'cruise', 
                'line', 
                'light', 
                'beep', 
                'warning', 
                'gps',
                'wash',
                'tire']

            command = request.data['command']
            if not command in available_commands :
                return Response({'error': 'unknown command'}, status.HTTP_400_BAD_REQUEST)
            
            car = list(Car.objects.all())[0]
            message = ''
            if command == 'car':
                field = request.data['field1']
                available_field_commands = ['on', 'off']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field == 'on':
                    car.is_on = True
                else:
                    car.is_on = False
            elif command == 'secure':
                field = request.data['field1']
                available_field_commands = ['on', 'off']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field == 'on':
                    car.secure_system = True
                else:
                    car.secure_system = False
            elif command == 'radio':
                field = request.data['field1']
                available_field_commands = ['on', 'off']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field == 'on':
                    car.radio = True
                else:
                    car.radio = False
            elif command == 'sound':
                field = request.data['field1']
                available_field_commands = ['lower', 'higher', 'off']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field == 'higher':
                    if car.sound >= 95:
                        car.sound = 100
                    else:
                        car.sound += 5
                elif field == 'lower':
                    if car.sound < 5:
                        car.sound = 0
                    else:
                        car.sound -= 5
                else:
                    car.sound = 0
            elif command == 'station':
                field = request.data['field1']
                available_field_commands = ['next', 'prev']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field == 'next':
                    if car.station == 1080:
                        car.station = 890
                    else:
                        car.station += 5
                else:
                    if car.station == 890:
                        car.station = 1080
                    else:
                        car.station -= 5
            elif command == 'call':
                field = request.data['field1']
                available_field_commands = ['accept', 'decline']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field == 'accept':
                    message = 'Allo!'
                else:
                    message = 'I am busy now, cant talk, sorry!'
                car.last_call_command = field
                car.last_call_date = datetime
            elif command == 'trans':
                field = request.data['field1']
                available_field_commands = ['drive', 'sport', 'neutral', 'back', 'park', 'brake']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field != 'brake' and field != 'park': #включаем фары при начале движения
                    car.lights = 'drive'
                elif field == 'brake' or field == 'park' or field == 'neutral': #выключаем круиз при отсутствии движения
                    car.is_cruise_on = False
                car.last_transfer_change_time = time
                car.transfer = field
            elif command == 'control':
                field = request.data['field1']
                available_field_commands = ['parking', 'invite']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field == 'parking':
                    car.last_parking_time = time
                else:
                    car.last_invite_time = time
            elif command == 'cruise':
                field = request.data['field1']
                available_field_commands = ['higher', 'lower', 'off']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                car.is_cruise_on = True
                if field == 'higher':
                    if car.cruise >= 240:
                        car.cruise = 250
                    else:
                        car.cruise += 10
                elif field == 'lower':
                    if car.cruise < 40:
                        car.cruise = 30
                    else:
                        car.cruise -= 10
                else:
                    car.is_cruise_on = False
            elif command == 'line':
                field = request.data['field1']
                available_field_commands = ['left', 'right']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                car.last_lines_change_time = time
                car.last_lines_change_command = field
            elif command == 'light':
                field = request.data['field1']
                available_field_commands = ['near', 'antifog', 'far', 'drive', 'off']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field != 'off' or (car.transfer != 'park' and car.transfer != 'brake' and field == 'off'):
                    car.lights = field
            elif command == 'beep':
                message = 'BEEP!'
                car.last_beep_time = time
            elif command == 'warning':
                field = request.data['field1']
                available_field_commands = ['on', 'off', 'one']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                car.warnings = field
                if field == 'one':
                    message = 'THANKS!'
                    car.last_thanks_date = datetime
                    car.warnings = 'off'
            elif command == 'gps':
                field = request.data['field1']
                available_field_commands = ['coordinate']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                car.warnings = field
                message = 'Coordinates: ' + \
                str(random.randint(0, 1000)) + ' ' + \
                str(random.randint(0, 1000)) + ' ' + \
                str(random.randint(0, 1000))
                car.last_gps_date = datetime
            elif command == 'wash':
                field = request.data['field1']
                available_field_commands = ['lights', 'glass']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field == 'lights':
                    car.last_wash_lights_time = time
                else:
                    car.last_wash_glass_time = time
            elif command == 'tire':
                field = request.data['field1']
                available_field_commands = ['normal', 'flat', 'half']
                if not field in available_field_commands:
                    return Response({'error': 'unknown field'}, status.HTTP_404_NOT_FOUND)
                if field != 'flat':
                    car.tires = field
            car.save()
            if message == '':
                return Response(status.HTTP_200_OK)
            else:
                return Response({'response': message}, status.HTTP_201_CREATED)
        
        except:
            return Response({'error': 'smth bad happened'}, status.HTTP_405_METHOD_NOT_ALLOWED)
        

#SEATS
class SeatAdminAPICreate(generics.CreateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = (
        IsAdminUser,
    )


class SeatAdminAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = (
        IsAdminUser,
    )


class SeatAPIGet(generics.ListAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = (
        Or(AllowAny,
           IsAuthenticated, 
           IsAdminUser),
    )


class SeatUpdateAPI(APIView):
    permission_classes = [IsAuthenticated|
                          IsAdminUser|
                          AllowAny]
    
    def post(self, request):
        try:
            available_commands = ['lower', 'higher', 'off']
            available_names = ['all', 'front_left', 'front_right', 'back_left', 'back_right', 'front', 'back']

            command = request.data['field1']
            name = request.data['field2']
            if not command in available_commands :
                return Response({'error': 'unknown command'}, status.HTTP_400_BAD_REQUEST)
            if not name in available_names:
                return Response({'error': 'unknown position'}, status.HTTP_404_NOT_FOUND)
            
            seats = list()
            if name == 'all':
                seats = list(Seat.objects.all())
            elif name == 'front':
                seats = list(Seat.objects.filter(Q(position='front_left') | Q(position='front_right')))
            elif name == 'back':
                seats = list(Seat.objects.filter(Q(position='back_left') | Q(position='back_right')))
            else:
                seats = list(Seat.objects.filter(Q(position=name)))

            for i in seats:
                if command == 'higher':
                    i.is_on=True
                    if i.temperature >= 35:
                        i.temperature=40
                    else:
                        i.temperature += 5
                elif command == 'lower':
                    i.is_on=True
                    if i.temperature < 25:
                        i.temperature=20
                    else:
                        i.temperature -= 5
                else:
                    i.is_on=False
                i.save()
            
            return Response(status.HTTP_200_OK)
        
        except:
            return Response({'error': 'smth bad happened'}, status.HTTP_405_METHOD_NOT_ALLOWED)
        

#WINDOWS
class WindowAdminAPICreate(generics.CreateAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer
    permission_classes = (
        IsAdminUser,
    )


class WindowAdminAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer
    permission_classes = (
        IsAdminUser,
    )


class WindowAPIGet(generics.ListAPIView):
    queryset = Window.objects.all()
    serializer_class = WindowSerializer
    permission_classes = (
        Or(AllowAny,
           IsAuthenticated, 
           IsAdminUser),
    )


class WindowUpdateAPI(APIView):
    permission_classes = [IsAuthenticated|
                          IsAdminUser|
                          AllowAny]
    
    def post(self, request):
        try:
            available_commands = ['open', 'close', 'half']
            available_names = ['all', 'front_left', 'front_right', 'back_left', 'back_right', 'front', 'back']

            command = request.data['field1']
            name = request.data['field2']
            if not command in available_commands :
                return Response({'error': 'unknown command'}, status.HTTP_400_BAD_REQUEST)
            if not name in available_names:
                return Response({'error': 'unknown position'}, status.HTTP_404_NOT_FOUND)
            
            windows = list()
            if name == 'all':
                windows = list(Window.objects.all())
            elif name == 'front':
                windows = list(Window.objects.filter(Q(position='front_left') | Q(position='front_right')))
            elif name == 'back':
                windows = list(Window.objects.filter(Q(position='back_left') | Q(position='back_right')))
            else:
                windows = list(Window.objects.filter(Q(position=name)))

            for i in windows:
                i.mode=command
                i.save()
            
            return Response(status.HTTP_200_OK)
        
        except:
            return Response({'error': 'smth bad happened'}, status.HTTP_405_METHOD_NOT_ALLOWED)
        

#PLACES
class PlaceAdminAPICreate(generics.CreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (
        IsAdminUser,
    )


class PlaceAdminAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (
        IsAdminUser,
    )


class PlaceAPIGet(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = (
        Or(AllowAny,
           IsAuthenticated, 
           IsAdminUser),
    )


class PlaceUpdateAPI(APIView):
    permission_classes = [IsAuthenticated|
                          IsAdminUser|
                          AllowAny]
    
    def post(self, request):
        try:
            available_commands = ['open', 'close']
            available_names = ['charge', 'roof']

            command = request.data['field1']
            name = request.data['field2']
            if not command in available_commands :
                return Response({'error': 'unknown command'}, status.HTTP_400_BAD_REQUEST)
            if not name in available_names:
                return Response({'error': 'unknown position'}, status.HTTP_404_NOT_FOUND)
            
            places = list()
            if name == 'all':
                places = list(Place.objects.all())
            else:
                places = list(Place.objects.filter(Q(position=name)))

            for i in places:
                if command == 'on':
                    i.is_on=True
                else:
                    i.is_on=False
                i.save()
            
            return Response(status.HTTP_200_OK)
        
        except:
            return Response({'error': 'smth bad happened'}, status.HTTP_405_METHOD_NOT_ALLOWED)


#CLIMATES
class ClimateAdminAPICreate(generics.CreateAPIView):
    queryset = Climate.objects.all()
    serializer_class = ClimateSerializer
    permission_classes = (
        IsAdminUser,
    )


class ClimateAdminAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Climate.objects.all()
    serializer_class = ClimateSerializer
    permission_classes = (
        IsAdminUser,
    )


class ClimateAPIGet(generics.ListAPIView):
    queryset = Climate.objects.all()
    serializer_class = ClimateSerializer
    permission_classes = (
        Or(AllowAny,
           IsAuthenticated, 
           IsAdminUser),
    )


class ClimateUpdateAPI(APIView):
    permission_classes = [IsAuthenticated|
                          IsAdminUser|
                          AllowAny]
    
    def post(self, request):
        try:
            available_commands = ['off', 'lower', 'higher']
            available_names = ['all', 'front', 'back']

            command = request.data['field1']
            name = request.data['field2']
            if not command in available_commands :
                return Response({'error': 'unknown command'}, status.HTTP_400_BAD_REQUEST)
            if not name in available_names:
                return Response({'error': 'unknown position'}, status.HTTP_404_NOT_FOUND)
            
            climates = list()
            if name == 'all':
                climates = list(Climate.objects.all())
            else:
                climates = list(Climate.objects.filter(Q(position=name)))

            for i in climates:
                if command == 'higher':
                    i.is_on=True
                    if i.temperature >= 35:
                        i.temperature=40
                    else:
                        i.temperature += 5
                elif command == 'lower':
                    i.is_on=True
                    if i.temperature < 20:
                        i.temperature=15
                    else:
                        i.temperature -= 5
                else:
                    i.is_on=False
                i.save()
            
            return Response(status.HTTP_200_OK)
        
        except:
            return Response({'error': 'smth bad happened'}, status.HTTP_405_METHOD_NOT_ALLOWED)



#GLASS
class GlassAdminAPICreate(generics.CreateAPIView):
    queryset = Glass.objects.all()
    serializer_class = GlassSerializer
    permission_classes = (
        IsAdminUser,
    )


class GlassAdminAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Glass.objects.all()
    serializer_class = GlassSerializer
    permission_classes = (
        IsAdminUser,
    )


class GlassAPIGet(generics.ListAPIView):
    queryset = Glass.objects.all()
    serializer_class = GlassSerializer
    permission_classes = (
        Or(AllowAny,
           IsAuthenticated, 
           IsAdminUser),
    )


class GlassUpdateAPI(APIView):
    permission_classes = [IsAuthenticated|
                          IsAdminUser|
                          AllowAny]
    
    @staticmethod
    def post(self, request):
        try:
            available_commands = ['off', 'on']
            available_names = ['all', 'front', 'back']

            command = request.data['field1']
            name = request.data['field2']
            if not command in available_commands :
                return Response({'error': 'unknown command'}, status.HTTP_400_BAD_REQUEST)
            if not name in available_names:
                return Response({'error': 'unknown position'}, status.HTTP_404_NOT_FOUND)
            
            glasses = list()
            if name == 'all':
                glasses = list(Glass.objects.all())
            else:
                glasses = list(Glass.objects.filter(Q(position=name)))

            for i in glasses:
                if command == 'on':
                    i.is_on=True
                else:
                    i.is_on=False
                i.save()
            
            return Response(status.HTTP_200_OK)
        
        except:
            return Response({'error': 'smth bad happened'}, status.HTTP_405_METHOD_NOT_ALLOWED)


#WIPERS
class WiperAdminAPICreate(generics.CreateAPIView):
    queryset = Wiper.objects.all()
    serializer_class = WiperSerializer
    permission_classes = (
        IsAdminUser,
    )


class WiperAdminAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wiper.objects.all()
    serializer_class = WiperSerializer
    permission_classes = (
        IsAdminUser,
    )


class WiperAPIGet(generics.ListAPIView):
    queryset = Wiper.objects.all()
    serializer_class = WiperSerializer
    permission_classes = (
        Or(AllowAny,
           IsAuthenticated, 
           IsAdminUser),
    )


class WiperUpdateAPI(APIView):
    permission_classes = [IsAuthenticated|
                          IsAdminUser|
                          AllowAny]
    
    def post(self, request):
        try:
            available_commands = ['off', 'one', 'slow', 'medium', 'fast']
            available_names = ['all', 'front', 'back']

            command = request.data['field1']
            name = request.data['field2']
            if not command in available_commands :
                return Response({'error': 'unknown command'}, status.HTTP_400_BAD_REQUEST)
            if not name in available_names:
                return Response({'error': 'unknown position'}, status.HTTP_404_NOT_FOUND)
            
            wipers = list()
            if name == 'all':
                wipers = list(Wiper.objects.all())
            else:
                wipers = list(Wiper.objects.filter(Q(position=name)))

            car = Car.objects.all()[0]
            message = ''
            for i in wipers:
                if command == 'one':
                    i.mode='one'
                    message = 'washed once'
                    i.mode='off'
                else:
                    i.mode=command
                i.save()
                
            if message != '':
                return Response({'response': message}, status.HTTP_201_CREATED)
            else:
                return Response(status.HTTP_200_OK)
        
        except:
            return Response({'error': 'smth bad happened'}, status.HTTP_405_METHOD_NOT_ALLOWED)


#DOORS
class DoorAdminAPICreate(generics.CreateAPIView):
    queryset = Door.objects.all()
    serializer_class = DoorSerializer
    permission_classes = (
        IsAdminUser,
    )


class DoorAdminAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Door.objects.all()
    serializer_class = DoorSerializer
    permission_classes = (
        IsAdminUser,
    )


class DoorAPIGet(generics.ListAPIView):
    queryset = Door.objects.all()
    serializer_class = DoorSerializer
    permission_classes = (
        Or(AllowAny,
           IsAuthenticated, 
           IsAdminUser),
    )


class DoorUpdateAPI(APIView):
    permission_classes = [IsAuthenticated|
                          IsAdminUser|
                          AllowAny]
    
    def post(self, request):
        try:
            available_commands = ['lock', 'unlock']
            available_names = ['all', 'front_left', 'front_right', 'back_left', 'back_right', 'front', 'back']

            command = request.data['field1']
            name = request.data['field2']
            if not command in available_commands:
                return Response({'error': 'unknown command'}, status.HTTP_400_BAD_REQUEST)
            if not name in available_names:
                return Response({'error': 'unknown position'}, status.HTTP_404_NOT_FOUND)
            
            doors = list()
            if name == 'all':
                doors = list(Door.objects.all())
            elif name == 'front':
                doors = list(Door.objects.filter(Q(position='front_left') | Q(position='front_right')))
            elif name == 'back':
                doors = list(Door.objects.filter(Q(position='back_left') | Q(position='back_right')))
            else:
                doors = list(Door.objects.filter(Q(position=name)))

            for i in doors:
                if command == 'lock':
                    i.is_locked=True
                else:
                    i.is_locked=False
                i.save()
            
            return Response(status.HTTP_200_OK)
        
        except:
            return Response({'error': 'smth bad happened'}, status.HTTP_405_METHOD_NOT_ALLOWED)
        

#TRUNKS
class TrunkAdminAPICreate(generics.CreateAPIView):
    queryset = Trunk.objects.all()
    serializer_class = TrunkSerializer
    permission_classes = (
        IsAdminUser,
    )


class TrunkAdminAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trunk.objects.all()
    serializer_class = TrunkSerializer
    permission_classes = (
        IsAdminUser,
    )


class TrunkAPIGet(generics.ListAPIView):
    queryset = Trunk.objects.all()
    serializer_class = TrunkSerializer
    permission_classes = (
        Or(AllowAny,
           IsAuthenticated, 
           IsAdminUser),
    )


class TrunkUpdateAPI(APIView):
    permission_classes = [IsAuthenticated|
                          IsAdminUser|
                          AllowAny]
    
    def post(self, request):
        try:
            available_commands = ['open', 'lock']
            available_names = ['all', 'front', 'back']

            command = request.data['field1']
            name = request.data['field2']
            if not command in available_commands :
                return Response({'error': 'unknown command'}, status.HTTP_400_BAD_REQUEST)
            if not name in available_names:
                return Response({'error': 'unknown position'}, status.HTTP_404_NOT_FOUND)
            
            trunks = list()
            if name == 'all':
                trunks = list(Trunk.objects.all())
            else:
                trunks = list(Trunk.objects.filter(Q(position=name)))

            for i in trunks:
                if command == 'lock':
                    i.is_opened=False
                else:
                    i.is_opened=True
                i.save()
            
            return Response(status.HTTP_200_OK)
        
        except:
            return Response({'error': 'smth bad happened'}, status.HTTP_405_METHOD_NOT_ALLOWED)