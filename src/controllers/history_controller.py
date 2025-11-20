class HistoryController:
  def __init__(self, clipboard_manager, on_history_changed):
    self.clipboard_manager = clipboard_manager
    self.on_history_changed = on_history_changed

    self.query = ""

    self.full_history = clipboard_manager.history.copy()
    self.filtered_history = self.full_history.copy()

    self.clipboard_manager.callback = self.add_item

  def apply_query(self, query: str):
    self.query = query.lower().strip()

    if self.query == "":
      self.filtered_history = self.full_history.copy()
    else:
      self.filtered_history = [
        item for item in self.full_history
        if self.query in item.lower()
      ]

    self._notify()
  
  def add_item(self, next_text):
    self.full_history = self.clipboard_manager.history.copy()
    self.filtered_history = self.full_history.copy()
    self._notify()

  def clear(self):
    self.clipboard_manager.clear_history()
    self.full_history = []
    self.filtered_history = []
    self._notify()

  def _notify(self):
    if self.on_history_changed:
      self.on_history_changed(self.filtered_history)