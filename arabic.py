# -*- coding: utf-8 -*-

from kivy.core.text import LabelBase
import arabic_reshaper


def register_font():

    LabelBase.register(
        name="Arabic",
        fn_regular="NotoNaskhArabic-Regular.ttf"
    )


def ar(text):

    if text is None:
        return ""

    return arabic_reshaper.reshape(
        str(text)
    )[::-1]