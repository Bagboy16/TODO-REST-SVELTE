from rest_framework import serializers
from todo.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        return user
    
    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user


class StepSerializer(serializers.ModelSerializer):

    class Meta:
        model = steps
        fields = ['id', 'description', 'is_completed']


class TaskSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    class Meta:
        model = tasks
        fields = ['id', 'title', 'description', 'is_completed', 'created_at', 'steps', 'user_id']

    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])
        print(steps_data)
        task = tasks.objects.create(**validated_data)
        for step in steps_data:
            steps.objects.create(task_id = task, **step)
        return task

    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps', [])
        instance = super().update(instance, validated_data)
        existing_steps = {step.id: step for step in steps.objects.filter(task_id = instance)}
        for step_data in steps_data:
            step_id = step_data.get('id')
            if step_id:
                existing_steps.pop(step_id).update(**step_data)
            else:
                steps.objects.create(task_id= instance, **step_data)
        for step in existing_steps.values():
            step.delete()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        step = steps.objects.filter(task_id = instance)
        representation['steps'] = StepSerializer(step, many=True).data
        return representation
