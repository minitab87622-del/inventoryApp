# -*- coding: utf-8 -*-
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.metrics import dp

from arabic import ar


class StatusDot(Widget):
    def __init__(self, color=(0, 1, 0, 1), **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(16), dp(16)), **kwargs)
        self.dot_color = color
        self.bind(pos=self._redraw, size=self._redraw)
        with self.canvas:
            self._color = Color(*self.dot_color)
            self._ellipse = Ellipse(pos=self.pos, size=self.size)

    def _redraw(self, *args):
        self._color.rgba = self.dot_color
        self._ellipse.pos = self.pos
        self._ellipse.size = self.size


class StockScreen(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=10,
            padding=10,
            **kwargs
        )

        self.app = app

        title = Label(
            text=ar("المخزون الحالي"),
            font_name="Arabic",
            size_hint_y=None,
            height=55,
            halign="right",
            valign="middle"
        )
        title.bind(size=title.setter("text_size"))
        self.add_widget(title)

        back = Button(
            text=ar("رجوع"),
            font_name="Arabic",
            size_hint_y=None,
            height=55
        )
        back.bind(on_press=lambda x: self.app.show_home())
        self.add_widget(back)

        scroll = ScrollView(do_scroll_x=False, bar_width=0)

        container = BoxLayout(
            orientation="vertical",
            spacing=12,
            size_hint_y=None,
            padding=[0, 0, 0, dp(10)]
        )
        container.bind(minimum_height=container.setter("height"))

        data = self.app.db.get_stock_report()

        if not data:
            empty = Label(
                text=ar("لا توجد بيانات مخزون بعد"),
                font_name="Arabic",
                size_hint_y=None,
                height=60,
                halign="right",
                valign="middle"
            )
            empty.bind(size=empty.setter("text_size"))
            container.add_widget(empty)

        for i, item in enumerate(data, start=1):
            name = item["name"]
            quantity = int(item["quantity"])
            imported = int(item["imported"])
            sold = int(item["sold"])

            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(165),
                padding=dp(12),
                spacing=dp(6)
            )

            with card.canvas.before:
                Color(0.97, 0.97, 0.97, 1)
                self._bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(14)])
            card.bind(pos=self._update_card_bg, size=self._update_card_bg)

            top_row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(28),
                spacing=dp(8)
            )

            dot = StatusDot(color=self.get_status_color(quantity))
            top_row.add_widget(dot)

            name_label = Label(
                text=str(i) + " - " + ar(name),
                font_name="Arabic",
                color=(0, 0, 0, 1),
                halign="right",
                valign="middle"
            )
            name_label.bind(size=name_label.setter("text_size"))
            top_row.add_widget(name_label)

            card.add_widget(top_row)

            # استخدام دالة make_line الموحدة لجميع السطور لضمان المحاذاة التامة
            card.add_widget(self.make_line(ar("إجمالي الوارد"), str(imported), is_bold=False))
            card.add_widget(self.make_line(ar("إجمالي المبيعات"), str(sold), is_bold=False))
            card.add_widget(self.make_line(ar("الكمية الحالية"), str(quantity), is_bold=True))

            container.add_widget(card)

        scroll.add_widget(container)
        self.add_widget(scroll)

    def _update_card_bg(self, card, *args):
        for instr in card.canvas.before.children:
            if isinstance(instr, RoundedRectangle):
                instr.pos = card.pos
                instr.size = card.size

    def make_line(self, label_text, value_text, is_bold=False):
        row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(28),
            spacing=dp(8)
        )

        # النص يمين بنسبة 0.7
        lbl = Label(
            text=label_text,
            font_name="Arabic",
            color=(0, 0, 0, 1),
            halign="right",
            valign="middle",
            size_hint_x=0.7,
            bold=is_bold
        )
        lbl.bind(size=lbl.setter("text_size"))

        # العدد يسار بنسبة 0.3 لضمان استقامة الأرقام تحت بعضها
        val = Label(
            text=value_text,
            font_name="Arabic",
            color=(0, 0, 0, 1),
            halign="left",
            valign="middle",
            size_hint_x=0.3,
            bold=is_bold
        )
        val.bind(size=val.setter("text_size"))

        row.add_widget(lbl)
        row.add_widget(val)
        return row

    def get_status_color(self, quantity):
        if quantity >= 50:
            return (0.1, 0.7, 0.2, 1)   # أخضر
        elif quantity >= 20:
            return (0.95, 0.75, 0.15, 1) # أصفر
        elif quantity > 5:
            return (1.0, 0.55, 0.1, 1)   # برتقالي
        else:
            return (0.9, 0.15, 0.15, 1)  # أحمر
