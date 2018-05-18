# -*- coding: utf-8 -*-

from page_object import PageObject
from page_object.ui import Button, Textbox


class LoginPage(PageObject):
    username = Textbox(name="USER_LOGIN")
    password = Textbox(name="USER_PASSWORD")
    submit = Button(name='Login')

    def login(self, username, password):
        from osago.ugsk.pages.policy_insurer import PolicyInsurerPage

        self.username = username
        self.password = password
        self.submit.click()
        self.wait_for_page_by_title("Выписать полис ОСАГО")
        return PolicyInsurerPage(self.webdriver)
