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
        path('board/<int:question_id>/', views.detail, name = 'detail'),
        path('board/<str:category>', views.search, name = 'search')
]