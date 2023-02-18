from django.shortcuts import render, redirect
from .models import Teacher, SubjectDetails
from .forms import  TeacherForm, SubjectForm, FileForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.base import ContentFile
from zipfile import ZipFile
import pandas as pd
from django.core.files.storage import FileSystemStorage
from rest_framework.generics import (
                                    RetrieveAPIView, \
                                    RetrieveDestroyAPIView, \
                                    ListAPIView, \
                                    CreateAPIView, \
                                    RetrieveUpdateAPIView, \
                                    GenericAPIView, \
                                    )
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SubjectSerializer, TeacherSerializer, SignInSerializer, TeacherUploadSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request

#Subject List
class SubjectsListView(ListAPIView):
    queryset = SubjectDetails.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('search')
        if query is not None:
            subject_details = SubjectDetails.objects.filter(Q(subject_name__icontains=query) )
            return render(request,'teacher/subjects.html',{'subject_details':subject_details})
        subject_details = SubjectDetails.objects.order_by("-date_created")
        return render(request,'teacher/subjects.html',{'subject_details':subject_details})


#Subject Create
class CreateSubjectsView(RetrieveAPIView, CreateAPIView):
    queryset = SubjectDetails.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SubjectSerializer
    
    def retrieve(self, request, *args, **kwargs):
        form = SubjectForm()
        context = {'form':form}
        return render(request,'teacher/form_page.html', context)

    def create(self, request, *args, **kwargs):
        form = SubjectForm(request.data)
        if form.is_valid():
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                form.save()
            else:
                return messages.error(request,'Invalid data has given in input')
        return redirect('/subjects')

#Subject Update
class SubjectUpdateView(RetrieveUpdateAPIView):
    queryset = SubjectDetails.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SubjectSerializer
    pk_url_kwarg = 'pk'

    def retrieve(self, request, pk,  *args, **kwargs):
        subject = SubjectDetails.objects.get(id=pk)
        form = SubjectForm(instance=subject)
        context = {'form':form}
        return render(request,'teacher/form_page.html', context)

    def post(self, request, pk, *args, **kwargs):
        subject = SubjectDetails.objects.get(id=pk)
        form = SubjectForm(request.data, instance=subject)
        if form.is_valid():
            form.save()
        return redirect('/subjects')


#Subject Delete
class SubjectsDestoryView(RetrieveDestroyAPIView):
    queryset = SubjectDetails.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SubjectSerializer
    pk_url_kwarg = 'pk'

    def retrieve(self, request, *args, **kwargs):
        form = SubjectForm()
        context = {'form':form}
        return render(request,'teacher/form_page.html', context)

    def post(self, request, pk, *args, **kwargs):
        subject = SubjectDetails.objects.get(id=pk)
        subject.delete()
        return redirect('/subjects')

#Teacher List
class TeacherListView(ListAPIView):
    queryset = Teacher.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('search')
        if query is not None:
             teachers = Teacher.objects.filter(
            Q(last_name__icontains=query) | 
            Q(subject__subject_name__icontains=query)
            ).order_by("-date_created")

        else:
            teachers = self.queryset.order_by("-date_created")
        return render(request,'teacher/teachers.html',{'teachers':teachers})

#Teacher Create
class TeacherCreateView(RetrieveAPIView, CreateAPIView):
    queryset = Teacher.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TeacherSerializer
    
    def get(self, request, *args, **kwargs):
        form = TeacherForm()
        context = {'form':form}
        return render(request,'teacher/form_page.html', context)

    def post(self, request, *args, **kwargs):
        form = TeacherForm(request.data)
        if form.is_valid():
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                form.save()
            else:
                return messages.error(request,'Invalid data has given in input')
        return redirect('/teachers')

#Teacher Delete
class TeacherDestroyView(RetrieveDestroyAPIView):
    queryset = Teacher.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TeacherSerializer
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        form = TeacherForm()
        context = {'form':form}
        return render(request,'teacher/form_page.html', context)

    def post(self, request, pk, *args, **kwargs):
        teacher = Teacher.objects.get(id=pk)
        teacher.delete()
        teachers = Teacher.objects.all().order_by("-date_created")
        return render(request,'teacher/teachers.html',{'teachers':teachers})

