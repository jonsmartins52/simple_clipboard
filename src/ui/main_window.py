import gi
from gi.repository import Gtk, Gdk

from src.ui.search_bar import SearchBar
from src.ui.history_list_view import HistoryListView
from src.ui.footer_bar import FooterBar
from src.ui.icon_loader import load_app_icon

class MainWindow(Gtk.Window):
    def __init__(self, controller, clipboard):
        super().__init__(title="Clipboard History")

        icon = load_app_icon("src/assets/icons/blink")
        if icon:
            self.set_icon(icon)

        self.set_default_size(600, 400)

        self.controller = controller
        self.clipboard = clipboard

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.vbox)

        self._load_css()
        self._build_ui()

    # -----------------------------------------------------
    # Montagem da UI
    # -----------------------------------------------------
    def _build_ui(self):
        # SEARCH BAR
        self.search_bar = SearchBar(self.controller.apply_query)
        self.vbox.pack_start(self.search_bar, False, False, 0)

        # LIST (HistoryListView)
        self.history_list = HistoryListView(
            on_item_selected=self._on_history_item_clicked
        )
        self.vbox.pack_start(self.history_list, True, True, 0)

        # FOOTER
        self.footer = FooterBar(self._on_clear_history)
        self.vbox.pack_start(self.footer, False, False, 0)        

    # -----------------------------------------------------
    # Copiar item selecionado
    # -----------------------------------------------------
    def _on_history_item_clicked(self, full_text: str):
        self.controller.clipboard_manager.suppress_next_copy_event = True
        self.clipboard.set_text(full_text, -1)

        try:
            self.clipboard.store()
        except Exception:
            pass

    # -----------------------------------------------------
    # Limpar histórico via diálogo
    # -----------------------------------------------------
    def _on_clear_history(self):
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
            self.search_bar.set_text("")

    def on_history_changed(self, filtered_items):
        self.history_list.render_items(filtered_items, self.controller.query)
    
    # -----------------------------------------------------
    # CSS
    # -----------------------------------------------------
    def _load_css(self):
        provider = Gtk.CssProvider()

        css_path = "src/ui/styles.css"

        try:
            provider.load_from_path(css_path)
        except Exception as e:
            print("Erro ao carregar css: ", e)
            return
        
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
