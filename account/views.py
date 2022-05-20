from django.shortcuts import render,get_object_or_404
from .serializers import (CreateUserSerializer, ChangePasswordSerializer,
                          UserSerializer, LoginUserSerializer, ForgetPasswordSerializer,ProfileSerializer)

from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.models import User, PhoneOTP,Profile
from rest_framework.views import APIView
from .utilmaths import phone_validator, password_generator, otp_generator 
import requests


from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from django.views.decorators.csrf import csrf_exempt

from rest_framework import permissions, generics, status,viewsets
from django.contrib.auth import login






class ForgotPasswordChange(APIView):
    def post(self, *args, **kwargs):
        phone = self.request.data.get('phone', False)
        otp = self.request.data.get('otp', False)
        password = self.request.data.get('password', False)

        if phone and otp and password:
            old = PhoneOTP.objects.filter(Q(phone__iexact = phone) & Q(otp__iexact = otp))
            if old.exists():

                old = old.first()
                if old.forgot_logged:

                    post_data ={
                    'phone':phone,
                    'password':password
                    }
                    user_obj = get_object_or_404(User, phone__iexact=phone)
                    serializer = ForgetPasswordSerializer(data = post_data)

                    if serializer.is_valid():
                        if user_obj:
                            user_obj.set_password(serializer.data.get('password'))
                            user_obj.is_active = True
                            user_obj.save()
                            old.delete()
                            return Response({
                            'status' : True,
                            'detail' : 'Password changed successfully. Please Login'
                            })

                else:
                    return Response({
                    'status' : False,
                    'detail' : 'OTP Verification failed. Please try again in previous step'
                    })

            else:
                return Response({
                'status' : False,
                'detail' : 'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password'
            })

        else:
            return Response({
                'status' : False,
                'detail' : 'Post request have parameters mising.'
            })






class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.last_login is None :
            user.first_login = True
            user.save()
            
        elif user.first_login:
            user.first_login = False
            user.save()
            
        login(request, user)
        return super().post(request, format=None)

def send_otp(phone):
    """
    This is an helper function to send otp to session stored phones or 
    passed phone number as argument.
    """
    count=1
    if phone:
      
        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)
        link = f'http://182.18.162.128/api/mt/SendSMS?Apikey=L8d8O5gjJ0iRo9tQ7NZzOg&senderid=SOEXAM&channel=Trans&DCS=0&flashsms=0&number={phone}&text= Your One Time Password is: {otp_key} It is valid for 02 min. Do not share with anybody, Need Help Call 0144 4901512 &route=2'
        # = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=c85bcfc6-751e-11ec-b710-0200cd936042={phone}&from=mahend&templatename=smsTest&var1={otp_key}'
        result = requests.get(link)
        if Response.status_code == 200:
           
           return otp_key
           
  

    else:
        return False

class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
                 # logic to send the otp and store the phone number and that otp in table. 
            else:
                otp = send_otp(phone)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        count = old.first().count
                        old.first().count = count + 1
                        old.first().save()
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                             phone =  phone, 
                             otp =   otp,
                             count = count
        
                             )
                    if count > 7:
                        return Response({
                            'status' : False, 
                             'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                    
                    
                else:
                    return Response({
                                'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                            })

                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
        else:
            return Response({
                'status': 'False', 'detail' : "I haven't received any phone number. Please do a POST request."
            })


class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent   = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()

                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to registration'
                    })
                else:
                    return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Phone not recognised. Kindly request a new otp with this number'
                })
 

        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or otp was not recieved in Post request'
            })

class Register(APIView):

    '''Takes phone and a password and creates a new user only if otp was verified and phone is new'''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        name=request.data.get('name', False)


        if phone and password:
            
            phone = str(phone)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
            else:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    if old.logged:
                        Temp_data = {'phone': phone, 'password': password,'name':name }

                        serializer = CreateUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()

                        old.delete()
                        return Response({
                            'status' : True, 
                            'detail' : 'Congrts, user has been created successfully.'
                        })

                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'

                        })
                else:
                    return Response({
                    'status' : False,
                    'detail' : 'Phone number not recognised. Kindly request a new otp with this number'
                })
                    




        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or password was not recieved in Post request'
            })



class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer


class UserView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

