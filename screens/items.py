# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from arabic import ar


class ItemsScreen(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=10,
            padding=10,
            **kwargs
        )

        self.app = app

        title = Label(
            text=ar("إدارة الأصناف"),
            font_name="Arabic",
            size_hint_y=None,
            height=50,
            halign="right",
            valign="middle"
        )
        title.bind(size=title.setter("text_size"))
        self.add_widget(title)

        self.input = TextInput(
            hint_text=ar("اكتب اسم الصنف"),
            font_name="Arabic",
            multiline=False,
            size_hint_y=None,
            height=55
        )
        self.add_widget(self.input)

        add_btn = Button(
            text=ar("إضافة صنف"),
            font_name="Arabic",
            size_hint_y=None,
            height=55
        )
        add_btn.bind(on_press=self.add_item)
        self.add_widget(add_btn)

        self.label = Label(
            font_name="Arabic",
            markup=True,
            size_hint_y=None,
            halign="right",
            valign="top"
        )
        self.label.bind(texture_size=self.update_height)
        self.label.bind(size=self.update_text_size)

        scroll = ScrollView()
        scroll.add_widget(self.label)
        self.add_widget(scroll)

        back = Button(
            text=ar("الرجوع للرئيسية"),
            font_name="Arabic",
            size_hint_y=None,
            height=55
        )
        back.bind(on_press=lambda x: self.app.show_home())
        self.add_widget(back)

        self.refresh()

    def update_text_size(self, *args):
        self.label.text_size = (self.label.width, None)

    def update_height(self, *args):
        self.label.height = self.label.texture_size[1] + 20

    def add_item(self, btn):
        name = self.input.text.strip()
        if name:
            self.app.db.add_item(name)
            self.input.text = ""
            self.refresh()

    def refresh(self):
        data = self.app.db.get_items()

        txt = "[b]" + ar("قائمة الأصناف") + "[/b]\n\n"

        for i, item in enumerate(data, start=1):
            txt += (
                str(i) + " - " + ar(item[0]) + "\n"
                + ar("الكمية الحالية") + " : " + str(item[1]) + "\n"
                + "________________________________\n\n"
            )

        self.label.text = txt