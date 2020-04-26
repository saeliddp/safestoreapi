from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from safestore.quickstart.models import Store
from rest_framework import viewsets
from rest_framework import permissions
from safestore.quickstart.serializers import UserSerializer, GroupSerializer, StoreSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from safestore.quickstart.mapinterface import get_stores_by_zip, ll2zip
import json
import datetime



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    @action(detail=True)
    def get_stores(self, request):
        print(request.query_params)
        store = self.get_object()
        return Response(store.get_stores)

@api_view(['GET', 'POST'])
def fetchstore(request):
    lat = request.query_params['lat']
    long = request.query_params['long']
    zip = str(ll2zip(lat, long))
    stores = Store.objects.filter(zipcode=zip)
    if len(stores) == 0:
        results = get_stores_by_zip(zip)
        for storepair in results:
            if zip in storepair[1]:
                tt = {'8:00am':0,'8:30am':0,'9:00am':0,'9:30am':0,'10:00am':0,'10:30am':0,'11:00am':0,'11:30am':0,'12:00pm':0,'12:30pm':0,'1:00pm':0,'1:30pm':0,'2:00pm':0,'2:30pm':0,'3:00pm':0,'3:30pm':0,'4:00pm':0,'4:30pm':0,'5:00pm':0,'5:30pm':0,'6:00pm':0,'6:30pm':0,'7:00pm':0,'7:30pm':0,'8:00pm':0}
                jtt = json.dumps(tt)
                Store(name=storepair[0], zipcode=zip, physical_address=storepair[1], timetable=jtt, latitude=storepair[2], longitude=storepair[3]).save()
        stores = Store.objects.filter(zipcode=zip)
        
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    end = "jdlfk"
    if hour >= 12:
        end = "pm"
    else:
        end = "am"
    minutestr = "30"
    if minute >= 30:
        hour += 1
        minutestr = "00"
    if hour >= 13:
        hour -= 12
    
    endstr = str(hour) + ":" + minutestr + end

    for s in stores:
        jsontt = json.loads(s.timetable)
        found = False
        min = 100000
        mintime = "8:00am"
        for key in jsontt:
            if key == endstr:
                found = True
                
            if not found:
                jsontt[key] = '0'
            elif int(jsontt[key]) < min:
                min = int(jsontt[key])
                mintime = key
        s.besttime = mintime
        s.save()
                
                
                
        

    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def addperson(request):
    storeid = int(request.query_params['id'])
    timeslot = request.query_params['slot']
    imc = request.query_params['imc']
    store = Store.objects.filter(id=storeid)[0]
    jsontt = json.loads(store.timetable)
    if imc == 't':
        jsontt[timeslot] = jsontt[timeslot] + 2
    else:
        jsontt[timeslot] = jsontt[timeslot] + 1
    newjson = json.dumps(jsontt)
    store.timetable = newjson
    store.save()
    return Response(StoreSerializer(store).data)

    