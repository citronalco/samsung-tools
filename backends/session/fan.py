#!/usr/bin/env python
# coding=UTF-8
#
# Samsung-Tools
# 
# Part of the 'Linux On My Samsung' project - <http://www.voria.org/forum>
#
# Copyleft (C) 2010 by
# Fortunato Ventre (voRia) - <vorione@gmail.com> - <http://www.voria.org>
#
# 'Samsung-Tools' is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# <http://www.gnu.org/licenses/gpl.txt>

import dbus.service

from backends.globals import *
from backends.session.util.locales import *
from backends.session.util.icons import *

class Fan(dbus.service.Object):
	""" Control CPU fan """
	def __init__(self, notify = None, conn = None, object_path = None, bus_name = None):
		dbus.service.Object.__init__(self, conn, object_path, bus_name)
		self.system_bus = None
		self.proxy = None
		self.interface = None
		self.notify = notify
	
	def __connect(self):
		""" Enable connection to system backend """
		self.system_bus = dbus.SystemBus()
		self.proxy = self.system_bus.get_object(SYSTEM_INTERFACE_NAME, SYSTEM_OBJECT_PATH_FAN)
		self.interface = dbus.Interface(self.proxy, SYSTEM_INTERFACE_NAME)
	
	def __not_available(self):
		""" Inform the user that the CPU fan control is not available. """
		""" Return always 'False'. """
		if self.notify != None:
			pass # TODO
		return False
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def IsAvailable(self, sender = None, conn = None):
		""" Check if the CPU fan control is available. """
		""" Return 'True' if available, 'False' if disabled. """
		self.__connect()
		return self.interface.IsAvailable()
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'i',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Status(self, sender = None, conn = None):
		""" Check current mode. """
		"""Return 0 if 'normal', 1 if 'silent', 2 if 'speed'. """
		""" Return 3 if any error. """
		if not self.IsAvailable():
			self.__not_available()
			return 3
		self.__connect()
		status = self.interface.Status()
		if self.notify != None:
			pass # TODO
		return status
			
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetNormal(self, sender = None, conn = None):
		""" Turn to 'normal' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available()
		self.__connect()
		result = self.interface.SetNormal()
		if self.notify != None:
			pass # TODO
		return result
		
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetSilent(self, sender = None, conn = None):
		""" Turn to 'silent' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available()
		self.__connect()
		result = self.interface.SetSilent()
		if self.notify != None:
			pass # TODO
		return result
		
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def SetSpeed(self, sender = None, conn = None):
		""" Turn to 'speed' mode. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available()
		self.__connect()
		result = self.interface.SetSpeed()
		if self.notify != None:
			pass # TODO
		return result
	
	@dbus.service.method(SESSION_INTERFACE_NAME, in_signature = None, out_signature = 'b',
						sender_keyword = 'sender', connection_keyword = 'conn')
	def Cycle(self, sender = None, conn = None):
		""" Set the next mode in a cyclic way. """
		""" Return 'True' on success, 'False' otherwise. """
		if not self.IsAvailable():
			return self.__not_available()
		self.__connect()
		result = self.interface.Cycle()
		if self.notify != None:
			pass # TODO
		return result
