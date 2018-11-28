# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.shortcuts import redirect,render,Http404
from forms import RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from models import Msg_inbox
from django.db.models import Q
from django.utils.timezone import datetime
class Home(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')
        else:
            m = []
            msgs = Msg_inbox.objects.filter(Q(receiver=request.user)|Q(sender=request.user)).values('sender__username').distinct()
            for i in msgs:
                if i['sender__username'] != unicode(request.user):
                    m.append(i)
            return render(request,'index.html',{'senders':m,'user':request.user})
class Msg(View):
    friend = None
    def get(self,request,friend=friend):
        self.friend = friend
        try:
            if request.user.is_authenticated:
                if self.friend:
                    receiver = User.objects.get(username=self.friend)
                    if receiver:
                        v = []
                        combined_queryset = Msg_inbox.objects.filter(Q(receiver=request.user)|Q(sender=request.user) | Q(receiver=receiver))
                        ordered_queryset = combined_queryset.order_by('sent_time').values('sender__username','receiver__username','msg_body','sent_time')
                        for i in ordered_queryset:
                            if i['receiver__username'] == unicode(request.user):
                                i['type'] = 'right'
                                i['rtype'] = 'left'
                                v.append(i)
                            else:
                                i['type'] = 'left'
                                i['rtype'] = 'right'
                                v.append(i)
                        return render(request, 'index.html', {'msgs':v,'user':request.user})
                    else:
                        return redirect('/')
                else:
                    raise Http404
            else:
                return redirect('/login')
        except:
            raise Http404
    def post(self,request):
        try:
            if request.user.is_authenticated:
                data = request.POST
                if data:
                    receiver = User.objects.get(username=data['receiver'])
                    if receiver:
                        m = Msg_inbox(sender=request.user,receiver=receiver,msg_body=data['msg_body'],sent_time=datetime.now(),received_time=datetime.now())
                        m.save()
                        return redirect('/')
                else:
                    raise Http404
            else:
                return redirect('/login')
        except:
            raise Http404
class Login(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        if request.POST:
            uname = request.POST['username']
            password = request.POST['password']
            u = authenticate(username=uname,password=password)
            if u is not None:
                login(request,u)
                return redirect('/')
        return render(request,'login.html',{'error':'Username or Password Not Exist'})
class Log_out(View):
    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('/login')
class Register(View):
    form_class = RegisterForm
    template_name = 'register.html'
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                vld = validate_password(password=password)
                print "Valid"
                print vld
                if vld == None:
                    email = form.cleaned_data['email']
                    User.objects.create_user(username=username, email=email, password=password)
                    user = authenticate(username=username,password=password)
                    if user is not None:
                        if user.is_active:
                            login(request,user)
                            return redirect('/')
                else:
                    return render(request, self.template_name,{'form':form,'error':["Form data not accurate.","Please check your inputs"]})
            else:
                return render(request, self.template_name, {'form': form, 'error': ["Form data not accurate.","Please check your inputs"]})
        except Exception, err:
            print err
            return render(request, self.template_name,{'form': form, 'error': err})