# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 15:52:48 2021

@author: New User
"""

import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "/supervisors")
print(response.json())