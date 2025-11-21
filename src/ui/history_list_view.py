import gi
#gi.require_version("Gtk", "3,0")
from gi.repository import Gtk, GLib

class HistoryListView(Gtk.ScrolledWindow):
  def __init__(self, on_item_selected):
    super().__init__()
    self.on_item_selected = on_item_selected
    self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

    self.listbox = Gtk.ListBox()
    self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
    self.listbox.connect("row-activated", self._on_row_activated)
    self.add(self.listbox)

  def _smart_truncate(self, text:str, max_chars: int) -> str:
     if len(text) <= max_chars:
        return text
     return text[:max_chars -3] + "..."

  def render_items(self, items: list[str], query: str = ""):
    for child in self.listbox.get_children():
      self.listbox.remove(child)

    for text in items:
      row = self._create_list_item(text, query)
      self.listbox.add(row)

    self.listbox.show_all()

  def _create_list_item(self, full_text: str, query: str):
      first_line = full_text.split("\n", 1)[0]
      
      title_text = self._smart_truncate(first_line, 60)
      body_text = self._smart_truncate(full_text, 120)

      box = self._build_container_box()
      
      title = self._build_title_label(title_text, query)

      body = self._build_body_label(body_text, query)

      copied_label = self._build_copied_label()

    # container horizontal para body + copied
      bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
      bottom_box.pack_start(body, True, True, 0)
      bottom_box.pack_end(copied_label, False, False, 0)

      # montar UI
      box.pack_start(title, False, False, 0)
      box.pack_start(bottom_box, False, False, 0)      

      row = Gtk.ListBoxRow()
      row.full_text = full_text
      row.copied_label = copied_label
      row.add(box)

      return row

  def _build_container_box(self):
     box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
     box.get_style_context().add_class("history-row")
     box.set_margin_top(6)
     box.set_margin_bottom(6)
     box.set_margin_start(10)
     box.set_margin_end(10)
     return box

  def _build_title_label(self, text: str, query: str):
     title = Gtk.Label(xalign=0)
     title.get_style_context().add_class("history-title")
     highlighted_title = self._highlight_text(text, query)
     title.set_markup(f"<b>{highlighted_title}</b>")
     title.set_line_wrap(False)
     return title

  def _build_body_label(self, text: str, query: str):
     body = Gtk.Label( xalign=0)
     body.get_style_context().add_class("history-body")
     highlighted_body = self._highlight_text(text, query)
     body.set_markup(highlighted_body)
     body.set_line_wrap(True)
     body.set_max_width_chars(60)
     return body
  
  def _build_copied_label(self):
    copied_label = Gtk.Label(label="✓ Copiado", xalign=1)
    copied_label.set_no_show_all(True)
    copied_label.set_opacity(0.0)
    copied_label.get_style_context().add_class("copied-label")
    return copied_label

  
  # --------------------------------------------------------
  # Evento de clique no item
  # --------------------------------------------------------
  def _on_row_activated(self, listbox, row):
      if hasattr(row, "full_text"):
          if self.on_item_selected:
              self.on_item_selected(row.full_text)

      if hasattr(row, "copied_label"):
         label = row.copied_label
         label.show()
         label.set_opacity(1.0)
         GLib.timeout_add(600, self._start_fade_out, label)

 
  def _start_fade_out(self, label):
     self._fade_step(label, 1.0)
     return False
  
  def _fade_step(self, label, opacity):
     opacity -= 0.1

     if opacity <= 0:
        label.hide()
        label.set_opacity(0.0)
        return False
     
     label.set_opacity(opacity)
     GLib.timeout_add(50, self._fade_step, label, opacity)
     return False

  def _highlight_text(self, text: str, query: str) -> str:
    if not query:
        return GLib.markup_escape_text(text)

    lower = text.lower()
    q = query.lower()

    start = lower.find(q)
    if start == -1:
        return GLib.markup_escape_text(text)

    end = start + len(query)

    before = GLib.markup_escape_text(text[:start])
    match = GLib.markup_escape_text(text[start:end])
    after = GLib.markup_escape_text(text[end:])

    return f"{before}<span background='#fff3a0'>{match}</span>{after}"
