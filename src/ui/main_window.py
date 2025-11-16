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

    # Search bar
    self.search_entry = Gtk.Entry()
    self.search_entry.set_placeholder_text("Buscar no histórico...")
    self.search_entry.connect("changed", self.on_search_changed)
    vbox.pack_start(self.search_entry, False, False, 0)

    # Scroll area
    scrolled = Gtk.ScrolledWindow()
    vbox.pack_start(scrolled, True, True, 0)

    self.listbox = Gtk.ListBox()
    scrolled.add(self.listbox)

    self.listbox.connect("row-activated", self.on_row_activated)

    self.full_history = self.clipboard_manager.history
    self.populate_list(self.full_history)

  def populate_list(self, items):
    for child in self.listbox.get_children():
      self.listbox.remove(child)

    for text in items:
      label = Gtk.Label(label=text, xalign=0)
      row = Gtk.ListBoxRow()
      row.add(label)
      self.listbox.add(row)

    self.listbox.show_all()

  def update_history(self, new_item):
    self.full_history = self.clipboard_manager.history
    self.apply_filter()

  
  def on_search_changed(self, entry):
    self.apply_filter()
    

  def apply_filter(self):
    query = self.search_entry.get_text().lower().strip()
    if query == "":
      filtered = self.full_history
    else:
      filtered = [
        item for item in self.full_history
        if query in item.lower()
      ]

    self.populate_list(filtered)

  def on_row_activated(self, listbox, row):
    child = row.get_child()
    if not child:
      return
    
    try:
      text = child.get_text()
    except Exception:
      label = child.get_child()
      text = label.get_text() if label else ""

    if not text:
      return
    
    self.clipboard.set_text(text, -1)

    try:
      self.clipboard.store()
    except Exception:
      pass

  '''def on_item_clicked(self, row, evnet):
    label = row.get_child()
    text = label.get_text()

    self.clipboard.set_text(text, -1)'''