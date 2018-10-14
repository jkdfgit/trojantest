#!/usr/bin/python
#-*- coding: utf-8 -*-

def run(**args):
	f = open("keydump.txt", "r")
	data = f.read()
	f.close()
	return str(data)
