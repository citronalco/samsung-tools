#!/usr/bin/python3
# coding=UTF-8
#
# Samsung-Tools
#
# Part of the 'Linux On My Samsung' project - <http://loms.voria.org>
#
# Copyleft (C) 2010 by
# Fortunato Ventre - <vorione@gmail.com> - <http://www.voria.org>
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

import os
import sys
import dbus

import gettext
_ = gettext.gettext
gettext.bindtextdomain("samsung-tools")
gettext.textdomain("samsung-tools")

WORK_DIRECTORY = "/usr/share/samsung-tools"
sys.path.append(WORK_DIRECTORY)

from backends.globals import *
from backends.session.util.locales import *

quiet = False

class Backlight():

    def __init__(self, option):
        self.option = option
        success = False
        retry = 3
        while retry > 0 and not success:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    SESSION_INTERFACE_NAME,
                    SESSION_OBJECT_PATH_BACKLIGHT)
                self.interface = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
                success = True
            except:
                retry = retry - 1
        if retry == 0:
            print ("Backlight control: unable to connect to session service!")
            sys.exit(1)

    def __on(self):
        return self.interface.Enable()

    def __off(self):
        return self.interface.Disable()

    def __status(self):
        return self.interface.IsEnabled()

    def __toggle(self):
        return self.interface.Toggle()

    def apply(self):
        if self.option is None:
            return
        if self.option == "on":
            result = self.__on()
            if not quiet:
                if result:
                    print (BACKLIGHT_ENABLED)
                else:
                    print (BACKLIGHT_ENABLING_ERROR)
        if self.option == "off":
            result = self.__off()
            if not quiet:
                if result:
                    print (BACKLIGHT_DISABLED)
                else:
                    print (BACKLIGHT_DISABLING_ERROR)
        if self.option == "toggle":
            result = self.__toggle()
            if not quiet:
                if result:
                    status = self.__status()
                    if status:
                        print (BACKLIGHT_ENABLED)
                    else:
                        print (BACKLIGHT_DISABLED)
                else:
                    print (BACKLIGHT_TOGGLING_ERROR)
        if self.option == "hotkey":
            from time import sleep
            from subprocess import Popen, PIPE
            tempfiles = ".samsung-tools-backlight-" + str(os.getuid()) + "-"
            tempfile = "/tmp/" + tempfiles + str(os.getpid())
            toggle = True
            try:
                ls = Popen(['ls /tmp/' + tempfiles + '*'],
                           stdout=PIPE, stderr=PIPE, shell=True)
                if len(ls.communicate()[0]) != 0:
                    toggle = False
            except:
                pass
            if toggle:
                Backlight("toggle").apply()
                try:
                    file = open(tempfile, "w").close()  # create temp file
                except:
                    pass
                sleep(0.5)
                try:
                    os.remove(tempfile)
                except:
                    pass
        if self.option == "status":
            result = self.__status()
            if not quiet:
                if result:
                    print (BACKLIGHT_STATUS_ENABLED)
                else:
                    print (BACKLIGHT_STATUS_DISABLED)


