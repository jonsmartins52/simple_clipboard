import gi
#gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class SearchBar(Gtk.Box):
    def __init__(self, on_query_changed):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Buscar no histórico...")

        # margens
        self.entry.set_margin_top(10)
        self.entry.set_margin_start(10)
        self.entry.set_margin_end(10)
        self.entry.set_margin_bottom(6)

        self.entry.connect("changed", self._on_changed)

        self.on_query_changed = on_query_changed

        self.pack_start(self.entry, False, False, 0)

    def _on_changed(self, entry):
        if self.on_query_changed:
            self.on_query_changed(entry.get_text())
