import os
import sys
import pickle

from gi.repository import Gtk

from credentials import Credentials
from proxy_man import ApplyProxy

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
    """ On clicking OK button, this popup destroys. """
    def on_click_ok(self, widget):
        sys.exit()

class SavePopup:
    """
    Class for popup which appears and asks for the name by which one want to
    save the profile as.
    """
    def __init__(self, profiles, default_save_name=''):
        """ Profiles is list of profiles to pickle"""
        self.builder = Gtk.Builder()
        self.builder.add_from_file('save.glade')
        dic = {
            'onclick_save_button': self.onclick_save_button,
            'onclick_cancel_button': self.onclick_cancel_button,
        }
        self.builder.connect_signals(dic)
        self.builder.get_object('save_textbox').set_text(default_save_name)
        self.profiles_list = profiles
        
    def onclick_save_button(self, widget):
        last_correct_element = {
            'name': self.builder.get_object('save_textbox').get_text(),
            'value': self.profiles_list[-1]
        }
        self.profiles_list[-1] = last_correct_element
        profile_file = open('profile.dat', 'wb')
        pickle.dump(self.profiles_list,profile_file)
        self.builder.get_object('main_window').destroy()
        return 
    
    def onclick_cancel_button(self, widget):
        self.builder.get_object('main_window').destroy()

class MainWindow:
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

        profile_file = open('profile.dat', 'rb')
        file_data = profile_file.readlines()
        profile_file.close()

        profile_file = open('profile.dat', 'rb')
        
        if file_data[0] == '\n':
            self.saved_profiles = []
        else:
            self.saved_profiles = pickle.load(profile_file)
        
        profile_file.close()

        for profile in self.saved_profiles:
            self.obj('comboboxtext1').append_text(profile['name'])
        
        dic = { 
            "onclick_quit_window": self.quit,
            
            "onclick_cancel_button": self.quit,
            "onclick_apply_button": self.onclick_apply_button,
            "onclick_load_button": self.onclick_load_button,
            "onclick_save_button": self.onclick_save_button,

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
            

    def get_data(self):
        """
        Takes all the data from the user interface and bundles it into a
        dictionary, and returns it
        """
        data = {}
        if self.obj('not_use_proxy_radio').get_active() == True:
            data['noproxy'] = True
        else:
            data['noproxy'] = False

            data['http'] = {
                'proxy': self.obj('http_proxy_textbox').get_text(),
                'port': self.obj('http_port_textbox').get_text(),
                'user': self.obj('http_user_textbox').get_text(),
                'password': self.obj('http_password_textbox').get_text(),
                'use_auth': True if self.obj('http_use_auth_checkbox')
                        .get_active() is True else False,
            }

            if self.obj('use_same_proxy_checkbox').get_active() is True:
                data['sameproxy'] = True
            else:
                data['sameproxy'] = False

                data['https'] = {
                    'proxy': self.obj('https_proxy_textbox').get_text(),
                    'port': self.obj('https_port_textbox').get_text(),
                    'user': self.obj('https_user_textbox').get_text(),
                    'password': self.obj('https_password_textbox').get_text(),
                    'use_auth': True if self.obj('https_use_auth_checkbox')
                            .get_active() is True else False,
                }
                
                data['ftp'] = {
                    'proxy': self.obj('ftp_proxy_textbox').get_text(),
                    'port': self.obj('ftp_port_textbox').get_text(),
                    'user': self.obj('ftp_user_textbox').get_text(),
                    'password': self.obj('ftp_password_textbox').get_text(),
                    'use_auth': True if self.obj('ftp_use_auth_checkbox')
                            .get_active() is True else False,
                }
                
        return data

    def set_data(self, data):
        """
        Takes the dictionary and fills the values in the UI accordingly
        """
        if data['noproxy'] is True:
            self.obj('not_use_proxy_radio').set_active(True)
            self.obj('all_values_box').set_sensitive(False)
        else:
            self.obj('not_use_proxy_radio').set_active(False)
            self.obj('use_proxy_radio').set_active(True)
            self.obj('all_values_box').set_sensitive(True)
            if data['sameproxy'] is True:
                self.obj('use_same_proxy_checkbox').set_active(True)
                proxies = ['http']
                self.obj('https_grid').set_sensitive(False)
                self.obj('ftp_grid').set_sensitive(False)
            else:
                self.obj('use_same_proxy_checkbox').set_active(False)
                proxies = ['http', 'https', 'ftp']
                self.obj('https_grid').set_sensitive(True)
                self.obj('ftp_grid').set_sensitive(True)
            for proxy in proxies:
                for label in ['proxy', 'port', 'user', 'password']:
                    self.obj(proxy+'_'+label+'_textbox').set_text(data[proxy][label])
                if data[proxy]['use_auth'] is False:
                    self.minibox_sensitivity(False, proxy)
                else:
                    self.minibox_sensitivity(True, proxy)
        
        

    def onclick_apply_button(self, widget):
        
        dat = self.get_data()
#        print dat
        
        cred = Credentials(dat)
        errors = cred.validate()
        
        if len(errors) is not 0:
            error_window = PopUp()
            error_text = 'Please check the following errors:\n'
            for i in range(len(errors)):
                error_text += ('    ' + str(i+1) + '. ' + errors[i] + '\n')
            error_window.popup_text(error_text)
            error_window.builder.get_object('main_window').show_all()
            return
        
        if ApplyProxy(cred).status is 'success':
            popup = DestructionPopUp()
            popup.popup_text('Proxy applied to the system! :)')
            popup.builder.get_object('main_window').show_all()

    def onclick_save_button(self, widget):
        #TODO(rushiagr): check if all the values from all fields are valid
        
        #NOTE(rushiagr): here, the last element of profile_list is the
        #       dictionary returned by function get_data. This last element
        #       will be modified in SavePopup class.
        
        profile_file = open('profile.dat', 'rb')
        file_data = profile_file.readlines()
        profile_file.close()
        profile_file = open('profile.dat', 'rb')
        
        if file_data[0] == '\n':
            profile_list = []
        else:
            profile_list = pickle.load(profile_file)
        
        profile_file.close()
        profile_list.append(self.get_data())
        
        
        default_profile_name = 'profile'+str(len(profile_list))
        save_popup = SavePopup(profile_list, default_profile_name)
        save_popup.builder.get_object('main_window').show_all()
        
        
        pass
    
    def onclick_load_button(self, widget):
#        print self.saved_profiles
#        self.set_data(self.saved_profiles)
        selected = self.obj('comboboxtext1').get_active_text()
#        print selected
        if selected is not None:
            for profile in self.saved_profiles:
                if profile['name'] == selected:
                    self.set_data(profile['value'])
        pass
    
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

