import os 
from gi.repository import Gio, Gtk, GdkPixbuf

def _is_dark_theme() -> bool:
  # detecta o tema atual do sistema usando variantes "dark"
  settings = Gtk.Settings.get_default()
  if not settings:
    return False
  
  theme_name = settings.get_property("gtk-theme-name")
  if not theme_name:
    return False
  
  theme_name = theme_name.lower()
  return "dark" in theme_name or "-dark" in theme_name

def load_app_icon(base_path: str):
  dark = _is_dark_theme()
  preferred = base_path + ("_dark" if dark else "_light")
  svg_path = preferred + ".svg"
  png_path = preferred + ".png"

  if os.path.exists(svg_path):
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(svg_path, 64,64)
    print(f"Info: ícone encontrado: {svg_path}")
    return pixbuf
  
  if os.path.exists(png_path):
    return Gio.FileIcon.new(Gio.File.new_for_path(png_path))
  
  print(f"Warning: Nenhum ícone encontrado para: {preferred}")
  return None