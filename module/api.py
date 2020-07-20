from django.db import transaction
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, mixins, authentication, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

import docker as docker_env

from module.models import *
from module.serializers import *
from module.utils import handle_uploaded_file

import os
import json
import time
import string
import random


class createExperiment(generics.CreateAPIView):  # NOTE Create Experiment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetrieveModuleSerializer

    def create(self, request, *args, **kwargs):
        try:
            print(self.kwargs['pk'])
            docker = Docker.objects.get(
                image_name=self.kwargs['pk'], state__in=['active', 'builded'])

            if docker.state == 'builded':
                if not docker.user.id == self.request.user.id:
                    return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)

            input = docker.elements_type.filter(kind='input').get()
            output = docker.elements_type.filter(kind='output')

            if output.count() == 0:
                output = False
            else:
                output = True

            if int(input.len) > 0:
                experiment, created = Experiment.objects.get_or_create(
                    docker=docker, user=self.request.user, state='created')
                if created:
                    experiment.create_workdir(outputs=output)
                experiments = [experiment]
            else:
                experiments = Experiment.objects.filter(
                    docker=docker, user=self.request.user, state='created')
                if experiments.count() == 0:
                    experiment = Experiment.objects.create(
                        docker=docker, user=self.request.user, state='created')
                    experiment.create_workdir(outputs=output)
                    experiments = [experiment]

            element_data = []
            for exp in experiments:
                for data in exp.elements.all():
                    element_data.append(data)

            data = dict(**self.serializer_class(docker).data)
            data["elements"] = RetrieveElementDataSerializer(
                element_data, many=True).data
            return Response(data)
        except ObjectDoesNotExist:
            return Response("Module not found",
                            status=status.HTTP_404_NOT_FOUND)


class uploadExamples(generics.CreateAPIView):  # NOTE Upload examples experiment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetrieveElementDataSerializer

    def create(self, request, *args, **kwargs):
        try:
            if self.request.user.role == 'developer':
                docker = Docker.objects.get(
                    user=self.request.user, image_name=self.kwargs['pk'], state__in=['active'])

            elif self.request.user.role == 'user':
                docker = Docker.objects.get(
                    subscribers=self.request.user, image_name=self.kwargs['pk'], state__in=['active'])

            elif self.request.user.role == 'admin':
                docker = Docker.objects.get(
                    image_name=self.kwargs['pk'], state__in=['active'])

            else:
                return Response("Permissions denied", status=status.HTTP_403_FORBIDDEN)

            input = docker.elements_type.filter(kind='input').get()
            output = docker.elements_type.filter(kind='output')

            if output.count() == 0:
                output = False
            else:
                output = True

            experiment = None

            if int(input.len) > 0:
                experiment, created = Experiment.objects.get_or_create(
                    docker=docker, user=self.request.user, state='created')
                if created:
                    experiment.create_workdir(outputs=output)

                for id in request.data["examples"]:
                    ref = ElementData.objects.get(id=id)
                    element = ElementData.objects.create(
                        experiment=experiment, kind='input', element=Element.objects.get(name='input'), name=ref.name)
                    ref.copy_input(
                        f"{experiment.get_workdir()}/inputs/input_{element.id}")
                    element.save()
            else:
                experiments = Experiment.objects.filter(
                    docker=docker, user=self.request.user, state='created')

                if experiments.count() > 0:
                    for exp in experiments:
                        if exp.elements.all().count() == 0:
                            experiment = exp

                    if not experiment:
                        experiment = Experiment.objects.create(
                            docker=docker, user=self.request.user, state='created')
                        experiment.create_workdir(outputs=output)

                else:
                    experiment, created = Experiment.objects.create(
                        docker=docker, user=self.request.user, state='created')
                    if created:
                        experiment.create_workdir(outputs=output)

                ref = ElementData.objects.get(id=request.data["examples"][0])
                element = ElementData.objects.create(
                    experiment=experiment, kind='input', element=Element.objects.get(name='input'), name=ref.name)
                element.value = ref.copy_input(
                    f"{experiment.get_workdir()}/inputs/input_{element.id}.{ref.name.split('.')[-1]}")
                element.save()

                for id in request.data["examples"][1:]:
                    experiment = Experiment.objects.create(
                        docker=docker, user=self.request.user, state='created')
                    experiment.create_workdir(outputs=output)
                    ref = ElementData.objects.get(id=id)
                    element = ElementData.objects.create(
                        experiment=experiment, kind='input', element=Element.objects.get(name='input'), name=ref.name)
                    element.value = ref.copy_input(
                        f"{experiment.get_workdir()}/inputs/input_{element.id}")
                    element.save()

            return Response(True)
        except ObjectDoesNotExist:
            return Response("Module not found",
                            status=status.HTTP_404_NOT_FOUND)


