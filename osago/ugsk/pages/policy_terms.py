# -*- coding: utf-8 -*-

from page_object import PageObject
from page_object.ui.jquery import Button, Textbox


class PolicyTermsPage(PageObject):
    policy_date_start = Textbox(css="input[ng-model='osagoPolicy.dateStart']")
    policy_date_end = Textbox(css="input[ng-model='osagoPolicy.dateEnd']")
    period = Textbox(
        css="input[ng-model='osagoPolicy.periods[$index].period']")
    period_start = Textbox(
        css="input[ng-model='osagoPolicy.periods[$index].start']")
    period_end = Textbox(
        css="input[ng-model='osagoPolicy.periods[$index].end']")
    prev_step = Button(css="button[ng-click='prevStep()']")
    next_step = Button(css="button[ng-click='nextStep()']")

    def prev(self):
        from osago.ugsk.pages.policy_drivers import PolicyDriversPage

        self.prev_step.click()
        return PolicyDriversPage(self.webdriver)

    def next(self):
        from osago.ugsk.pages.policy_extra import PolicyExtraPage

        self.next_step.click()
        return PolicyExtraPage(self.webdriver)
