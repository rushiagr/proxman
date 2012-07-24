#! /usr/bin/env python

# Bugs: Either enter all the details of all the three types of proxies: http, ftp
#       and ftp, or else none. No flexibility implemented so far.

#       * what if any of the below files do not exist at all, and we need to create them?!

import os
import sys
from gi.repository import Gtk  

"""
Class to display the main screen correctly and making it behave correctly.
"""
class ProxyMan:

    def __init__( self ):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui.glade")
        self.builder.get_object("grid2").set_sensitive(False)
        self.builder.get_object("grid3").set_sensitive(False)
#        print self.builder.get_object("checkbutton1").get_active()
        self.no_root = Gtk.Builder()
        self.no_root.add_from_file("no_root.glade")
        
        dic = { 
            "on_quit_window" : self.quit,
            "click_cancel" : self.quit,
            "click_apply" : self.quit,
            "click_ok" : self.quit,
            "radio_click_no_proxy" : self.noProxy,
            "radio_click_use_proxy" : self.useProxy,
            "toggle_use_same_proxy" : self.useSameProxy,
            "toggle_auth1" : self.toggleAuth1,
            "toggle_auth2" : self.toggleAuth2,
            "toggle_auth3" : self.toggleAuth3,
            "proxy_textbox1_changed" : self.proxyTextboxChanged,
            "port_textbox1_changed" : self.portTextboxChanged,
            "uname_textbox1_changed" : self.unameTextboxChanged,
            "pword_textbox1_changed" : self.pwordTextboxChanged,
        }
        
        self.builder.connect_signals( dic )
        
    
    def noProxy(self, widget):
        self.builder.get_object("grid1").set_sensitive(False)
        self.builder.get_object("grid2").set_sensitive(False)
        self.builder.get_object("grid3").set_sensitive(False)
        self.builder.get_object("checkbutton4").set_sensitive(False)

    def useProxy(self, widget):
        self.builder.get_object("grid1").set_sensitive(True)
        self.builder.get_object("checkbutton4").set_sensitive(True)
        if self.builder.get_object("checkbutton4").get_active() == False:
            self.builder.get_object("grid2").set_sensitive(True)
            self.builder.get_object("grid3").set_sensitive(True)
        
    def useSameProxy(self, widget):
        if self.builder.get_object("checkbutton4").get_active() == True:
            self.builder.get_object("grid2").set_sensitive(False)
            self.builder.get_object("grid3").set_sensitive(False)
            if self.builder.get_object("checkbutton1").get_active() == True:
                self.builder.get_object("checkbutton2").set_active(True)
                self.builder.get_object("checkbutton3").set_active(True)
            else:
                self.builder.get_object("checkbutton2").set_active(False)
                self.builder.get_object("checkbutton3").set_active(False)
        else:
            self.builder.get_object("grid2").set_sensitive(True)
            self.builder.get_object("grid3").set_sensitive(True)
        
        self.builder.get_object("uname_textbox2").set_text(self.builder.get_object("uname_textbox1").get_text())
        self.builder.get_object("uname_textbox3").set_text(self.builder.get_object("uname_textbox1").get_text())
        self.builder.get_object("pword_textbox2").set_text(self.builder.get_object("pword_textbox1").get_text())
        self.builder.get_object("pword_textbox3").set_text(self.builder.get_object("pword_textbox1").get_text())
        self.builder.get_object("proxy_textbox2").set_text(self.builder.get_object("proxy_textbox1").get_text())
        self.builder.get_object("proxy_textbox3").set_text(self.builder.get_object("proxy_textbox1").get_text())
        self.builder.get_object("port_textbox2").set_text(self.builder.get_object("port_textbox1").get_text())
        self.builder.get_object("port_textbox3").set_text(self.builder.get_object("port_textbox1").get_text())
        
        if self.builder.get_object("checkbutton1").get_active() == True and self.builder.get_object("checkbutton4").get_active() == True:
            self.builder.get_object("checkbutton2").set_active(True)
            self.builder.get_object("checkbutton3").set_active(True)
        self.toggleAuth2(widget)
        self.toggleAuth3(widget)
        
    def toggleAuth1(self, widget):
        if self.builder.get_object("checkbutton1").get_active() == False:
            self.builder.get_object("uname_label1").set_sensitive(False)
            self.builder.get_object("pword_label1").set_sensitive(False)
            self.builder.get_object("uname_textbox1").set_sensitive(False)
            self.builder.get_object("pword_textbox1").set_sensitive(False)
        else:
            self.builder.get_object("uname_label1").set_sensitive(True)
            self.builder.get_object("pword_label1").set_sensitive(True)
            self.builder.get_object("uname_textbox1").set_sensitive(True)
            self.builder.get_object("pword_textbox1").set_sensitive(True)
        if self.builder.get_object("checkbutton1").get_active() == True and self.builder.get_object("checkbutton4").get_active() == True:
            self.builder.get_object("checkbutton2").set_active(True)
            self.builder.get_object("checkbutton3").set_active(True)
        else:
            if self.builder.get_object("checkbutton1").get_active() == False and self.builder.get_object("checkbutton4").get_active() == True:
                self.builder.get_object("checkbutton2").set_active(False)
                self.builder.get_object("checkbutton3").set_active(False)
    
    def toggleAuth2(self, widget):
        if self.builder.get_object("checkbutton2").get_active() == False:
            self.builder.get_object("uname_label2").set_sensitive(False)
            self.builder.get_object("pword_label2").set_sensitive(False)
            self.builder.get_object("uname_textbox2").set_sensitive(False)
            self.builder.get_object("pword_textbox2").set_sensitive(False)
        elif self.builder.get_object("checkbutton4").get_active() == False:
            self.builder.get_object("uname_label2").set_sensitive(True)
            self.builder.get_object("pword_label2").set_sensitive(True)
            self.builder.get_object("uname_textbox2").set_sensitive(True)
            self.builder.get_object("pword_textbox2").set_sensitive(True)
    
    def toggleAuth3(self, widget):
        if self.builder.get_object("checkbutton3").get_active() == False:
            self.builder.get_object("uname_label3").set_sensitive(False)
            self.builder.get_object("pword_label3").set_sensitive(False)
            self.builder.get_object("uname_textbox3").set_sensitive(False)
            self.builder.get_object("pword_textbox3").set_sensitive(False)
        elif self.builder.get_object("checkbutton4").get_active() == False:
            self.builder.get_object("uname_label3").set_sensitive(True)
            self.builder.get_object("pword_label3").set_sensitive(True)
            self.builder.get_object("uname_textbox3").set_sensitive(True)
            self.builder.get_object("pword_textbox3").set_sensitive(True)
    
    def proxyTextboxChanged(self, widget):
        if self.builder.get_object("checkbutton4").get_active() == True:
            self.builder.get_object("proxy_textbox2").set_text(self.builder.get_object("proxy_textbox1").get_text())
            self.builder.get_object("proxy_textbox3").set_text(self.builder.get_object("proxy_textbox1").get_text())
    
    def portTextboxChanged(self, widget):
        if self.builder.get_object("checkbutton4").get_active() == True:
            self.builder.get_object("port_textbox2").set_text(self.builder.get_object("port_textbox1").get_text())
            self.builder.get_object("port_textbox3").set_text(self.builder.get_object("port_textbox1").get_text())
    
    def unameTextboxChanged(self, widget):
        if self.builder.get_object("checkbutton4").get_active() == True:
            self.builder.get_object("uname_textbox2").set_text(self.builder.get_object("uname_textbox1").get_text())
            self.builder.get_object("uname_textbox3").set_text(self.builder.get_object("uname_textbox1").get_text())
    
    def pwordTextboxChanged(self, widget):
        if self.builder.get_object("checkbutton4").get_active() == True:
            self.builder.get_object("pword_textbox2").set_text(self.builder.get_object("pword_textbox1").get_text())
            self.builder.get_object("pword_textbox3").set_text(self.builder.get_object("pword_textbox1").get_text())
    
    def quit(self, widget):
        sys.exit(0)


