import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from clipboard_manager import ClipboardManager
from ui.main_window import MainWindow

def main():
  manager = ClipboardManager(callback=None)
  
  win = MainWindow(manager)
  win.connect("destroy", Gtk.main_quit)
  
  
  def on_new_clipboard_item(text):
    if win:
      win.update_history(text)

  manager.callback = on_new_clipboard_item
  manager.start()
  
  win.show_all()

  Gtk.main()
  manager.stop()

if __name__ == "__main__":
  main()
