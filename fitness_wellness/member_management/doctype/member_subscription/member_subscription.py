# Copyright (c) 2026, fitness_wellness and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MemberSubscription(Document):
    def before_save(self):
        from fitness_wellness.utils.calculations import calculate_prorated_amount
        if self.plan and self.start_date:
            plan_doc = frappe.get_doc("Membership Plan", self.plan)
            from frappe.utils import add_months
            self.end_date = add_months(self.start_date, plan_doc.duration_months)
            if not self.actual_amount:
                self.actual_amount = calculate_prorated_amount(
                    plan_doc.price, self.start_date
                )
            self.class_credits_remaining = plan_doc.class_credits
            self.pt_sessions_remaining = plan_doc.personal_training_sessions

    def on_submit(self):
        from fitness_wellness.billing import auto_create_membership_invoice
        auto_create_membership_invoice(self)
        if self.payment_mode == "EMI" and self.emi_months:
            from fitness_wellness.utils.calculations import generate_emi_schedule
            generate_emi_schedule(self.name, self.actual_amount,
                                  self.emi_months, self.start_date)

    def on_cancel(self):
        from fitness_wellness.member_management import handle_subscription_cancel
        handle_subscription_cancel(self)

