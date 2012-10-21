#! /usr/bin/env python

import os
import sys
from gi.repository import Gtk  
import commands


PROXY_ADDRESS_INCORRECT = 0
PROXY_PORT_INCORRECT = 1
PROXY_CREDENTIALS_INCORRECT = 2

UNSET_EXISTING_VARIABLES = 3
DO_NOTHING = 4


class Credentials:
    """ Class to hold the proxy credentials """
    
    def __init__(self, proxy_address, proxy_port,
                       username='', password=''):
        self.proxy_address = proxy_address
        self.proxy_port = proxy_port
        self.username = username
        self.password = password
    
    def is_auth(self):
        """ Checks whether authorization exist. Assumes credentials are valid """
        if self.username != '' and self.password != '':
            return True
        else:
            return False
    
    def validate(self):
        """ 
        Checks if the credentials are in proper format. 
        Returns (possibly empty) list of error numbers.
        """
        
        error_codes = []
        
        # Improper format for proxy address
        split_address = self.proxy_address.split('.')
        
        is_address_correct = True
        
        if len(split_address) != 4:
            is_address_correct = False
        if is_address_correct:
            for i in split_address:
                if not i.isdigit():
                    is_address_correct = False
                    break
                if int(i) > 255 or int(i) < 0:
                    is_address_correct = False
                    break
        
        if is_address_correct == False:
            error_codes.append(PROXY_ADDRESS_INCORRECT)
            
        # Improper format for proxy port
        if not self.proxy_port.isdigit():
            error_codes.append(PROXY_PORT_INCORRECT)
        elif int(self.proxy_port) > 65535 or int(self.proxy_port) < 0:
            error_codes.append(PROXY_PORT_INCORRECT)
            
        # Only one of proxy username or password is null
        if (self.username=='' and len(self.password) > 0) or \
                    ( len(self.username) > 0 and self.password==''):
            error_codes.append(PROXY_CREDENTIALS_INCORRECT)
            
        return error_codes


class PopUp:
    """
    Class to manage a popup message window. Default action on clicking the OK 
    button is 'do nothing and close the popup window'
    """
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('popup.glade')
        dic = { 'on_ok_button_click' : self.on_click_ok, }
        self.builder.connect_signals(dic)
        
    def on_click_ok(self, widget):
        self.builder.get_object('main_window').destroy()
        
    def popup_text(self, new_string):
        self.builder.get_object('default_label').set_text(new_string)


