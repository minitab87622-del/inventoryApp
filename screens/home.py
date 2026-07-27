# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from arabic import ar


class HomeScreen(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=10,
            padding=10,
            **kwargs
        )

        self.app = app


        title = Label(
            text=ar("نظام مراقبة المخزون"),
            font_name="Arabic",
            size_hint_y=None,
            height=60
        )

        self.add_widget(title)



        self.add_widget(
            self.create_button(
                "الأصناف",
                self.open_items
            )
        )


        self.add_widget(
            self.create_button(
               "الوارد )المستورد (",
                self.open_imports
            )
        )


        self.add_widget(
            self.create_button(
                "المبيعات",
                self.open_sales
            )
        )


        self.add_widget(
            self.create_button(
                "المخزون الحالي",
                self.open_stock
            )
        )



    def create_button(self, text, function):

        btn = Button(
            text=ar(text),
            font_name="Arabic",
            size_hint_y=None,
            height=60
        )

        btn.bind(
            on_press=function
        )

        return btn



    def open_items(self, btn):
        self.app.show_items()



    def open_imports(self, btn):
        self.app.show_imports()



    def open_sales(self, btn):
        self.app.show_sales()



    def open_stock(self, btn):
        self.app.show_stock()