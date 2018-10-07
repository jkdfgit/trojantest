#!/usr/bin/python
#-*- coding: utf-8 -*-

import os, platform

platform_information = str(platform.platform())

def ipInformation(command):
	parsing = os.popen(command)
	result = ""
	for i in parsing.readlines():
		result += i
	return str(b)

def run(**args):
	if "windows" in str(platform_information).lower():
		return ipInformation("ipconfig")
	elif ("linux" in str(platform_information).lower()) or ("unix" in str(platform_information).lower()):
		return ipInformation("ifconfig")
