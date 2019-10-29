#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 22:44:15 2019

@author: karthik
"""

from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name = 'index'),
        path('<int:question_id>/', views.detail, name = 'detail'),
        path('random/', views.random_question, name = 'random'),
        path('gameboard/', views.gameboard, name = 'gameboard'),
        path('<str:search_string>/', views.search, name = 'search')
]
'''
path('<str:category>/', views.search_category, name = 'search'),
        path('<str:category>/<int:score>/', views.search_category_score, name = 'search')
'''