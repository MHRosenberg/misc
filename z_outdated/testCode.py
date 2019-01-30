#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 21:31:26 2018

@author: matthew
"""

for i in range(0,10):
    text = "This is {variable_a} formatted  {varB} string".format(variable_a= i, varB = i +5)
    print(text)
    
text = "This is another {0} formatted string \
with multiple variables like {1} {2} {3}.".format(
    "variable based", 
    "some random", 
    "replacement", 
    "text"
    )
print(text)

text = "The %%s format string is not as %s, but still very %s." %("robust", "useful")
print(text)