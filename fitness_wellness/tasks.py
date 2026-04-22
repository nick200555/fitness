# fitness_wellness/tasks.py
import frappe
from frappe.utils import today, add_days, nowdate


def send_membership_expiry_reminders():
    """Send reminder to members whose subscription expires in 7 or 1 day."""
    for days in [7, 1]:
        target_date = add_days(today(), days)
        subs = frappe.get_all("Member Subscription",
            filters={"end_date": target_date, "status": "Active"},
            fields=["name", "member"])
        for sub in subs:
            member = frappe.get_doc("Member", sub.member)
            frappe.sendmail(
                recipients=[member.email],
                subject=f"Membership Expiry Reminder — {days} day(s) left",
                message=f"Dear {member.full_name}, your membership expires on {target_date}. Please renew to continue enjoying our facilities."
            )


def auto_generate_monthly_invoices():
    """Auto-generate invoices for active subscriptions (placeholder)."""
    pass


def check_equipment_maintenance_due():
    """Flag equipment where next_service_due <= today."""
    due = frappe.get_all("Equipment Register",
        filters={"next_service_due": ["<=", today()], "status": "Operational"},
        fields=["name", "equipment_name"])
    for eq in due:
        frappe.get_doc({
            "doctype": "Maintenance Log",
            "equipment": eq.name,
            "maintenance_date": today(),
            "maintenance_type": "Preventive",
            "work_done": "Auto-flagged for scheduled maintenance",
            "status": "Pending Follow-Up"
        }).insert(ignore_permissions=True)


def mark_absent_unbooked_members():
    """Placeholder — marks absent for unbooked class slots."""
    pass


def generate_trainer_commission_vouchers():
    """Auto-generate Trainer Commission records for active trainers."""
    from frappe.utils import get_first_day, get_last_day, add_months
    import datetime
    period_to = frappe.utils.getdate(today())
    period_from = get_first_day(period_to)
    period_to_date = get_last_day(period_to)
    trainers = frappe.get_all("Trainer Profile", filters={"status": "Active"}, fields=["name"])
    for t in trainers:
        exists = frappe.db.exists("Trainer Commission", {
            "trainer": t.name,
            "period_from": period_from,
            "period_to": period_to_date
        })
        if not exists:
            doc = frappe.get_doc({
                "doctype": "Trainer Commission",
                "trainer": t.name,
                "period_from": str(period_from),
                "period_to": str(period_to_date)
            })
            doc.insert(ignore_permissions=True)


def send_weekly_progress_reports():
    """Placeholder — send weekly progress reports to members."""
    pass


def process_emi_deductions():
    """Placeholder — trigger EMI deduction reminders for due instalments."""
    pass
