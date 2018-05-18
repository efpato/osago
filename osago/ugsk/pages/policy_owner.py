# -*- coding: utf-8 -*-

import logging

from page_object import PageObject
from page_object.ui.jquery import Button, Select, Textbox
from selenium.webdriver.support.wait import WebDriverWait

from osago.ugsk.pages.ui import AutocompleteTextbox


class PolicyOwnerPage(PageObject):
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
    prev_step = Button(css="button[ng-click='prevStep()']")
    next_step = Button(css="button[ng-click='nextStep()']")

    def wait_for_load(self, timeout=60):
        logging.debug("Waiting for loader ...")
        WebDriverWait(self.webdriver, timeout).until_not(
            lambda d: d.find_element_by_css_selector(
                "center[data-ng-if='isLoadFormOsago']"),
            'Waiting for loader has expired!')

    def owner_is_insurer(self):
        el = Button(css="input[text='Является страхователем']").__get__(
            self, self.__class__)
        el.click()
        el.click()

    def prev(self):
        from osago.ugsk.pages.policy_insurer import PolicyInsurerPage

        self.prev_step.click()
        return PolicyInsurerPage(self.webdriver)

    def next(self):
        from osago.ugsk.pages.policy_vehicle import PolicyVehiclePage

        self.next_step.click()
        return PolicyVehiclePage(self.webdriver)
