import requests
from rest_framework import generics, views, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import FundFamily, MutualFund, Portfolio, Investment
from .serializer import (
    UserSerializer, FundFamilySerializer, PortfolioSerializer,
    FundFamilyCreateSerializer, MutualFundCreateSerializer, InvestmentCreateSerializer
)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['username'] = user.username

        return token

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class FundFamilyListView(generics.ListAPIView):
    queryset = FundFamily.objects.all()
    serializer_class = FundFamilySerializer

class MutualFundListView(views.APIView):
    def get(self, request, family_id):
        family = FundFamily.objects.get(id=family_id)
        response = requests.get(
            "https://latest-mutual-fund-nav.p.rapidapi.com/funds",
            params={"fundFamily": family.name, "openEnded": "true"},
            headers={"X-RapidAPI-Key": "your_rapidapi_key"}
        )
        data = response.json()
        # Save or process mutual fund data
        return Response(data)


class PortfolioView(generics.RetrieveAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.portfolio


# Create FundFamily
class FundFamilyCreateView(generics.CreateAPIView):
    queryset = FundFamily.objects.all()
    serializer_class = FundFamilyCreateSerializer
    # permission_classes = [permissions.IsAuthenticated]

# Create MutualFund
class MutualFundCreateView(generics.CreateAPIView):
    queryset = MutualFund.objects.all()
    serializer_class = MutualFundCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create Investment
class InvestmentCreateView(generics.CreateAPIView):
    queryset = Investment.objects.all()
    serializer_class = InvestmentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the user's portfolio to the investment
        portfolio = Portfolio.objects.get(user=self.request.user)
        serializer.save(portfolio=portfolio)


# List all investments in the user's portfolio
class InvestmentListView(generics.ListAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)