class Bluetooth():

    def __init__(self, option, use_notify=False):
        self.option = option
        self.use_notify = use_notify
        success = False
        retry = 3
        while retry > 0 and not success:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    SESSION_INTERFACE_NAME,
                    SESSION_OBJECT_PATH_BLUETOOTH)
                self.interface = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
                success = True
            except:
                retry = retry - 1
        if retry == 0:
            print ("Bluetooth control: unable to connect to session service!")
            sys.exit(1)

    def __is_available(self):
        return self.interface.IsAvailable()

    def __on(self):
        return self.interface.Enable(self.use_notify)

    def __off(self):
        return self.interface.Disable(self.use_notify)

    def __toggle(self):
        return self.interface.Toggle(self.use_notify)

    def __status(self):
        return self.interface.IsEnabled(self.use_notify)

    def apply(self):
        if self.option is None:
            return
        if not self.__is_available():
            if not quiet:
                print (BLUETOOTH_NOT_AVAILABLE)
            self.__status()  # needed to show notification
            return
        if self.option == "on":
            result = self.__on()
            if not quiet:
                if result:
                    print (BLUETOOTH_ENABLED)
                else:
                    print (BLUETOOTH_ENABLING_ERROR)
        if self.option == "off":
            result = self.__off()
            if not quiet:
                if result:
                    print (BLUETOOTH_DISABLED)
                else:
                    print (BLUETOOTH_DISABLING_ERROR)
        if self.option == "toggle":
            result = self.__toggle()
            if not quiet:
                if result:
                    # Temporary disable notifications
                    n = self.use_notify
                    self.use_notify = False
                    status = self.__status()
                    self.use_notify = n
                    # Notification re-enabled
                    if status:
                        print (BLUETOOTH_ENABLED)
                    else:
                        print (BLUETOOTH_DISABLED)
                else:
                    print (BLUETOOTH_TOGGLING_ERROR)
        if self.option == "hotkey":
            from time import sleep
            from subprocess import Popen, PIPE
            tempfiles = ".samsung-tools-bluetooth-" + str(os.getuid()) + "-"
            tempfile = "/tmp/" + tempfiles + str(os.getpid())
            toggle = True
            try:
                ls = Popen(['ls /tmp/' + tempfiles + '*'],
                           stdout=PIPE, stderr=PIPE, shell=True)
                if len(ls.communicate()[0]) != 0:
                    toggle = False
            except:
                pass
            if toggle:
                Bluetooth("toggle", self.use_notify).apply()
                try:
                    file = open(tempfile, "w").close()  # create temp file
                except:
                    pass
                sleep(0.5)
                try:
                    os.remove(tempfile)
                except:
                    pass
        if self.option == "status":
            result = self.__status()
            if not quiet:
                if result:
                    print (BLUETOOTH_STATUS_ENABLED)
                else:
                    print (BLUETOOTH_STATUS_DISABLED)


