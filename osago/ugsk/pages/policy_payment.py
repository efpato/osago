# -*- coding: utf-8 -*-

import logging

from page_object import PageObject
from page_object.ui.jquery import Button
from selenium.webdriver.support.wait import WebDriverWait


class PolicyPaymentPage(PageObject):
    redirect = Button(css="a[data-ng-click='selectionOsagoStartRedirect()']")
    prev_step = Button(css="button[ng-click='prevStep()']")

    def wait_for_rsa_check(self, timeout=300):
        logging.debug("Waiting for RSA check ...")
        WebDriverWait(self.webdriver, timeout).until_not(
            lambda d: d.find_elements_by_css_selector(
                "div[data-ng-bind='options.text']"),
            'Waiting for RSA check has expired')

    def confirm(self):
        el = Button(
            css=("input[data-ng-model="
                 "'rsaCheckResult.confirmSelectionPersonalData']")
        ).__get__(self, self.__class__)
        el.click()
        el.click()

    def prev(self):
        from osago.ugsk.pages.policy_extra import PolicyExtraPage

        self.prev_step.click()
        return PolicyExtraPage(self.webdriver)
