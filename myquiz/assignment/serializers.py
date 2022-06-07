from rest_framework import serializers

from assignment .models import Assignment
from assignment .models import SubmitAssignment

class AssignmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assignment
        fields = '__all__'
class SubmitAssignmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SubmitAssignment
        fields = '__all__'