class Cpu():

    def __init__(self, option, use_notify=False):
        self.option = option
        self.use_notify = use_notify
        success = False
        retry = 3
        while retry > 0 and not success:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    SESSION_INTERFACE_NAME,
                    SESSION_OBJECT_PATH_CPU)
                self.interface = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
                success = True
            except:
                retry = retry - 1
        if retry == 0:
            print ("CPU fan control: unable to connect to session service!")
            sys.exit(1)

    def __is_temperature_available(self):
        return self.interface.IsTemperatureAvailable()

    def __is_fan_available(self):
        return self.interface.IsFanAvailable()

    def __temp(self):
        return self.interface.GetTemperature()

    def __normal(self):
        return self.interface.SetFanNormal(self.use_notify)

    def __silent(self):
        return self.interface.SetFanSilent(self.use_notify)

    def __overclock(self):
        return self.interface.SetFanOverclock(self.use_notify)

    def __cycle(self):
        return self.interface.Cycle(self.use_notify)

    def __status(self):
        return self.interface.Status(self.use_notify)

    def apply(self):
        if self.option is None:
            return
        if self.__is_temperature_available() and self.option != "hotkey" and not quiet:
            print (CPU_TEMPERATURE + " " + self.__temp() + " °C")
        if not self.__is_fan_available():
            if not quiet:
                print (FAN_NOT_AVAILABLE)
            self.__status()  # needed to show notification
            return
        if self.option == "normal":
            result = self.__normal()
            if not quiet:
                if result:
                    print (FAN_STATUS_NORMAL)
                else:
                    print (FAN_SWITCHING_ERROR)
        if self.option == "silent":
            result = self.__silent()
            if not quiet:
                if result:
                    print (FAN_STATUS_SILENT)
                else:
                    print (FAN_SWITCHING_ERROR)
        if self.option == "overclock":
            result = self.__overclock()
            if not quiet:
                if result:
                    print (FAN_STATUS_OVERCLOCK)
                else:
                    print (FAN_SWITCHING_ERROR)
        if self.option == "cycle":
            result = self.__cycle()
            if not quiet:
                if result:
                    # Temporary disable notifications
                    n = self.use_notify
                    self.use_notify = False
                    mode = self.__status()
                    self.use_notify = n
                    # Notification re-enabled
                    if mode == 0:
                        print (FAN_STATUS_NORMAL)
                    if mode == 1:
                        print (FAN_STATUS_SILENT)
                    if mode == 2:
                        print (FAN_STATUS_OVERCLOCK)
                    if mode == 3:
                        print (FAN_STATUS_ERROR)
                else:
                    print (FAN_SWITCHING_ERROR)
        if self.option == "hotkey":
            from time import sleep
            from subprocess import Popen, PIPE
            tempfiles = ".samsung-tools-cpu-" + str(os.getuid()) + "-"
            tempfile = "/tmp/" + tempfiles + str(os.getpid())
            hotkey = True
            try:
                ls = Popen(['ls /tmp/' + tempfiles + '*'],
                           stdout=PIPE, stderr=PIPE, shell=True)
                if len(ls.communicate()[0]) != 0:
                    hotkey = False
            except:
                pass
            if hotkey:
                Cpu("hotkey2", self.use_notify).apply()
                try:
                    file = open(tempfile, "w").close()  # create temp file
                except:
                    pass
                sleep(0.5)
                try:
                    os.remove(tempfile)
                except:
                    pass
        if self.option == "hotkey2":
            from time import sleep
            from subprocess import Popen, PIPE
            tempfiles = ".samsung-tools-cpufan-" + str(os.getuid()) + "-"
            tempfile = "/tmp/" + tempfiles + str(os.getpid())
            action = "status"
            try:
                ls = Popen(['ls /tmp/' + tempfiles + '*'],
                           stdout=PIPE, stderr=PIPE, shell=True)
                if len(ls.communicate()[0]) != 0:
                    action = "cycle"
            except:
                pass
            Cpu(action, self.use_notify).apply()
            try:
                file = open(tempfile, "w").close()  # create temp file
            except:
                pass
            sleep(9.5)
            try:
                os.remove(tempfile)
            except:
                pass
        if self.option == "status":
            result = self.__status()
            if not quiet:
                if result == 0:
                    print (FAN_STATUS_NORMAL)
                if result == 1:
                    print (FAN_STATUS_SILENT)
                if result == 2:
                    print (FAN_STATUS_OVERCLOCK)
                if result == 3:
                    print (FAN_STATUS_ERROR)


