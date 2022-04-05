from rest_framework import serializers
from ..models import QuestionCategory


class QuestionCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionCategory
        fields = ['id', 'category']
