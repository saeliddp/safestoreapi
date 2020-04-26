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
from safestore.quickstart.mapinterface import get_stores_by_zip
import json




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
    zip = request.query_params['zipcode']
    stores = Store.objects.filter(zipcode=zip)
    if len(stores) == 0:
        results = get_stores_by_zip(zip)
        for storepair in results:
            if zip in storepair[1]:
                tt = {'12:00am':0,'12:30am':0,'1:00am':0,'1:30am':0,'2:00am':0,'2:30am':0,'3:00am':0,'3:30am':0,'4:00am':0,'4:30am':0,'5:00am':0,'5:30am':0,'6:00am':0,'6:30am':0,'7:00am':0,'7:30am':0,'8:00am':0,'8:30am':0,'9:00am':0,'9:30am':0,'10:00am':0,'10:30am':0,'11:00am':0,'11:30am':0,'12:00pm':0,'12:30pm':0,'1:00pm':0,'1:30pm':0,'2:00pm':0,'2:30pm':0,'3:00pm':0,'3:30pm':0,'4:00pm':0,'4:30pm':0,'5:00pm':0,'5:30pm':0,'6:00pm':0,'6:30pm':0,'7:00pm':0,'7:30pm':0,'8:00pm':0,'8:30pm':0,'9:00pm':0,'9:30pm':0,'10:00pm':0,'10:30pm':0,'11:00pm':0,'11:30pm':0}
                jtt = json.dumps(tt)
                Store(name=storepair[0], zipcode=zip, physical_address=storepair[1], timetable=jtt).save()
        stores = Store.objects.filter(zipcode=zip)
        
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

    