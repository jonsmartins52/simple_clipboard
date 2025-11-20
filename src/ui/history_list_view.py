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

      box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
      box.get_style_context().add_class("history-row")
      box.set_margin_top(6)
      box.set_margin_bottom(6)
      box.set_margin_start(10)
      box.set_margin_end(10)
      
      title = Gtk.Label(xalign=0)
      title.get_style_context().add_class("history-title")
      highlighted_title = self._highlight_text(title_text, query)
      title.set_markup(f"<b>{highlighted_title}</b>")
      title.set_line_wrap(False)

      body = Gtk.Label( xalign=0)
      body.get_style_context().add_class("history-body")
      highlighted_body = self._highlight_text(body_text, query)
      body.set_markup(highlighted_body)
      body.set_line_wrap(True)
      body.set_max_width_chars(60)

      box.pack_start(title, False, False, 0)
      box.pack_start(body, False, False, 0)

      row = Gtk.ListBoxRow()
      row.full_text = full_text
      row.add(box)

      return row

  # --------------------------------------------------------
  # Evento de clique no item
  # --------------------------------------------------------
  def _on_row_activated(self, listbox, row):
      if hasattr(row, "full_text"):
          if self.on_item_selected:
              self.on_item_selected(row.full_text)

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
