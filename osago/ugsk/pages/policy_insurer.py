# -*- coding: utf-8 -*-

from page_object import PageObject
from page_object.ui.jquery import Button, Select, Textbox

from osago.ugsk.pages.ui import AutocompleteTextbox


class PolicyInsurerPage(PageObject):
    _NG_MODEL = "[ng-model='contractor.{}']".format
    _NG_MODEL_DOC = "[ng-model='contractor.document.{}']".format

    lastname = Textbox(css=_NG_MODEL('lastname'))
    firstname = Textbox(css=_NG_MODEL('name'))
    middlename = Textbox(css=_NG_MODEL('middlename'))
    birthday = Textbox(css=_NG_MODEL('birthday'))
    doc_type = Select(css=_NG_MODEL('documentType'))
    doc_series = Textbox(css=_NG_MODEL_DOC('series'))
    doc_number = Textbox(css=_NG_MODEL_DOC('number'))
    phone = Textbox(css=_NG_MODEL('telephones.mobile'))
    registration_address = AutocompleteTextbox(
        css=_NG_MODEL('registrationAddress'))
    flat_number = Textbox(css=_NG_MODEL('registrationAddressFlatNumber'))
    next_step = Button(css="button[ng-show='next_step']")

    def confirm(self):
        el = Button(
            css="input[ng-model='processPersonalDataConfirm.value']"
        ).__get__(self, self.__class__)
        el.click()
        el.click()

    def next(self):
        from osago.ugsk.pages.policy_owner import PolicyOwnerPage

        self.next_step.click()
        return PolicyOwnerPage(self.webdriver)
