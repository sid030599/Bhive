from rest_framework import serializers
from .models import User, FundFamily, MutualFund, Portfolio, Investment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Portfolio.objects.create(user=user)  # Create portfolio on user creation
        return user

class FundFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = FundFamily
        fields = '__all__'

class MutualFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutualFund
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    funds = MutualFundSerializer(many=True)

    class Meta:
        model = Portfolio
        fields = ['funds']

class FundFamilyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundFamily
        fields = ['id', 'name']

class MutualFundCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutualFund
        fields = ['id', 'name', 'family', 'nav', 'is_open_ended']

class InvestmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'portfolio', 'fund', 'amount']
