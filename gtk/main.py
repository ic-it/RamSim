from ast import Gt
import inspect
from pprint import pprint
import sys
import gi

gi.require_version('Gtk', '4.0')

# from gi.repository import Gtk, Gio
from gi.repository import Gtk, Gio
from window import RamsimWindow, AboutDialog


class RamsimApplication(Gtk.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='org.example.App',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.quit_action, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('open_file', self.on_open, ["<Control>o"])
        self.create_action('save_file', self.on_save, ["<Control>s"])

        self.open_dialog = Gtk.FileChooserNative.new(title="Choose a file",
                                                     parent=self.props.active_window, action=Gtk.FileChooserAction.OPEN)
        self.open_dialog.connect("response", self.open_response)
        # f = Gtk.FileFilter()
        # f.set_name("RAM files")
        # f.add_mime_type("*/ram")
        # self.open_dialog.add_filter(f)
    def quit_action(self, *args):
        self.quit()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = RamsimWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = AboutDialog(self.props.active_window)
        about.present()
    
    def on_save(self, widget, _):
        self.props.active_window.save_file()
    
    def on_open(self, widget, _):
        self.open_dialog.show()
    
    def open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            filename = file.get_path()
            self.props.active_window.open_file(filename)

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = RamsimApplication()
    return app.run(sys.argv)


main(1)