"""
Class to handle the behaviour when the program is not run as a root
"""
class NoRoot:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("no_root.glade")
        
        dic = { 
            "on_ok_button_click" : self.quit,
        }
        
        self.builder.connect_signals( dic )
        
    def quit(self, widget):
        sys.exit(0)
        
class ApplyProxy:
    def __init__(self, is_proxy=False, 
                 proxy_address='', proxy_port='', 
                 username='',password=''
                 ):
                 
        # Fetching configuration information from all required text files
        bashrc_file = open('/etc/bash.bashrc','r')
        bashrc_contents = bashrc_file.readlines()
        bashrc_file.close()
        bashrc_file = open('/etc/bash.bashrc', 'w')
        for i in bashrc_contents:
            if i.lower().startswith('export http_proxy') or i.lower().startswith('export https_proxy') or i.lower().startswith('export ftp_proxy'):
                i = ''
        bashrc_file.write(''.join(bashrc_contents))
        bashrc_file.close()

        env_file = open('/etc/environment','r')
        env_contents = env_file.readlines()
        env_file.close()
        env_file = open('/etc/environment','w')
        for i in env_contents:
            if i.lower().startswith('http_proxy') or i.lower().startswith('https_proxy') or i.lower().startswith('ftp_proxy'):
                i = ''
        env_file.write(''.join(env_contents))
        env_file.close()
        
        aptconf_file = open('/etc/apt/apt.conf', 'w')
        aptconf_file.write('')
        aptconf_file.close()
        
        
        if not is_proxy:
            
            # Update /root/.synaptic/synaptic.conf file
            sconf_file = open('/root/.synaptic/synaptic.conf', 'w')
            sconf_contents = sconf_file.readlines()
            for i in sconf_contents:
                if i.startswith('  UseProxy'):
                    i = i.split('"')
                    i[1] = '0'
                    i = '"'.join(i)
                break
            sconf_file.writelines(sconf_contents)
            sconf_file.close()
            
        else:
            
            # Validation
            proxy_address_split = proxy_address.split('.')
            if len(proxy_address_split) != 4:
                sys.exit()
            no_alpha_character = False
            for i in proxy_address_split:
                if not i.isdigit():
                    no_alpha_character = True
                    break
            if no_alpha_character == True:
                sys.exit()
            
            if not proxy_port.isdigit() or len(proxy_port) > 5:
                sys.exit()
                
            if (username=='' and len(password) > 0) or ( len(username) > 0 and password==''):
                sys.exit()
            
            authentication = True
            if username=='' and password=='':
                authentication = False
                
            # Update /etc/environment file
            env_file = open('/etc/environment', 'w')
            if authentication:
                env_contents.append('http_proxy=http://' + username + ':' + password + '@' + proxy_address + ':' + proxy_port + '/\n')
                env_contents.append('https_proxy=https://' + username + ':' + password + '@' + proxy_address + ':' + proxy_port + '/\n')
                env_contents.append('ftp_proxy=ftp://' + username + ':' + password + '@' + proxy_address + ':' + proxy_port + '/\n')
            else:
                env_contents.append('export http_proxy=http://' + proxy_address + ':' + proxy_port + '/\n')
                env_contents.append('export https_proxy=https://' + proxy_address + ':' + proxy_port + '/\n')
                env_contents.append('export ftp_proxy=ftp://' + proxy_address + ':' + proxy_port + '/\n')

            env_file.write(''.join(env_contents))
            env_file.close()
            
            # Update /etc/bash.bashrc file
            bashrc_file = open('/etc/bash.bashrc', 'w')
            if authentication:
                bashrc_contents.append('export http_proxy=http://' + username + ':' + password + '@' + proxy_address + ':' + proxy_port + '/\n')
                bashrc_contents.append('export https_proxy=https://' + username + ':' + password + '@' + proxy_address + ':' + proxy_port + '/\n')
                bashrc_contents.append('export ftp_proxy=ftp://' + username + ':' + password + '@' + proxy_address + ':' + proxy_port + '/\n')
            else:
                bashrc_contents.append('export http_proxy=http://' + proxy_address + ':' + proxy_port + '/\n')
                bashrc_contents.append('export https_proxy=https://' + proxy_address + ':' + proxy_port + '/\n')
                bashrc_contents.append('export ftp_proxy=ftp://' + proxy_address + ':' + proxy_port + '/\n')

            bashrc_file.write(''.join(bashrc_contents))
            bashrc_file.close()
            
            # Update /etc/apt/apt.conf file
            aptconf_file = open('/etc/apt/apt.conf', 'w')
            if authentication:
                aptconf_file.write('Acquire::http::Proxy "http://' +  username + ':' + password + '@' + proxy_address + ':' + proxy_port + '/";\n')
                aptconf_file.write('Acquire::https::Proxy "https://' +  username + ':' + password + '@' + proxy_address + ':' + proxy_port + '/";\n')
                aptconf_file.write('Acquire::ftp::Proxy "ftp://' +  username + ':' + password + '@' + proxy_address + ':' + proxy_port + '/";\n')
                aptconf_file.write('\n')
            else:
                aptconf_file.write('Acquire::http::Proxy "http://' + proxy_address + ':' + proxy_port + '/";\n')
                aptconf_file.write('Acquire::https::Proxy "https://' + proxy_address + ':' + proxy_port + '/";\n')
                aptconf_file.write('Acquire::ftp::Proxy "ftp://' + proxy_address + ':' + proxy_port + '/";\n')
                aptconf_file.write('\n')
            
            aptconf_file.close()
            
            # Update /root/.synaptic/synaptic.conf file
            sconf_file = open('/root/.synaptic/synaptic.conf', 'w')
            sconf_contents = sconf_file.readlines()
            for i in sconf_contents:
                if i.startswith('  httpProxyUser'):
                    if authentication:
                        i = i.split('"')
                        i[1] = username
                        i = '"'.join(i)
                    else:
                        i = i.split('"')
                        i[1] = ''
                        i = '"'.join(i)
                if i.startswith('  httpProxyPass'):
                    if authentication:
                        i = i.split('"')
                        i[1] = password
                        i = '"'.join(i)
                    else:
                        i = i.split('"')
                        i[1] = ''
                        i = '"'.join(i)
                if i.startswith('  httpProxy'):
                    i = i.split('"')
                    i[1] = proxy_address
                    i = '"'.join(i)
                if i.startswith('  httpProxyPort'):
                    i = i.split('"')
                    i[1] = proxy_port
                    i = '"'.join(i)
                if i.startswith('  ftpProxy'):
                    i = i.split('"')
                    i[1] = proxy_address
                    i = '"'.join(i)
                if i.startswith('  ftpProxyPort'):
                    i = i.split('"')
                    i[1] = proxy_port
                    i = '"'.join(i)
            sconf_file.writelines(sconf_contents)
            
                    
proxyMan = ProxyMan()
window = proxyMan.builder.get_object("window1")
window.show_all()
if os.geteuid() != 0:
    noRoot = NoRoot()
    noroot = noRoot.builder.get_object("window1")
    noroot.show_all()
    
Gtk.main()

