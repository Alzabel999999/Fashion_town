from rest_framework import serializers
from ..models import ProblemArea


class ProblemAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemArea
        fields = ['id', 'problem_area']