#Teacher Update
class TeacherUpdateView(RetrieveUpdateAPIView):
    queryset = Teacher.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TeacherSerializer
    pk_url_kwarg = 'pk'

    def get(self, request, pk,  *args, **kwargs):
        teacher = Teacher.objects.get(id=pk)
        form = TeacherForm(instance=teacher)
        context = {'form':form}
        return render(request,'teacher/form_page.html', context)

    def post(self, request, pk, *args, **kwargs):
        teacher = Teacher.objects.get(id=pk)
        form = TeacherForm(request.data, instance=teacher)
        if form.is_valid():
            form.save()
        teachers = Teacher.objects.all().order_by("-date_created")
        return render(request,'teacher/teachers.html',{'teachers':teachers})


#Bulk Teacher Upload
class TeacherUploadView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TeacherUploadSerializer
    parser_classes = [MultiPartParser]

    def get(self, request,  *args, **kwargs):
        form = FileForm()
        context = {'form':form}
        return render(request,"teacher/upload_teachers.html",context)

    def post(self, request : Request, *args, **kwargs):
        request_serializer = self.serializer_class(data=request.data)
        request_serializer.is_valid(raise_exception=False)
        
        csv_file = request.FILES["teacher_file"]
        images_file = request.FILES["teacher_images"]
        zip_images = {}
        if not csv_file.name.endswith('.csv'):
            form = FileForm()
            messages.error(request,'File is not CSV type')
            context = {'form':form}
            return render(request,"teacher/upload_teachers.html",context)

        if not images_file.name.endswith('.zip'):
            form = FileForm()
            messages.error(request,'File is not ZIP type')
            context = {'form':form}
            return render(request,"teacher/upload_teachers.html",context)

        if images_file:
            zip_file = ZipFile(images_file)
            for name in zip_file.namelist():
                
                data = zip_file.read(name)
                zip_images[name.split('.')[0]] = data        

        if csv_file.multiple_chunks(): #if file is too large then return
            messages.error(request, 'Upload file is TOO big (%2f MB).' %(csv_file.size/(1000*1000),))
            form = FileForm()
            context = {'form':form}
            return render(request,"teacher/upload_teachers.html",context)
    
        fs = FileSystemStorage()
        file = fs.save('file_name.csv', csv_file)
        df = pd.read_csv(fs.path(file))
        for index, row in df.iterrows():
            try:
    
                data_dict = {}
                if row['Email Address']:
                    data_dict["first_name"] = row['First Name']
                    data_dict["last_name"] = row['Last Name']
                    data_dict["email"] = row['Email Address']
                    data_dict["phone"] = row['Phone Number']
                    data_dict["room_number"] = row['Room Number']
                    form = TeacherForm(data_dict)
                    if form.is_valid():
                        form.save()
                        if row['Profile picture'].split('.')[0] in zip_images.keys():
                            obj = Teacher.objects.get(email=row['Email Address'])
                            content_file = ContentFile(zip_images[row['Profile picture'].split('.')[0]])
                            obj.teacher_profile_pic.save('image_name.jpg', content_file)
                        my_list = [item for item in row['Subjects taught'].split(',') if item]
                        
                        for subject in my_list:
                            obj = Teacher.objects.get(email=row['Email Address'])
                            subject = subject.strip()
                            subject_details = {}
                            subject_details['subject_name'] = subject.title()
                            subjects_count = obj.subject.all().count()
                            
                            if int(subjects_count) <5:
                                ignore_duplicate = SubjectDetails.objects.filter(subject_name=subject_details['subject_name']).count()
                                if ignore_duplicate == 0:
                                    form = SubjectForm(subject_details)
                                    if form.is_valid():
                                        form.save()
                                sub_obj = SubjectDetails.objects.get(subject_name=subject_details['subject_name'])
                                obj.subject.add(sub_obj)
                        
            except Exception as e:
                print('Exception occured during saving cutomer details' ,e)
        teachers = Teacher.objects.all()
        return render(request,'teacher/teachers.html',{'teachers':teachers}) 


#Teacher Subjects
class TeacherSubjectsListView(RetrieveAPIView):
    queryset = Teacher.objects.all()
    permission_classes = (IsAuthenticated,)
    pk_url_kwarg = 'pk'


    def get(self, request, pk, *args, **kwargs):
        queryset = self.queryset.get(id=pk).subject.all()
        
        context = {'subject_details': queryset}
        return render(request,'teacher/teacher_subjects.html', context)

#SignIn View
class SignIntView(GenericAPIView):
    serializer_class = SignInSerializer

    def get(self, request):
        return render(request, 'teacher/signin.html',{})

    def post(self, request, *args, **kwargs):
        request_serializer = self.serializer_class(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        user = authenticate(request, **request_serializer.data)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,"Username or Password is not correct.")
        return render(request, 'teacher/signin.html',{})

#Signout View
class SignoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('signin')
