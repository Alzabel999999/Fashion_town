from rest_framework import serializers
from ..models import CommonFeedback, CommonFeedbackAttachment


class CommonFeedbackSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = CommonFeedback
        fields = ['problem_area', 'name', 'email', 'message']

    def create(self, validated_data):
        instance = super(CommonFeedbackSerializer, self).create(validated_data)
        request = self.context['request']
        files = request.FILES.getlist('files', [])
        for file in files:
            if file.size < 5000000:
                CommonFeedbackAttachment.objects.create(common_feedback=instance, attachment=file)
        return instance
