# -*- coding: utf-8 -*-

import logging
import time

from page_object import PageElement, PageElementWrapper

__all__ = ['AutocompleteTextbox', 'AutocompleteTextboxWrapper']


class AutocompleteTextboxWrapper(PageElementWrapper):
    """ JQuery wrapper for <input type="text" autocomplete>"""

    @property
    def value(self):
        return self._el.parent.execute_script(
            'return $("{}").val();'.format(self._locator[1]))

    def enter_text(self, text, timeout=3):
        logging.info("%s entering text ...", self)
        self._el.parent.execute_script(
            """
            $("{0}:visible").val("{1}").change();
            setTimeout(function () {{
                $("{0}:visible ~ ul li").first().click();
            }}, {2});
            """.format(self._locator[1], text, timeout * 1000))
        time.sleep(timeout + .1)


class AutocompleteTextbox(PageElement):
    """ AutocompleteTextbox descriptor"""

    def __get__(self, instance, owner):
        return AutocompleteTextboxWrapper(
            self.find(instance.webdriver), self._locator)

    def __set__(self, instance, value):
        if value is None:
            return

        value = str(value).strip()
        if not value:
            return

        self.__get__(instance, instance.__class__).enter_text(value)
