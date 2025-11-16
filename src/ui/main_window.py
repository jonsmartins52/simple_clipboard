import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class MainWindow(Gtk.Window):
  def __init__(self, controller, clipboard):
    super().__init__(title="Clipboard History")
    self.set_default_size(600,400)

    self.controller = controller
    self.clipboard = clipboard    

    self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    self.add(self.vbox)

    self._build_header()       
    self._build_list()
    self._build_footer()
  
  '''
    UI Builders
  '''
  def _build_header(self):
    self.search_entry = Gtk.Entry()
    self.search_entry.set_placeholder_text("Buscar no histórico...")
    self.search_entry.connect("changed", self.on_search_changed)

    self.search_entry.set_margin_top(10)
    self.search_entry.set_margin_start(10)
    self.search_entry.set_margin_end(10)
    self.search_entry.set_margin_bottom(6)

    self.vbox.pack_start(self.search_entry, False, False, 0)

  def _build_list(self):
    self.scrolled = Gtk.ScrolledWindow()
    self.vbox.pack_start(self.scrolled, True, True, 0)
    self.listbox = Gtk.ListBox()
    self.listbox.connect("row-activated", self.on_row_activated)
    self.scrolled.add(self.listbox)

  def _build_footer(self):
    footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    footer.set_margin_start(10)
    footer.set_margin_end(10)
    footer.set_margin_bottom(10)
    self.vbox.pack_start(footer, False, False, 0)

    clear_btn = Gtk.Button(label="Limpar histórico")
    clear_btn.connect("clicked", self.on_clear_clicked)

    footer.pack_start(clear_btn, False, False, 0)
  
  '''
    Métodos de atualização da UI
  '''
  def populate_list(self, items):
    for child in self.listbox.get_children():
      self.listbox.remove(child)

    for text in items:
      row = self.create_list_item(text)
      self.listbox.add(row)

    self.listbox.show_all()

  def create_list_item(self, full_text):
    first_line = full_text.split("\n")[0][:60]
    if len(full_text.split("\n")[0]) > 60:
      first_line += "..."

    if len(full_text) > 120:
        display_text = full_text[:120] + "..."
    else:
        display_text = full_text

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
    box.set_margin_top(6)
    box.set_margin_bottom(6)
    box.set_margin_start(10)
    box.set_margin_end(10)    

    escaped_title = GLib.markup_escape_text(first_line)
    title = Gtk.Label(label=first_line, xalign=0)
    title.set_markup(f"<b>{escaped_title}</b>")
    title.set_line_wrap(False)

    body = Gtk.Label(label=display_text, xalign=0)
    body.set_line_wrap(True)
    body.set_max_width_chars(60)

    box.pack_start(title, False, False, 0)
    box.pack_start(body, False, False, 0)

    row = Gtk.ListBoxRow()
    row.add(box)

    #row.clipboard_text = full_text

    return row

  '''
    Eventos da UI
  '''
  def on_clear_clicked(self, button):
    dialog = Gtk.MessageDialog(
      transient_for=self,
      flags=0,
      message_type=Gtk.MessageType.WARNING,
      buttons=Gtk.ButtonsType.OK_CANCEL,
      text="Limpar histórico?"
    )
    dialog.format_secondary_text("Esta ação não pode ser desfeita.")
    response = dialog.run()
    dialog.destroy()

    if response == Gtk.ResponseType.OK:
      self.controller.clear()

  def on_search_changed(self, entry):
    query = entry.get_text()
    self.controller.apply_query(query) 

  def _get_full_text_from_row(self, row):
    box = row.get_child()
    children = box.get_children()

    if len(children) >= 2:
      body_label = children[1]
      return body_label.get_text()

    return ""
  
  def on_row_activated(self, listbox, row):
    text = self._get_full_text_from_row(row)
    if not text:
        return

    self.clipboard.set_text(text, -1)

    try:
        self.clipboard.store()
    except Exception:
        pass

  