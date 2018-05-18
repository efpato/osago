# -*- coding: utf-8 -*-

from page_object import PageObject
from page_object.ui.jquery import Button, Textbox


class PolicyDriversPage(PageObject):
    _NG_MODEL = "input.ng-empty[ng-model='driver.{}']".format
    _NG_MODEL_DOC = "input.ng-empty[ng-model='driver.document.{}']".format

    lastname = Textbox(css=_NG_MODEL("lastname"))
    firstname = Textbox(css=_NG_MODEL("name"))
    middlename = Textbox(css=_NG_MODEL("middlename"))
    birthday = Textbox(css=_NG_MODEL("birthday"))
    doc_series = Textbox(css=_NG_MODEL_DOC("series"))
    doc_number = Textbox(css=_NG_MODEL_DOC("number"))
    experience_from = Textbox(css=_NG_MODEL_DOC("experienceFrom"))
    add_driver = Button(css="a[ng-click='addDriver()']")
    prev_step = Button(css="button[ng-click='prevStep()']")
    next_step = Button(css="button[ng-click='nextStep()']")

    def multidrive(self, yes):
        if yes:
            el = Button(css="#multidrive_Y").__get__(self, self.__class__)
        else:
            el = Button(css="#multidrive_N").__get__(self, self.__class__)
        el.click()
        el.click()

    def prev(self):
        from osago.ugsk.pages.policy_vehicle import PolicyVehiclePage

        self.prev_step.click()
        return PolicyVehiclePage(self.webdriver)

    def next(self):
        from osago.ugsk.pages.policy_terms import PolicyTermsPage

        self.next_step.click()
        return PolicyTermsPage(self.webdriver)
