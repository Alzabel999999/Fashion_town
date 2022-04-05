from rest_framework import serializers
from ..models import FAQ, FAQUserQuestion


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = ['id', 'ordering', 'answer', 'question']


class FAQUserQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQUserQuestion
        fields = ['name', 'email', 'category', 'question']
