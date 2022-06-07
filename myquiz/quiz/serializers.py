from rest_framework import serializers

from quiz .models import QuesModel,QuizModel,ResultModel,AnswerModel

class QuesModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuesModel
        fields = '__all__'
class QuizModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizModel
        fields = '__all__'
        
        
class ResultModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResultModel
        fields = '__all__'
class AnswerModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AnswerModel
        fields = '__all__'