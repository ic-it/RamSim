import os
from typing import List
from gi.repository import Gtk
from gi.repository import GtkSource, Gio

from ramsim.ops import ops, HALT, AdditionalOp, OpS, OpI
from ramsim.parser import Parser
from ramsim.executor import Executor
from ramsim.iout import IOut
from ramsim.iiostream import IIOstream
from ramsim.register import Register



class Codeview(GtkSource.View):
    def __init__(self) -> None:
        super().__init__()

        # Get the application settings
        # self.settings = Gio.Settings(string=open("gtk/dev.eglenelidgamaliel.code.json", 'r').read())

        # # Connect to the settings style-scheme change signal
        # self.settings.connect("changed::code-view-style-scheme", self.on_style_scheme_changed)
        # self.on_style_scheme_changed(self.settings, "code-view-style-scheme")

        # Set GtkSource.View properties
        self.set_show_line_numbers(True)
        self.set_auto_indent(True)
        self.set_highlight_current_line(True)
        self.set_monospace(True)
        self.set_top_margin(10)
        self.set_bottom_margin(10)

        self.file = None

    def on_style_scheme_changed(self, settings: Gio.Settings, key: str) -> None:
        style_scheme_id = settings.get_string("code-view-style-scheme")
        style_scheme = GtkSource.StyleSchemeManager.get_default().get_scheme(style_scheme_id)
        self.get_buffer().set_style_scheme(style_scheme)




@Gtk.Template(string=open('gtk/window.ui', 'r').read())
class RamsimWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'RamsimWindow'

    class Out(IOut):
        def __init__(self, win) -> None:
            self.win = win
        
        def runtime_error(self, text: str, line: int = None, file_path: str = None):
            data = f"Runtime error%s%s:" % (f" on line {line}"if line else "", f" in file {file_path}" if file_path else "") + " " + text
            self.win.info_outb.insert_markup(self.win.info_outb.get_start_iter(), f'<span color="red">{data}</span>\n', -1)
        
        def syntax_error(self, text: str, line: int, file_path: str):
            data = f"Syntax error on line {line} in {file_path}:" + " " + text
            self.win.info_outb.insert_markup(self.win.info_outb.get_start_iter(), f'<span color="red">{data}</span>\n', -1)
    
    class IOstream(IIOstream):
        def __init__(self, win) -> None:
            self.win = win
        def input(self) -> int:
            ...
        
        def output(self, value: int):
            self.win.output.set_text(self.win.output.get_text() + f"{value};")
            

    info_out = Gtk.Template.Child("info_out")
    # code = Codeview()
    code = Gtk.Template.Child("code")
    open_file_button = Gtk.Template.Child("open_file_button")
    save_file_button = Gtk.Template.Child("save_file_button")
    run_button = Gtk.Template.Child("run_button") 
    output = Gtk.Template.Child("output")

    bufer = Gtk.Template.Child("bufer")
    bufer_id_col = Gtk.Template.Child("bufer_id_col")
    bufer_value_col = Gtk.Template.Child("bufer_value_col")
    edited = False

    codewin = Gtk.Template.Child("codewin")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_path = None
        self.codeb = self.code.get_buffer()
        self.info_outb = self.info_out.get_buffer()
        self.outputb = self.output.get_buffer()
        # self.codewin.set_child(self.code)

        self.codeb.connect("changed", self.highlite_code)
        self.open_file_button.connect("clicked", lambda _:self.get_application().on_open(_,_))
        self.save_file_button.connect("clicked", lambda _:self.save_file())
        self.run_button.connect("clicked", lambda _:self.run_code())
    
    def highlite_code(self, editable):
        # return
        if not self.edited:
            self.edited = True
            text = editable.get_text(editable.get_start_iter(), editable.get_end_iter(), None)
            ti = editable.get_start_iter()
            cpos = ti.get_offset()
            cpos = editable.get_property()
            ops_colors = {
                HALT: "#FF5936",
                AdditionalOp: "#3698FF",
                OpS: "#41B641",
                OpI: "#9841B6",
            }
            other_colors = {
                "comment": "#787878",
                "label": "#D0CA0E"
            }
            rlines = []
            lines: List[str] = text.split("\n")
            for line in lines:
                comment = ""
                start_spaces = 0
                end_spaces = 0
                while line.startswith(" "):
                    line = line[1:]
                    start_spaces += 1
                while line.endswith(" "):
                    line = line[:-1]
                    end_spaces += 1
                if "#" in line:
                    line, comment = line.split("#", 1)
                    comment = f'<span color="{other_colors.get("comment")}">#{comment}</span>'
                if line.endswith(":"):
                    line = f'<span color="{other_colors.get("label")}">{line}</span>'
                for op in ops:
                    for token in op.tokens:
                        if line.upper().startswith(token):
                            color = ""
                            for opi in ops_colors:
                                if issubclass(op, opi):
                                    color = ops_colors.get(opi)
                            if color:
                                line = f'<span color="{color}">{line[:len(token)]}</span>' + line[len(token):]

                rlines.append(" "*start_spaces + line + comment + " "*end_spaces)
            
            text = "\n".join(rlines)
        
            editable.set_text("", -1)
            editable.insert_markup(editable.get_start_iter(), text, -1)
            ti = editable.get_start_iter()
            ti.set_offset(cpos)
            editable.place_cursor(ti)
            self.edited = False
    
    def open_file(self, file_path: str):
        self.file_path = file_path
        with open(file_path, "r") as f:
            self.codeb.set_text("", -1)
            self.codeb.insert(self.codeb.get_end_iter(), f.read())
        self.info_outb.insert(self.info_outb.get_start_iter(), f"Loaded file: {self.file_path}\n")
    
    def save_file(self):
        if not self.file_path:
            return
        else:
            with open(self.file_path, "w") as f:
                f.write(self.codeb.get_text(self.codeb.get_start_iter(), self.codeb.get_end_iter(), None))
            self.info_outb.insert(self.info_outb.get_start_iter(), f"Saved file: {self.file_path}\n")
    
    def run_code(self):
        if not self.file_path:
            return
        self.save_file()
        self.output.set_text("")
        
        path = os.path.dirname(self.file_path) + "/"
        p = Parser(self.file_path, self.Out(self))
        if not p.parse():
            return
        e = Executor(p.parsed_data, self.Out(self), self.IOstream(self), Register(), path)
        e.execute()



class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'RamSim'
        self.props.version = "0.1.0"
        self.props.authors = ['Illia Chaban']
        self.props.copyright = '2022 Illia'
        # self.props.logo_icon_name = 'org.example.App'
        self.props.modal = True
        self.set_transient_for(parent)