class DestructionPopUp(PopUp):
    """ Popup window created from this class destroys the whole program when 
        one clicks on 'OK' button """
    def on_click_ok(self, widget):
        sys.exit()


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
            "onclick_quit_window": self.quit,
            "onclick_cancel_button": self.quit,
            "onclick_apply_button": self.onclick_apply_button,
            "onclick_not_use_proxy_radio": self.onclick_not_use_proxy_radio,
            "onclick_use_proxy_radio": self.onclick_use_proxy_radio,
            "toggle_use_same_proxy_checkbox":
                self.toggle_use_same_proxy_checkbox,
                
            "toggle_http_auth": self.toggle_http_auth,
            "toggle_https_auth": self.toggle_https_auth,
            "toggle_ftp_auth": self.toggle_ftp_auth,

            "onchange_http_proxy_textbox": self.onchange_http_proxy_textbox,
            "onchange_http_port_textbox": self.onchange_http_port_textbox,
            "onchange_http_user_textbox": self.onchange_http_user_textbox,
            "onchange_http_password_textbox":
                self.onchange_http_password_textbox,
        }
        
        self.builder.connect_signals( dic ) 
        
    def obj(self, object_name):
        """
        Returns the object for the given :object_name:
        Just to save some keyboard strokes.
        (Function does nothing but calls self.builder.get_object(object_name))
        """
        return self.builder.get_object(object_name)
    
    def minibox_sensitivity(self, sensitivity, minibox_type):
        """
        A minibox contain username and password labels and textboxes.
        This function changes the sensitivity of :minibox_type: minibox to
        the value of boolean :sensitivity:
        
        params
        :sensitivity:
            boolean variable to specify the minibox should be sensitive or not
        :minibox_type:
            a string, either 'http', 'https' or 'ftp'
        """
        for elem in ['_user_label', '_user_textbox',
                     '_password_label', '_password_textbox']:
            self.obj(minibox_type + elem).set_sensitive(sensitivity)
            

    def onclick_apply_button(self, widget):
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
        
    
    def onclick_not_use_proxy_radio(self, widget):
        for proxy_type in ['http', 'https', 'ftp']:
            self.obj(proxy_type + '_grid').set_sensitive(False)
        self.obj("use_same_proxy_checkbox").set_sensitive(False)

    def onclick_use_proxy_radio(self, widget):
        self.obj("http_grid").set_sensitive(True)
        self.obj("use_same_proxy_checkbox").set_sensitive(True)
        if self.obj("use_same_proxy_checkbox").get_active() == False:
            self.obj("https_grid").set_sensitive(True)
            self.obj("ftp_grid").set_sensitive(True)
        
    def toggle_use_same_proxy_checkbox(self, widget):
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
        
        for typ in ['https', 'ftp']:
            for elem in ['proxy', 'port', 'user', 'password']:
                self.obj(typ +'_' + elem + '_textbox').set_text(
                    self.obj('http_' + elem + "_textbox").get_text())

        
        if self.obj("http_use_auth_checkbox").get_active() is True and \
                self.obj("use_same_proxy_checkbox").get_active() is True:
            self.obj("https_use_auth_checkbox").set_active(True)
            self.obj("ftp_use_auth_checkbox").set_active(True)

        self.toggle_https_auth(widget)
        self.toggle_ftp_auth(widget)
        
    def toggle_http_auth(self, widget):
        if self.obj("http_use_auth_checkbox").get_active() is False:
            self.minibox_sensitivity(False, 'http')
        else:
            self.minibox_sensitivity(True, 'http')
        if self.obj("http_use_auth_checkbox").get_active() == True and \
                self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_use_auth_checkbox").set_active(True)
            self.obj("ftp_use_auth_checkbox").set_active(True)
        else:
            if self.obj("http_use_auth_checkbox").get_active() == False and \
                    self.obj("use_same_proxy_checkbox").get_active() == True:
                self.obj("https_use_auth_checkbox").set_active(False)
                self.obj("ftp_use_auth_checkbox").set_active(False)
    
    def toggle_https_auth(self, widget):
        if self.obj("https_use_auth_checkbox").get_active() == False:
            self.minibox_sensitivity(False, 'https')
        elif self.obj("use_same_proxy_checkbox").get_active() == False:
            self.minibox_sensitivity(True, 'https')
    
    def toggle_ftp_auth(self, widget):
        if self.obj("ftp_use_auth_checkbox").get_active() == False:
            self.minibox_sensitivity(False, 'ftp')
        elif self.obj("use_same_proxy_checkbox").get_active() == False:
            self.minibox_sensitivity(True, 'ftp')
    
    def onchange_http_proxy_textbox(self, widget):
        if self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_proxy_textbox").set_text(
                self.obj("http_proxy_textbox").get_text())
            self.obj("ftp_proxy_textbox").set_text(
                self.obj("http_proxy_textbox").get_text())
    
    def onchange_http_port_textbox(self, widget):
        if self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_port_textbox").set_text(
                self.obj("http_port_textbox").get_text())
            self.obj("ftp_port_textbox").set_text(
                self.obj("http_port_textbox").get_text())
    
    def onchange_http_user_textbox(self, widget):
        if self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_user_textbox").set_text(
                self.obj("http_user_textbox").get_text())
            self.obj("ftp_user_textbox").set_text(
                self.obj("http_user_textbox").get_text())
    
    def onchange_http_password_textbox(self, widget):
        if self.obj("use_same_proxy_checkbox").get_active() == True:
            self.obj("https_password_textbox").set_text(
                self.obj("http_password_textbox").get_text())
            self.obj("ftp_password_textbox").set_text(
                self.obj("http_password_textbox").get_text())
    
    def quit(self, widget):
        sys.exit(0)


