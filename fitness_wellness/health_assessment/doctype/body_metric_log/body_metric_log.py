# Copyright (c) 2026, fitness_wellness and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BodyMetricLog(Document):
    def before_save(self):
        if self.weight_kg and self.weight_kg > 0:
            # Requires height from Health Profile
            hp = frappe.db.get_value("Health Profile", {"member": self.member}, "height_cm")
            if hp:
                height_m = hp / 100
                self.bmi = round(self.weight_kg / (height_m * height_m), 2)

