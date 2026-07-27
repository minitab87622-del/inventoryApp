# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from arabic import register_font
from database import Database

from screens.home import HomeScreen
from screens.items import ItemsScreen
from screens.imports import ImportsScreen
from screens.sales import SalesScreen
from screens.stock import StockScreen


Window.softinput_mode = "resize"
register_font()


class InventoryApp(App):
    def build(self):
        self.db = Database()
        self.root_box = BoxLayout()
        self.show_home()
        return self.root_box

    def change_screen(self, screen):
        self.root_box.clear_widgets()
        self.root_box.add_widget(screen)

    def show_home(self):
        self.change_screen(HomeScreen(self))

    def show_items(self):
        self.change_screen(ItemsScreen(self))

    def show_imports(self):
        self.change_screen(ImportsScreen(self))

    def show_sales(self):
        self.change_screen(SalesScreen(self))

    def show_stock(self):
        self.change_screen(StockScreen(self))


if __name__ == "__main__":
    InventoryApp().run()