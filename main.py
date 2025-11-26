import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from src.services.clipboard_manager import ClipboardManager
from src.services.json_storage import JsonStorage
from src.ui.main_window import MainWindow
from src.controllers.history_controller import HistoryController

def main():
  storage = JsonStorage()
  manager = ClipboardManager(callback=None, storage=storage)
  controller = HistoryController(manager, on_history_changed=None)
  
  win = MainWindow(controller, manager.clipboard)
  controller.on_history_changed = win.on_history_changed

  manager.start()

  win.connect("destroy", Gtk.main_quit)
  win.show_all()
  Gtk.main()

if __name__ == "__main__":
  main()