class Webcam():

    def __init__(self, option, use_notify=False):
        self.option = option
        self.use_notify = use_notify
        success = False
        retry = 3
        while retry > 0 and not success:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    SESSION_INTERFACE_NAME,
                    SESSION_OBJECT_PATH_WEBCAM)
                self.interface = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
                success = True
            except:
                retry = retry - 1
        if retry == 0:
            print ("Webcam control: unable to connect to session service!")
            sys.exit(1)

    def __is_available(self):
        return self.interface.IsAvailable()

    def __on(self):
        return self.interface.Enable(self.use_notify)

    def __off(self):
        return self.interface.Disable(self.use_notify)

    def __toggle(self):
        return self.interface.Toggle(self.use_notify)

    def __status(self):
        return self.interface.IsEnabled(self.use_notify)

    def apply(self):
        if self.option is None:
            return
        if not self.__is_available():
            if not quiet:
                print (WEBCAM_NOT_AVAILABLE)
            self.__status()  # needed to show notification
            return
        if self.option == "on":
            result = self.__on()
            if not quiet:
                if result:
                    print (WEBCAM_ENABLED)
                else:
                    print (WEBCAM_ENABLING_ERROR)
        if self.option == "off":
            result = self.__off()
            if not quiet:
                if result:
                    print (WEBCAM_DISABLED)
                else:
                    print (WEBCAM_DISABLING_ERROR)
        if self.option == "toggle":
            result = self.__toggle()
            if not quiet:
                if result:
                    # Temporary disable notifications
                    n = self.use_notify
                    self.use_notify = False
                    status = self.__status()
                    self.use_notify = n
                    # Notification re-enabled
                    if status:
                        print (WEBCAM_ENABLED)
                    else:
                        print (WEBCAM_DISABLED)
                else:
                    print (WEBCAM_TOGGLING_ERROR)
        if self.option == "hotkey":
            from time import sleep
            from subprocess import Popen, PIPE
            tempfiles = ".samsung-tools-webcam-" + str(os.getuid()) + "-"
            tempfile = "/tmp/" + tempfiles + str(os.getpid())
            toggle = True
            try:
                ls = Popen(['ls /tmp/' + tempfiles + '*'],
                           stdout=PIPE, stderr=PIPE, shell=True)
                if len(ls.communicate()[0]) != 0:
                    toggle = False
            except:
                pass
            if toggle:
                Webcam("toggle", self.use_notify).apply()
                try:
                    file = open(tempfile, "w").close()  # create temp file
                except:
                    pass
                sleep(0.5)
                try:
                    os.remove(tempfile)
                except:
                    pass
        if self.option == "status":
            result = self.__status()
            if not quiet:
                if result:
                    print (WEBCAM_STATUS_ENABLED)
                else:
                    print (WEBCAM_STATUS_DISABLED)


class Wireless():

    def __init__(self, option, use_notify=False):
        self.option = option
        self.use_notify = use_notify
        success = False
        retry = 3
        while retry > 0 and not success:
            try:
                bus = dbus.SessionBus()
                proxy = bus.get_object(
                    SESSION_INTERFACE_NAME,
                    SESSION_OBJECT_PATH_WIRELESS)
                self.interface = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
                success = True
            except:
                retry = retry - 1
        if retry == 0:
            print ("Wireless control: unable to connect to session service!")
            sys.exit(1)

    def __is_available(self):
        return self.interface.IsAvailable()

    def __on(self):
        return self.interface.Enable(self.use_notify)

    def __off(self):
        return self.interface.Disable(self.use_notify)

    def __toggle(self):
        return self.interface.Toggle(self.use_notify)

    def __status(self):
        return self.interface.IsEnabled(self.use_notify)

    def apply(self):
        if self.option is None:
            return
        if not self.__is_available():
            if not quiet:
                print (WIRELESS_NOT_AVAILABLE)
            self.__status()  # needed to show notification
            return
        if self.option == "on":
            result = self.__on()
            if not quiet:
                if result:
                    print (WIRELESS_ENABLED)
                else:
                    print (WIRELESS_ENABLING_ERROR)
        if self.option == "off":
            result = self.__off()
            if not quiet:
                if result:
                    print (WIRELESS_DISABLED)
                else:
                    print (WIRELESS_DISABLING_ERROR)
        if self.option == "toggle":
            result = self.__toggle()
            if not quiet:
                if result:
                    # Temporary disable notifications
                    n = self.use_notify
                    self.use_notify = False
                    status = self.__status()
                    self.use_notify = n
                    # Notification re-enabled
                    if status:
                        print (WIRELESS_ENABLED)
                    else:
                        print (WIRELESS_DISABLED)
                else:
                    print (WIRELESS_TOGGLING_ERROR)
        if self.option == "hotkey":
            from time import sleep
            from subprocess import Popen, PIPE
            tempfiles = ".samsung-tools-wireless-" + str(os.getuid()) + "-"
            tempfile = "/tmp/" + tempfiles + str(os.getpid())
            toggle = True
            try:
                ls = Popen(['ls /tmp/' + tempfiles + '*'],
                           stdout=PIPE, stderr=PIPE, shell=True)
                if len(ls.communicate()[0]) != 0:
                    toggle = False
            except:
                pass
            if toggle:
                Wireless("toggle", self.use_notify).apply()
                try:
                    file = open(tempfile, "w").close()  # create temp file
                except:
                    pass
                sleep(0.5)
                try:
                    os.remove(tempfile)
                except:
                    pass
        if self.option == "status":
            result = self.__status()
            if not quiet:
                if result:
                    print (WIRELESS_STATUS_ENABLED)
                else:
                    print (WIRELESS_STATUS_DISABLED)


