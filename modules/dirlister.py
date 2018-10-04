#!/usr/bin/python

import os

def run(**args):
	print "[*] In dirlistermodule."
	files = os.listdir(".")

	return str(files)
