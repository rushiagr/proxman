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
        self.obj("https_grid").set_sensitive(False)
        self.obj("ftp_grid").set_sensitive(False)
        self.popup = Gtk.Builder()
        self.popup.add_from_file("popup.glade")
        
        dic = { 
            "onclick_quit_window" : self.quit,
            "onclick_cancel_button" : self.quit,
            "onclick_apply_button" : self.applyToSystem,
            "onclick_not_use_proxy_radio" : self.noProxy,
            "onclick_use_proxy_radio" : self.useProxy,
            "toggle_use_same_proxy_checkbox" : self.useSameProxy,
            "toggle_http_auth" : self.toggleAuth1,
            "toggle_https_auth" : self.toggleAuth2,
            "toggle_ftp_auth" : self.toggleAuth3,
            "onchange_http_proxy_textbox" : self.proxyTextboxChanged,
            "onchange_http_port_textbox" : self.portTextboxChanged,
            "onchange_http_user_textbox" : self.unameTextboxChanged,
            "onchange_http_password_textbox" : self.pwordTextboxChanged,
        }
        
        self.builder.connect_signals( dic ) 
        
    def obj(self, object_name):
        """
        Returns the object for the given :object_name:
        Just to save some keyboard strokes.
        """
        return self.builder.get_object(object_name)

    def applyToSystem(self, widget):
        if self.obj('not_use_proxy_radio').get_active() == True:
            applyProxy = ApplyProxy(False)
        else:
            proxy_address = self.obj('http_proxy_textbox').get_text()
            proxy_port = self.obj('http_port_textbox').get_text()
            username = self.obj('http_user_textbox').get_text()
            password = self.obj('http_password_textbox').get_text()
            credentials = Credentials(proxy_address, proxy_port,
                                      username, password)
            applyProxy = ApplyProxy(True, credentials)
        
    
    def noProxy(self, widget):
        self.obj("http_grid").set_sensitive(False)
        self.obj("https_grid").set_sensitive(False)
        self.obj("ftp_grid").set_sensitive(False)
        self.obj("use_same_proxy_checkbox").set_sensitive(False)

    def useProxy(self, widget):
        self.obj("http_grid").set_sensitive(True)
        self.obj("use_same_proxy_checkbox").set_sensitive(True)
        if self.obj("use_same_proxy_checkbox").get_active() == False:
            self.obj("https_grid").set_sensitive(True)
            self.obj("ftp_grid").set_sensitive(True)
        
    def useSameProxy(self, widget):
        if self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_grid").set_sensitive(False)
            self.obj("ftp_grid").set_sensitive(False)
            if self.obj("http_use_auth_checkbox").get_active() == True:
                self.obj("https_use_auth_checkbox").set_active(True)
                self.obj("ftp_use_auth_checkbox").set_active(True)
            else:
                self.obj("https_use_auth_checkbox").set_active(False)
                self.obj("ftp_use_auth_checkbox").set_active(False)
        else:
            self.obj("https_grid").set_sensitive(True)
            self.obj("ftp_grid").set_sensitive(True)
        
        self.obj("https_proxy_textbox").set_text(
            self.obj("http_proxy_textbox").get_text())
        self.obj("https_port_textbox").set_text(
            self.obj("http_port_textbox").get_text())
        self.obj("https_user_textbox").set_text(
            self.obj("http_user_textbox").get_text())
        self.obj("https_password_textbox").set_text(
            self.obj("http_password_textbox").get_text())

        self.obj("ftp_proxy_textbox").set_text(
            self.obj("http_proxy_textbox").get_text())
        self.obj("ftp_port_textbox").set_text(
            self.obj("http_port_textbox").get_text())
        self.obj("ftp_user_textbox").set_text(
            self.obj("http_user_textbox").get_text())
        self.obj("ftp_password_textbox").set_text(
            self.obj("http_password_textbox").get_text())
        
        if self.obj("http_use_auth_checkbox").get_active() is True and self.obj("use_same_proxy_checkbox").get_active() is True:
            self.obj("https_use_auth_checkbox").set_active(True)
            self.obj("ftp_use_auth_checkbox").set_active(True)

        self.toggleAuth2(widget)
        self.toggleAuth3(widget)
        
    def toggleAuth1(self, widget):
        if self.obj("http_use_auth_checkbox").get_active() is False:
            self.obj("http_user_label").set_sensitive(False)
            self.obj("http_password_label").set_sensitive(False)
            self.obj("http_user_textbox").set_sensitive(False)
            self.obj("http_password_textbox").set_sensitive(False)
        else:
            self.obj("http_user_label").set_sensitive(True)
            self.obj("http_password_label").set_sensitive(True)
            self.obj("http_user_textbox").set_sensitive(True)
            self.obj("http_password_textbox").set_sensitive(True)
        if self.obj("http_use_auth_checkbox").get_active() == True and self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_use_auth_checkbox").set_active(True)
            self.obj("ftp_use_auth_checkbox").set_active(True)
        else:
            if self.obj("http_use_auth_checkbox").get_active() == False and self.obj("use_same_proxy_checkbox").get_active() == True:
                self.obj("https_use_auth_checkbox").set_active(False)
                self.obj("ftp_use_auth_checkbox").set_active(False)
    
    def toggleAuth2(self, widget):
        if self.obj("https_use_auth_checkbox").get_active() == False:
            self.obj("https_user_label").set_sensitive(False)
            self.obj("https_password_label").set_sensitive(False)
            self.obj("https_user_textbox").set_sensitive(False)
            self.obj("https_password_textbox").set_sensitive(False)
        elif self.obj("use_same_proxy_checkbox").get_active() == False:
            self.obj("https_user_label").set_sensitive(True)
            self.obj("https_password_label").set_sensitive(True)
            self.obj("https_user_textbox").set_sensitive(True)
            self.obj("https_password_textbox").set_sensitive(True)
    
    def toggleAuth3(self, widget):
        if self.obj("ftp_use_auth_checkbox").get_active() == False:
            self.obj("ftp_user_label").set_sensitive(False)
            self.obj("ftp_password_label").set_sensitive(False)
            self.obj("ftp_user_textbox").set_sensitive(False)
            self.obj("ftp_password_textbox").set_sensitive(False)
        elif self.obj("use_same_proxy_checkbox").get_active() == False:
            self.obj("ftp_user_label").set_sensitive(True)
            self.obj("ftp_password_label").set_sensitive(True)
            self.obj("ftp_user_textbox").set_sensitive(True)
            self.obj("ftp_password_textbox").set_sensitive(True)
    
    def proxyTextboxChanged(self, widget):
        if self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_proxy_textbox").set_text(self.obj("http_proxy_textbox").get_text())
            self.obj("ftp_proxy_textbox").set_text(self.obj("http_proxy_textbox").get_text())
    
    def portTextboxChanged(self, widget):
        if self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_port_textbox").set_text(self.obj("http_port_textbox").get_text())
            self.obj("ftp_port_textbox").set_text(self.obj("http_port_textbox").get_text())
    
    def unameTextboxChanged(self, widget):
        if self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_user_textbox").set_text(self.obj("http_user_textbox").get_text())
            self.obj("ftp_user_textbox").set_text(self.obj("http_user_textbox").get_text())
    
    def pwordTextboxChanged(self, widget):
        if self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_password_textbox").set_text(self.obj("http_password_textbox").get_text())
            self.obj("ftp_password_textbox").set_text(self.obj("http_password_textbox").get_text())
    
    def quit(self, widget):
        sys.exit(0)
