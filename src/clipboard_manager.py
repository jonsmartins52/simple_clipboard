import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class ClipboardManager:
  def __init__(self, callback, poll_interval=0.5):
     self.history = []
     self.callback = callback
     self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
     self._last_text = ""
     self._timeout_id = None

  def start(self):
    self._timeout_id = GLib.timeout_add(500, self._check_clipboard)

  def stop(self):
    if self._timeout_id:
      GLib.source_remove(self._timeout_id)
      self._timeout_id = None

  def _check_clipboard(self):
    text = self.clipboard.wait_for_text()
    if text and text != self._last_text:
      self._last_text = text
      if text not in self.history:
        self.history.insert(0, text)
        self.history = self.history[:20]
        if self.callback:
          self.callback(text)

    return True