from rest_framework import serializers

from .models import SubjectDetails, Teacher


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubjectDetails
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = "__all__"


class SignInSerializer(serializers.Serializer):


    username = serializers.CharField(min_length=1)
    password = serializers.CharField(min_length=1)

class TeacherUploadSerializer(serializers.Serializer):

    teacher_file = serializers.FileField()
    teacher_images = serializers.FileField()