class createElementData(generics.CreateAPIView):  # NOTE Create element data
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetrieveElementDataSerializer

    def create(self, request, *args, **kwargs):
        try:
            docker = Docker.objects.get(
                image_name=self.kwargs['pk'], state__in=['active', 'builded'])

            if docker.state == 'builded':
                if not docker.user.id == self.request.user.id:
                    return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)

            input = docker.elements_type.filter(kind='input').get()
            output = docker.elements_type.filter(kind='output')

            if output.count() == 0:
                output = False
            else:
                output = True

            experiment = None

            if int(input.len) > 0:
                experiment, created = Experiment.objects.get_or_create(
                    docker=docker, user=self.request.user, state='created')
                if created:
                    experiment.create_workdir(outputs=output)
            else:
                experiments = Experiment.objects.filter(
                    docker=docker, user=self.request.user, state='created')

                if experiments.count() > 0:
                    for exp in experiments:
                        if exp.elements.all().count() == 0:
                            experiment = exp

                    if not experiment:
                        experiment = Experiment.objects.create(
                            docker=docker, user=self.request.user, state='created')
                        experiment.create_workdir(outputs=output)

                else:
                    experiment, created = Experiment.objects.create(
                        docker=docker, user=self.request.user, state='created')
                    if created:
                        experiment.create_workdir(outputs=output)

            file = request.FILES['file']

            if docker.state == 'builded':
                element = ElementData.objects.create(
                    experiment=experiment, kind='input', element=Element.objects.get(name='input'), name=file.name, example=True)
            else:
                element = ElementData.objects.create(
                    experiment=experiment, kind='input', element=Element.objects.get(name='input'), name=file.name)

            element.value = handle_uploaded_file(
                file, experiment.inputs(), 'input_{}'.format(element.id))

            element.save()
            return Response(self.serializer_class(element).data)
        except ObjectDoesNotExist:
            return Response("Module not found",
                            status=status.HTTP_404_NOT_FOUND)


class DeleteElementData(generics.DestroyAPIView):  # NOTE Delete element data
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetrieveElementDataSerializer

    def delete(self, request, *args, **kwargs):
        input = ElementData.objects.get(id=self.kwargs['pk'])
        input.delete()

        experiment = input.experiment
        experiments = experiment.docker.experiments.filter(
            user=self.request.user, state='created')
        if experiments.count() > 1:
            experiment.delete()
        return Response(True)


class listExperiments(generics.ListAPIView):  # NOTE List experiments
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateExperimentSerializer

    def get_queryset(self):
        return Experiment.objects.filter(state='executing')


class retrieveExperiment(generics.RetrieveAPIView):  # NOTE Show experiment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateExperimentSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            experiment = Experiment.objects.get(
                id=self.kwargs['pk'], user=self.request.user)
            data = dict(self.serializer_class(experiment).data)
            data["elements"] = {}
            data["docker"] = ListModuleSerializer(experiment.docker).data
            data["experiments"] = [str(i.id) for i in experiment.docker.experiments.filter(
                user=self.request.user, state__in=['executed', 'executing', 'error']).all()]

            for element in experiment.elements.all():
                if element.kind in data["elements"]:
                    data["elements"][element.kind].append(
                        element.get_public_path() if element.get_public_path() else element.value)
                else:
                    data["elements"][element.kind] = [
                        element.get_public_path() if element.get_public_path() else element.value]

            return Response(
                data
            )
        except ObjectDoesNotExist:
            return Response("Module not found",
                            status=status.HTTP_404_NOT_FOUND)
