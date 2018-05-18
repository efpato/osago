# -*- coding: utf-8 -*-

from page_object import PageObject
from page_object.ui.jquery import Button, Select, Textbox


class PolicyVehiclePage(PageObject):
    _NG_MODEL_DOC = ("[ng-model='vehicle.documents"
                     "[vehicle.currentDocumentType].{}']").format

    purpose = Select(css="select[ng-model='osagoPolicy.vehicle.purposeOfUse']")
    mark = Select(css="select[ng-model='vehicle.mark']")
    model = Select(css="select[ng-model='vehicle.model']")
    year = Textbox(css="input[ng-model='vehicle.year']")
    category = Select(css="select[ng-model='vehicle.category']")
    power = Textbox(css="input[ng-model='vehicle.power']")
    power_kw = Textbox(css="input[ng-model='vehicle.powerKw']")
    max_mass = Textbox(css="input[ng-model='vehicle.maxMass']")
    seats_count = Textbox(css="input[ng-model='vehicle.seatsCount']")
    doc_type = Select(css="select[ng-model='vehicle.currentDocumentType']")
    doc_series = Textbox(css=_NG_MODEL_DOC("series"))
    doc_number = Textbox(css=_NG_MODEL_DOC("number"))
    doc_date_of_issue = Textbox(css=_NG_MODEL_DOC("dateOfIssue"))
    reg_number = Textbox(css="input[ng-model='vehicle.regNumber']")
    vin = Textbox(css="input[ng-model='vehicle.vin']")
    inspection_card_number = Textbox(
        css="input[ng-model='osagoPolicy.vehicle.inspectionCard.number']")
    inspection_card_date = Textbox(
        css="input[ng-model='osagoPolicy.vehicle.inspectionCard.term']")
    prev_step = Button(css="button[ng-click='prevStep()']")
    next_step = Button(css="button[ng-click='nextStep()']")

    def with_trailer(self):
        el = Button(
            css="input[ng-model='osagoPolicy.vehicle.withTrailer']"
        ).__get__(self, self.__class__)
        el.click()
        el.click()

    def russia(self):
        el = Button(
            css="input[text='На территории РФ']"
        ).__get__(self, self.__class__)
        el.click()
        el.click()

    def registration(self):
        el = Button(
            css="input[text='Следует к месту регистрации']"
        ).__get__(self, self.__class__)
        el.click()
        el.click()

    def prev(self):
        from osago.ugsk.pages.policy_owner import PolicyOwnerPage

        self.prev_step.click()
        return PolicyOwnerPage(self.webdriver)

    def next(self):
        from osago.ugsk.pages.policy_drivers import PolicyDriversPage

        self.next_step.click()
        return PolicyDriversPage(self.webdriver)
