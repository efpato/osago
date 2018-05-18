# -*- coding: utf-8 -*-

from page_object import PageObject
from page_object.ui.jquery import Button


class PolicyExtraPage(PageObject):
    prev_step = Button(css="button[ng-click='prevStep()']")
    next_step = Button(css="button[ng-click='nextStep()']")

    def delivery_electronically(self):
        el = Button(css="input[text='Электронно']").__get__(
            self, self.__class__)
        el.click()
        el.click()

    def prev(self):
        from osago.ugsk.pages.policy_terms import PolicyTermsPage

        self.prev_step.click()
        return PolicyTermsPage(self.webdriver)

    def next(self):
        from osago.ugsk.pages.policy_payment import PolicyPaymentPage

        self.next_step.click()
        return PolicyPaymentPage(self.webdriver)
