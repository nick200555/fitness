# Copyright (c) 2026, fitness_wellness and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MembershipInvoice(Document):
    def on_submit(self):
        from fitness_wellness.billing import create_sales_invoice
        create_sales_invoice(self)

    def before_save(self):
        self.balance_due = (self.total_amount or 0) - (self.paid_amount or 0)
        if self.balance_due <= 0:
            self.payment_status = "Paid"
        elif (self.paid_amount or 0) > 0:
            self.payment_status = "Partially Paid"

