# Copyright (c) 2026, fitness_wellness and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ClassEnrollment(Document):
    def on_submit(self):
        from fitness_wellness.class_management import update_class_capacity
        update_class_capacity(self)
        # Deduct class credit if chargeable
        ct = frappe.db.get_value("Class Schedule", self.class_schedule, "class_type")
        if ct:
            is_chargeable = frappe.db.get_value("Class Type", ct, "is_chargeable")
            if is_chargeable and self.member:
                sub = frappe.db.get_value("Member Subscription",
                    {"member": self.member, "status": "Active"}, "name")
                if sub:
                    sub_doc = frappe.get_doc("Member Subscription", sub)
                    if sub_doc.class_credits_remaining > 0:
                        sub_doc.db_set("class_credits_remaining",
                                       sub_doc.class_credits_remaining - 1)
                        self.db_set("credit_deducted", 1)

