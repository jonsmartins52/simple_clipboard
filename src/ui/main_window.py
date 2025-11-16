import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class MainWindow(Gtk.Window):
  def __init__(self, clipboard_manager):
    super().__init__(title="Clipboard History")
    self.set_default_size(400,300)
    self.clipboard_manager = clipboard_manager
    self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    self.add(vbox)

    self.liststore = Gtk.ListStore(str)
    self.treeview = Gtk.TreeView(model=self.liststore)

    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn("Histórico", renderer, text=0)
    self.treeview.append_column(column)
    vbox.pack_start(self.treeview, True, True, 0)

    self.treeview.connect("row-activated", self.on_row_activated)

  def update_history(self, new_item):
    self.liststore.clear()
    for item in self.clipboard_manager.history:
      self.liststore.append([item])

  def on_row_activated(self, treeview, path, column):
    model = treeview.get_model()
    item = model[path][0]
    self.clipboard.set_text(item, -1)
    print(f"Copiando novamente: {item}")