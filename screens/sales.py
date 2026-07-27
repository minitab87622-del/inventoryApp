# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.clock import Clock

from arabic import ar
from database import normalize_digits


class SalesScreen(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=10,
            padding=10,
            **kwargs
        )

        self.app = app
        self.boxes = {}
        self.scroll = None

        title = Label(
            text=ar("تسجيل المبيعات"),
            font_name="Arabic",
            size_hint_y=None,
            height=50,
            halign="right",
            valign="middle"
        )
        title.bind(size=title.setter("text_size"))
        self.add_widget(title)

        top_bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=55,
            spacing=10
        )

        save_btn = Button(
            text=ar("حفظ المبيعات"),
            font_name="Arabic"
        )
        save_btn.bind(on_press=self.save_sales)

        back_btn = Button(
            text=ar("رجوع"),
            font_name="Arabic"
        )
        back_btn.bind(on_press=lambda x: self.app.show_home())

        top_bar.add_widget(save_btn)
        top_bar.add_widget(back_btn)
        self.add_widget(top_bar)

        self.container = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None,
            padding=[0, 0, 0, dp(260)]
        )
        self.container.bind(minimum_height=self.container.setter("height"))

        items = self.app.db.get_items()

        if not items:
            empty = Label(
                text=ar("لا توجد أصناف بعد"),
                font_name="Arabic",
                size_hint_y=None,
                height=50,
                halign="right",
                valign="middle"
            )
            empty.bind(size=empty.setter("text_size"))
            self.container.add_widget(empty)

        for item in items:
            row = BoxLayout(
                size_hint_y=None,
                height=60,
                spacing=10
            )

            name = Label(
                text=ar(item[0]),
                font_name="Arabic",
                halign="right",
                valign="middle"
            )
            name.bind(size=name.setter("text_size"))

            amount = TextInput(
                hint_text=ar("الكمية المباعة"),
                font_name="Arabic",
                multiline=False,
                write_tab=False,
                halign="right"
            )
            amount.bind(focus=self.on_focus_field)

            self.boxes[item[0]] = amount

            row.add_widget(name)
            row.add_widget(amount)
            self.container.add_widget(row)

        self.container.add_widget(Widget(size_hint_y=None, height=dp(40)))

        self.scroll = ScrollView(
            size_hint_y=1,
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=0
        )
        self.scroll.add_widget(self.container)
        self.add_widget(self.scroll)

    def on_focus_field(self, field, focused):
        if focused and self.scroll:
            Clock.schedule_once(
                lambda dt: self.scroll.scroll_to(
                    field,
                    padding=dp(120),
                    animate=True
                ),
                0.05
            )

    def save_sales(self, btn):
        any_saved = False

        for name, box in self.boxes.items():
            raw = normalize_digits(box.text.strip())
            try:
                amount = int(raw) if raw else 0
            except:
                amount = 0

            if amount > 0:
                if self.app.db.add_sale(name, amount):
                    any_saved = True

        self.app.show_stock()