def usage(option=None, opt=None, value=None, parser=None):
    print ("Samsung Tools %s" % APP_VERSION)
    print ("Command Line Utility")
    print ("\n")
    print ("Usage: %s <interface> <option> ..." % os.path.basename(sys.argv[0]))
    print ("\n")
    print ("Backlight:")
    print ("\t" + "Interface" + ":\t-b | --backlight")
    print ("\t" + "Options" + ":\ton | off | toggle | hotkey | status")
    print ("Bluetooth:")
    print ("\t" + "Interface" + ":\t-B | --bluetooth")
    print ("\t" + "Options" + ":\ton | off | toggle | hotkey | status")
    print ("CPU fan:")
    print ("\t" + "Interface" + ":\t-c | --cpu")
    print ("\t" + "Options" + ":\tnormal | silent | overclock | cycle | hotkey | status")
    print ("Webcam:")
    print ("\t" + "Interface" + ":\t-w | --webcam")
    print ("\t" + "Options" + ":\ton | off | toggle | hotkey | status")
    print ("Wireless:")
    print ("\t" + "Interface" + ":\t-W | --wireless")
    print ("\t" + "Options" + ":\ton | off | toggle | hotkey | status")
    print ("\n")
    print ("Other options:")
    print (" -a | --status\t\t" + "Show status for all devices.")
    print (" -n | --show-notify\t" + "Show graphical notifications.")
    print (" -q | --quiet\t\t" + "Do not print messages on standard output.")
    print (" -i | --interface\t" + "Show the control interface currently in use.")
    print (" -s | --stop-session\t" + "Stop the session service.")
    print (" -S | --stop-system\t" + "Stop the system service.")
    print ("\n")
    print ("Examples of use:")
    print (" - Toggle backlight:")
    print (" %s --backlight toggle" % os.path.basename(sys.argv[0]))
    print ("\n")
    print (" - Toggle wireless and set CPU fan mode to 'silent':")
    print (" %s --wireless toggle --cpu silent" % os.path.basename(sys.argv[0]))
    print ("\n")
    print (" - Disable bluetooth, webcam and wireless:")
    print (" %s -B off -w off -W off" % os.path.basename(sys.argv[0]))
    print ("\n")
    print ("For more informations, visit the 'Linux On My Samsung' forum:")
    print ("\n")
    print (" - http://loms.voria.org")
    print ("\n")
    print ("Copyleft by: Fortunato Ventre - vorione@gmail.com")
    print ("Released under GPLv3 license" + ".")
    sys.exit(0)


