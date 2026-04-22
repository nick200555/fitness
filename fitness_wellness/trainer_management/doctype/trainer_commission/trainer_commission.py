# Copyright (c) 2026, fitness_wellness and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TrainerCommission(Document):
    def before_save(self):
        from fitness_wellness.utils.calculations import calculate_trainer_commission
        if self.trainer and self.period_from and self.period_to:
            result = calculate_trainer_commission(
                self.trainer, self.period_from, self.period_to
            )
            self.group_sessions_taken = result["group_sessions_taken"]
            self.pt_sessions_taken    = result["pt_sessions_taken"]
            self.gross_commission     = result["gross_commission"]
            self.tds_deducted         = result["tds_deducted"]
            self.net_payable          = result["net_payable"]

    def on_submit(self):
        je = frappe.get_doc({
            "doctype": "Journal Entry",
            "voucher_type": "Journal Entry",
            "posting_date": self.period_to,
            "accounts": [
                {"account": frappe.db.get_single_value(
                    "Accounts Settings", "commission_expense_account") or
                    "Commission Expense - FW",
                 "debit_in_account_currency": self.net_payable},
                {"account": frappe.db.get_single_value(
                    "Accounts Settings", "default_payable_account") or
                    "Creditors - FW",
                 "credit_in_account_currency": self.net_payable},
            ],
            "remark": f"Trainer commission for {self.trainer} ({self.period_from} to {self.period_to})"
        })
        je.insert(ignore_permissions=True)
        je.submit()
        self.db_set("journal_entry", je.name)

