# Copyright (c) 2026, fitness_wellness and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SubscriptionFreeze(Document):
    def before_save(self):
        from frappe.utils import date_diff, add_days
        if self.freeze_from and self.freeze_to:
            self.days_frozen = date_diff(self.freeze_to, self.freeze_from)
            if self.member_subscription:
                current_end = frappe.db.get_value(
                    "Member Subscription", self.member_subscription, "end_date")
                if current_end:
                    self.new_end_date = add_days(current_end, self.days_frozen)

    def on_submit(self):
        if self.member_subscription and self.new_end_date:
            frappe.db.set_value("Member Subscription",
                                self.member_subscription, "end_date", self.new_end_date)
            frappe.db.set_value("Member Subscription",
                                self.member_subscription, "status", "Frozen")

