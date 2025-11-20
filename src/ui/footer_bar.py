import gi
#gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FooterBar(Gtk.Box):
    def __init__(self, on_clear_clicked):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)

        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_bottom(10)

        self.clear_btn = Gtk.Button(label="Limpar histórico")
        self.clear_btn.connect("clicked", self._on_clear)

        self.pack_start(self.clear_btn, False, False, 0)

        self.on_clear_clicked = on_clear_clicked

    def _on_clear(self, button):
        if self.on_clear_clicked:
            self.on_clear_clicked()
