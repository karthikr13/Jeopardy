#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 22:44:15 2019

@author: karthik
"""

#defines each possible URL in the /board URL that the user can hit
from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name = 'index'),
        path('<int:question_id>/', views.detail, name = 'detail'),
        path('random/', views.random_question, name = 'random'),
        path('gameboard/', views.gameboard, name = 'gameboard'),
        path('<str:search_string>/page=<int:page_number>', views.search, name = 'search'),
        path('<str:search_string>/', views.search_no_page, name = 'search_no_page')
]