class ApplyProxy:
    def __init__(self, is_proxy=False, credentials=None):
        if is_proxy == False:
            self.clearproxy(UNSET_EXISTING_VARIABLES)
            self.display_success()
        else:
            errors = credentials.validate()
            if len(errors) == 0:
                self.clearproxy(DO_NOTHING)
                self.update_files(credentials)
                self.display_success()
            else:
                self.display_error(errors) ##
            
    def clearproxy(self, state):
        """ Removes existing proxy from the system.
            if the value of state is UNSET_EXISTING_VARIABLES, it unsets the 
            existing proxy environment variables from the shells spawned after 
            this program is executed """
        # Clearing /etc/bash.bashrc file
        bashrc_file = open('/etc/bash.bashrc','r')
        bashrc_contents = bashrc_file.readlines()
        bashrc_file.close()

        bashrc_file = open('/etc/bash.bashrc', 'w')
        for i in range(len(bashrc_contents)):
            if bashrc_contents[i].lower().startswith('export http_proxy') or \
                    bashrc_contents[i].lower().startswith('export https_proxy') or \
                    bashrc_contents[i].lower().startswith('export ftp_proxy') or \
                    bashrc_contents[i].lower().startswith('unset http_proxy') or \
                    bashrc_contents[i].lower().startswith('unset ftp_proxy') or \
                    bashrc_contents[i].lower().startswith('unset https_proxy'):
                    
                bashrc_contents[i] = ''
        bashrc_file.write(''.join(bashrc_contents))
        
        if state == UNSET_EXISTING_VARIABLES:
            bashrc_file.write('unset http_proxy\n')
            bashrc_file.write('unset https_proxy\n')
            bashrc_file.write('unset ftp_proxy\n')
        
        bashrc_file.close()
        
        # Clearing /etc/environment file
        env_file = open('/etc/environment','r')
        env_contents = env_file.readlines()
        env_file.close()
        env_file = open('/etc/environment','w')
        for i in range(len(env_contents)):
            if env_contents[i].lower().startswith('http_proxy') or \
                    env_contents[i].lower().startswith('https_proxy') or \
                    env_contents[i].lower().startswith('ftp_proxy'):
                env_contents[i] = ''
        env_file.write(''.join(env_contents))
        env_file.close()
        
        # Clearing /etc/apt/apt.conf file
        aptconf_file = open('/etc/apt/apt.conf', 'w')
        aptconf_file.write('')
        aptconf_file.close()
        
        ## clear proxy from synaptic
        if os.path.exists('/root/.synaptic/synaptic.conf'):
            sconf_file = open('/root/.synaptic/synaptic.conf', 'r')
            sconf_contents = sconf_file.readlines()
            sconf_file.close()
            
            for i in range(len(sconf_contents)):
                if sconf_contents[i].find('useProxy') > -1:
                    sconf_contents[i] = list(sconf_contents[i])
                    sconf_contents[i][12] = '0'
                    sconf_contents[i] = ''.join(sconf_contents[i])
                    break
            
            sconf_file = open('/root/.synaptic/synaptic.conf', 'w')
            sconf_file.writelines(sconf_contents)
            sconf_file.close()

        
    def update_files(self, credentials):
        """
        Updates all the four files with provided proxy values.
        Assumes all four files is already clear of all previous proxies.
        """

        combo_string = credentials.proxy_address + ':' + credentials.proxy_port
        if credentials.is_auth() == True:
            combo_string = credentials.username + ':' + credentials.password + '@' + combo_string
        
        # Update /etc/bash.bashrc, /etc/environment, and /etc/apt/apt.conf file
        bashrc_file = open('/etc/bash.bashrc', 'a')
        env_file = open('/etc/environment', 'a')
        aptconf_file = open('/etc/apt/apt.conf', 'a')

        protocols = ['http', 'https', 'ftp']
        
        for i in protocols:
            bashrc_file.write('export ' + i + '_proxy=' + i + '://' + combo_string + '/\n')
            env_file.write(i + '_proxy="' + i + '://' + combo_string + '/"\n')
            aptconf_file.write('Acquire::' + i + '::Proxy "' + i + '://' + combo_string + '/";\n')
            
        bashrc_file.close()
        env_file.close()
        aptconf_file.close()
        
        # Update /root/.synaptic/synaptic.conf file
        if os.path.exists('/root/.synaptic/synaptic.conf'):
            sconf_file = open('/root/.synaptic/synaptic.conf', 'r')
            sconf_contents = sconf_file.readlines()
            sconf_file.close()
            
            value = {
                'useProxy'      : '1',
                'httpProxyUser' : credentials.username,
                'httpProxyPass' : credentials.password,
                'httpProxy'     : credentials.proxy_address,
                'httpProxyPort' : credentials.proxy_port,
                'ftpProxy'      : credentials.proxy_address,
                'ftpProxyPort'  : credentials.proxy_port,
                }
            
            def change_value(string):
                """
                For a line 'string' of synaptic.conf file, it assigns to 'name' attribute a value 'value'
                """
                
                split_string = string.split('"')
                if len(split_string) == 3:
                    string_name = split_string[0].split()[0]
                    string_value = split_string[1]
                    
                    if value.has_key(string_name) == True:
                        string_value = value[string_name]
                        updated_string = '  ' + string_name + ' "' + string_value + '";\n'
                        return updated_string
                return string
                
            for i in range(len(sconf_contents)):
                sconf_contents[i] = change_value(sconf_contents[i])
            
            sconf_file = open('/root/.synaptic/synaptic.conf', 'w')
            sconf_file.writelines(sconf_contents)
            sconf_file.close()

    def display_error(self, errorcodes):
        error_window = PopUp()
        error_text = 'Please check the following errors:\n'
        disp_string = {
            PROXY_ADDRESS_INCORRECT     : 'Enter proxy address in correct format.',
            PROXY_PORT_INCORRECT        : 'Proxy port should be an integer between 0 and 65535.',
            PROXY_CREDENTIALS_INCORRECT : 'Only username or only password cannot be null.',
        }
        for i in range(len(errorcodes)):
            error_text += ('    ' + str(i+1) + '. ' + disp_string[errorcodes[i]] + '\n')
        error_window.popup_text(error_text)
        error_window.builder.get_object('main_window').show_all()

    def display_success(self):
        popup = DestructionPopUp()
        popup.popup_text('Proxy applied to the system! :)')
        popup.builder.get_object('main_window').show_all()



proxyMan = ProxyMan()
window = proxyMan.builder.get_object("main_window")
window.show_all()
if os.geteuid() != 0:
    noRoot = DestructionPopUp()
    noRoot.popup_text('Please run the application as ROOT user')
    noRoot.builder.get_object('main_window').show_all()
    
Gtk.main()
