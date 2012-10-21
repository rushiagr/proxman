from gi.repository import Gtk

from ui import *

proxyMan = MainWindow()
window = proxyMan.builder.get_object("main_window")
window.show_all()
if os.geteuid() != 0:
    noRoot = DestructionPopUp()
    noRoot.popup_text('Please run the application as ROOT user')
    noRoot.builder.get_object('main_window').show_all()
    
Gtk.main()

