#! /usr/bin/env python


import sys
from gi.repository import Gtk


class ProxyMan:
    """
    Class to display the main screen correctly and make it behave correctly.
    """
    def __init__( self ):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui.glade")
        self.builder.get_object("grid2").set_sensitive(False)
        self.builder.get_object("grid3").set_sensitive(False)
        self.popup = Gtk.Builder()
        self.popup.add_from_file("popup.glade")
        
        dic = { 
            "on_quit_window" : self.quit,
            "click_cancel" : self.quit,
            "click_apply" : self.applyToSystem,
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
        
    def applyToSystem(self, widget):
        if self.builder.get_object('radiobutton1').get_active() == True:
            applyProxy = ApplyProxy(False)
        else:
            proxy_address = self.builder.get_object('proxy_textbox1').get_text()
            proxy_port = self.builder.get_object('port_textbox1').get_text()
            username = self.builder.get_object('uname_textbox1').get_text()
            password = self.builder.get_object('pword_textbox1').get_text()
            credentials = Credentials(proxy_address, proxy_port,
                                      username, password)
            applyProxy = ApplyProxy(True, credentials)
        
    
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