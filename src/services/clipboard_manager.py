import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class ClipboardManager:
  def __init__(self, callback, storage):
     self.storage = storage
     self.history = storage.load()
     self.callback = callback
     self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
     self._last_text = ""
     self._timeout_id = None
     self.max_items = 20

  def start(self):
    initial = self.clipboard.wait_for_text()
    if initial:
      self._last_text = initial
      
    self._timeout_id = GLib.timeout_add(500, self._check_clipboard)

  def stop(self):
    if self._timeout_id:
      GLib.source_remove(self._timeout_id)
      self._timeout_id = None
    try:
      self.storage.save(self.history)
    except Exception:
      pass

  def clear_history(self):
    self.history = []
    self.storage.save(self.history)
    self.clipboard.set_text("", -1)
    try:
      self.clipboard.store()
    except:
      pass
      
    self._last_text = ""
  
  def _check_clipboard(self):
    try:
      text = self.clipboard.wait_for_text()
    except Exception as e:
      return True
    
    if text and text != self._last_text:
      self._last_text = text

      if text in self.history:
        self.history.remove(text)

      self.history.insert(0, text)
      self.history = self.history[:self.max_items]

      self.storage.save(self.history)

      if self.callback:
        self.callback(text)
    

    return True