def main():
    if len(sys.argv) == 1:
        print ("No action(s) specified.")
        print ("Use --help for instructions.")
        sys.exit(1)

    from optparse import OptionParser
    usage_string = ("Usage: %s <interface> <option> ..." %
                           os.path.basename(sys.argv[0]))
    parser = OptionParser(usage_string, add_help_option=False)
    parser.add_option('-h', '--help',
                      action="callback",
                      callback=usage)
    parser.add_option('-b', '--backlight',
                      dest="backlight",
                      type="choice",
                      choices=['on', 'off', 'toggle', 'hotkey', 'status'])
    parser.add_option('-B', '--bluetooth',
                      dest="bluetooth",
                      type="choice",
                      choices=['on', 'off', 'toggle', 'hotkey', 'status'])
    parser.add_option(
        '-c',
        '--cpu',
        dest="cpu",
        type="choice",
        choices=[
            'normal',
            'silent',
            'overclock',
            'cycle',
            'hotkey',
            'status'])
    parser.add_option('-w', '--webcam',
                      dest="webcam",
                      type="choice",
                      choices=['on', 'off', 'toggle', 'hotkey', 'status'])
    parser.add_option('-W', '--wireless',
                      dest="wireless",
                      type="choice",
                      choices=['on', 'off', 'toggle', 'hotkey', 'status'])
    parser.add_option('-n', '--show-notify',
                      action="store_true",
                      dest="show_notify",
                      default=False)
    parser.add_option('-q', '--quiet',
                      action="store_true",
                      dest="quiet",
                      default=False)
    parser.add_option('-i', '--interface',
                      action="store_true",
                      dest="interface",
                      default=False)
    parser.add_option('-s', '--stop-session',
                      action="store_true",
                      dest="stopsession",
                      default=False)
    parser.add_option('-S', '--stop-system',
                      action="store_true",
                      dest="stopsystem",
                      default=False)
    parser.add_option('-a', '--status',
                      action="store_true",
                      dest="status",
                      default=False)

    (options, args) = parser.parse_args()

    global quiet
    quiet = options.quiet

    if options.status:
        options.backlight = "status"
        options.bluetooth = "status"
        options.cpu = "status"
        options.webcam = "status"
        options.wireless = "status"

    if os.getuid() == 0:
        print ("This program is intended to be used only by non-privileged users.")
        sys.exit(1)

    if len(args) != 0:
        print ("Wrong argument(s).")
        print ("Use --help for instructions.")
        sys.exit(1)

    # Check if the dbus daemon is running. If not, start it.
    if "DBUS_SESSION_BUS_ADDRESS" not in os.environ:
        try:
            from subprocess import Popen, PIPE, STDOUT
            p = Popen(
                'dbus-launch --exit-with-session',
                shell=True,
                stdout=PIPE,
                stderr=STDOUT)
            for var in p.stdout:
                sp = var.split('=', 1)
                os.environ[sp[0]] = sp[1][:-1]
        except:
            print ("Unable to start a DBus daemon!")
            sys.exit(1)

    Backlight(options.backlight).apply()
    Bluetooth(options.bluetooth, options.show_notify).apply()
    Cpu(options.cpu, options.show_notify).apply()
    Webcam(options.webcam, options.show_notify).apply()
    Wireless(options.wireless, options.show_notify).apply()

    if options.interface and not quiet:
        try:
            bus = dbus.SystemBus()
            proxy = bus.get_object(
                SYSTEM_INTERFACE_NAME,
                SYSTEM_OBJECT_PATH_OPTIONS)
            opts = dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
            ci = opts.GetControlInterface()
            print ("Control interface:")
            if ci == "esdm":
                print ("easy-slow-down-manager")
            elif ci == "sl":
                print ("samsung-laptop")
            else:
                print ("-")
        except:
            print ("Control interface: unable to connect to system service!")
            pass

    if options.stopsession:
        try:
            bus = dbus.SessionBus()
            proxy = bus.get_object(
                SESSION_INTERFACE_NAME,
                SESSION_OBJECT_PATH_GENERAL)
            general = dbus.Interface(proxy, SESSION_INTERFACE_NAME)
            general.Exit()
            if not quiet:
                print ("Session service stopped")
        except:
            if not quiet:
                print ("Cannot stop session service")
            pass

    if options.stopsystem:
        try:
            bus = dbus.SystemBus()
            proxy = bus.get_object(
                SYSTEM_INTERFACE_NAME,
                SYSTEM_OBJECT_PATH_GENERAL)
            general = dbus.Interface(proxy, SYSTEM_INTERFACE_NAME)
            general.Exit()
            if not quiet:
                print ("System service stopped")
        except:
            if not quiet:
                print ("Cannot stop system service")
            pass

if __name__ == "__main__":
    main()
