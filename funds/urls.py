# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('fund-families/', views.FundFamilyListView.as_view(), name='fund-families'),
    path('mutual-funds/<int:family_id>/', views.MutualFundListView.as_view(), name='mutual-funds'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path('fund-families/create/', views.FundFamilyCreateView.as_view(), name='create-fund-family'),
    path('mutual-funds/create/', views.MutualFundCreateView.as_view(), name='create-mutual-fund'),
    path('investments/create/', views.InvestmentCreateView.as_view(), name='create-investment'),
    path('investments/', views.InvestmentListView.as_view(), name='list-investments'),
]