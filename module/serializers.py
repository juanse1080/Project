from rest_framework import serializers
from .models import *
from authenticate.models import User
from django.db import transaction
from module.utils import handle_uploaded_file


class ImageSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=500)
    label = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)


class CreateElementsType(serializers.Serializer):
    kind = serializers.CharField(max_length=30)
    len = serializers.IntegerField()
    state = serializers.BooleanField(required=False)
    value = serializers.CharField()


class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "photo"]


class CheckBuildSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=32)


class ElementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementType
        fields = '__all__'


class ListModuleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    elements_type = ElementTypeSerializer(many=True)

    class Meta:
        model = Docker
        fields = '__all__'


class RetrieveModuleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    elements_type = ElementTypeSerializer(many=True)

    class Meta:
        model = Docker
        fields = ["elements_type", "image_name", "subscribers", "classname", "created_at", "description",
                  "extensions", "user", "file", "image", "name", "protocol", "state", "view", "workdir", "background"]


class RetriveExperiment(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ["id", "state"]


class RetrieveElementDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementData
        fields = '__all__'


class ListExamplesModule(serializers.ModelSerializer):
    href = serializers.TimeField()

    class Meta:
        model = ElementData
        fields = '__all__'


class CreateExperimentSerializer(serializers.ModelSerializer):
    docker = RetrieveModuleSerializer()

    class Meta:
        model = Experiment
        fields = '__all__'


class ListRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = '__all__'


class RetriveExperimentSerializer(serializers.ModelSerializer):
    docker = RetrieveModuleSerializer()
    records = ListRecordsSerializer(many=True)

    class Meta:
        model = Experiment
        fields = '__all__'


class ListExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'


class ListExperimentIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ['id']


class CreateModuleSerializer(serializers.ModelSerializer):
    elements = CreateElementsType(many=True)
    background = serializers.ImageField()

    def create(self, validated_data):
        temp = validated_data.copy()
        del temp["elements"]
        with transaction.atomic():
            docker = Docker(**temp)
            docker.background = handle_uploaded_file(
                temp["background"], docker.get_path(), f"img_{docker.id}")
            docker.save()
            for element in validated_data["elements"]:
                ElementType.objects.create(
                    kind=element['kind'],
                    docker=docker,
                    element=Element.objects.get(name=element['kind']),
                    value=element['value'],
                    len=element['len']
                )
        return docker

    class Meta:
        model = Docker
        fields = ['id', 'image_name', 'proto', 'user', 'protocol',
                  'name', 'description', 'image', 'workdir', 'file', 'classname', 'elements', 'view', 'extensions', 'background']
