#! /usr/bin/env python

# Case: When 'use auth' is not same for all three checkboxes, and you select 'use same proxy'

import sys
from gi.repository import Gtk  


class ProxyMan:
    def go(self, object_string):
        return self.builder.get_object(object_string)

    def __init__( self ):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui.glade")
        self.go("grid2").set_sensitive(False)
        self.go("grid3").set_sensitive(False)
#        print self.go("checkbutton1").get_active()
        
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
        self.go("grid1").set_sensitive(False)
        self.go("grid2").set_sensitive(False)
        self.go("grid3").set_sensitive(False)
        self.go("checkbutton4").set_sensitive(False)

    def useProxy(self, widget):
        self.go("grid1").set_sensitive(True)
        self.go("checkbutton4").set_sensitive(True)
        if self.go("checkbutton4").get_active() == False:
            self.go("grid2").set_sensitive(True)
            self.go("grid3").set_sensitive(True)
        
    def useSameProxy(self, widget):
        if self.go("checkbutton4").get_active() == True:
            self.go("grid2").set_sensitive(False)
            self.go("grid3").set_sensitive(False)
            if self.go("checkbutton1").get_active() == True:
                self.go("checkbutton2").set_active(True)
                self.go("checkbutton3").set_active(True)
            else:
                self.go("checkbutton2").set_active(False)
                self.go("checkbutton3").set_active(False)
        else:
            self.go("grid2").set_sensitive(True)
            self.go("grid3").set_sensitive(True)
        
        self.go("uname_textbox2").set_text(self.go("uname_textbox1").get_text())
        self.go("uname_textbox3").set_text(self.go("uname_textbox1").get_text())
        self.go("pword_textbox2").set_text(self.go("pword_textbox1").get_text())
        self.go("pword_textbox3").set_text(self.go("pword_textbox1").get_text())
        self.go("proxy_textbox2").set_text(self.go("proxy_textbox1").get_text())
        self.go("proxy_textbox3").set_text(self.go("proxy_textbox1").get_text())
        self.go("port_textbox2").set_text(self.go("port_textbox1").get_text())
        self.go("port_textbox3").set_text(self.go("port_textbox1").get_text())
        
        if self.go("checkbutton1").get_active() == True and self.go("checkbutton4").get_active() == True:
            self.go("checkbutton2").set_active(True)
            self.go("checkbutton3").set_active(True)
        self.toggleAuth2(widget)
        self.toggleAuth3(widget)
        
    def toggleAuth1(self, widget):
        if self.go("checkbutton1").get_active() == False:
            self.go("uname_label1").set_sensitive(False)
            self.go("pword_label1").set_sensitive(False)
            self.go("uname_textbox1").set_sensitive(False)
            self.go("pword_textbox1").set_sensitive(False)
        else:
            self.go("uname_label1").set_sensitive(True)
            self.go("pword_label1").set_sensitive(True)
            self.go("uname_textbox1").set_sensitive(True)
            self.go("pword_textbox1").set_sensitive(True)
        if self.go("checkbutton1").get_active() == True and self.go("checkbutton4").get_active() == True:
            self.go("checkbutton2").set_active(True)
            self.go("checkbutton3").set_active(True)
        else:
            if self.go("checkbutton1").get_active() == False and self.go("checkbutton4").get_active() == True:
                self.go("checkbutton2").set_active(False)
                self.go("checkbutton3").set_active(False)
    
    def toggleAuth2(self, widget):
        if self.go("checkbutton2").get_active() == False:
            self.go("uname_label2").set_sensitive(False)
            self.go("pword_label2").set_sensitive(False)
            self.go("uname_textbox2").set_sensitive(False)
            self.go("pword_textbox2").set_sensitive(False)
        elif self.go("checkbutton4").get_active() == False:
            self.go("uname_label2").set_sensitive(True)
            self.go("pword_label2").set_sensitive(True)
            self.go("uname_textbox2").set_sensitive(True)
            self.go("pword_textbox2").set_sensitive(True)
    
    def toggleAuth3(self, widget):
        if self.go("checkbutton3").get_active() == False:
            self.go("uname_label3").set_sensitive(False)
            self.go("pword_label3").set_sensitive(False)
            self.go("uname_textbox3").set_sensitive(False)
            self.go("pword_textbox3").set_sensitive(False)
        elif self.go("checkbutton4").get_active() == False:
            self.go("uname_label3").set_sensitive(True)
            self.go("pword_label3").set_sensitive(True)
            self.go("uname_textbox3").set_sensitive(True)
            self.go("pword_textbox3").set_sensitive(True)
    
    def proxyTextboxChanged(self, widget):
        if self.go("checkbutton4").get_active() == True:
            self.go("proxy_textbox2").set_text(self.go("proxy_textbox1").get_text())
            self.go("proxy_textbox3").set_text(self.go("proxy_textbox1").get_text())
    
    def portTextboxChanged(self, widget):
        if self.go("checkbutton4").get_active() == True:
            self.go("port_textbox2").set_text(self.go("port_textbox1").get_text())
            self.go("port_textbox3").set_text(self.go("port_textbox1").get_text())
    
    def unameTextboxChanged(self, widget):
        if self.go("checkbutton4").get_active() == True:
            self.go("uname_textbox2").set_text(self.go("uname_textbox1").get_text())
            self.go("uname_textbox3").set_text(self.go("uname_textbox1").get_text())
    
    def pwordTextboxChanged(self, widget):
        if self.go("checkbutton4").get_active() == True:
            self.go("pword_textbox2").set_text(self.go("pword_textbox1").get_text())
            self.go("pword_textbox3").set_text(self.go("pword_textbox1").get_text())
    
    def quit(self, widget):
        sys.exit(0)
        
proxyMan = ProxyMan()
window = proxyMan.go("window1")
window.show_all()

Gtk.main()

