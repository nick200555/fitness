# fitness_wellness/utils/calculations.py
import frappe
from frappe.utils import flt, date_diff, add_months, today


def calculate_prorated_amount(plan_price, start_date, billing_day=1):
    """
    Calculate prorated amount when subscription starts mid-cycle.
    Returns full amount if starting on or before billing day.
    """
    from datetime import date
    start = frappe.utils.getdate(start_date)
    days_in_month = 30
    if start.day <= billing_day:
        return flt(plan_price)
    days_remaining = days_in_month - start.day + billing_day
    return flt(plan_price * days_remaining / days_in_month)


def generate_emi_schedule(subscription_name, total_amount, no_of_instalments, start_date):
    """
    Generate EMI instalment rows for a given subscription.
    Called via hooks on Member Subscription submit when payment_mode == 'EMI'.
    """
    instalment_amount = flt(total_amount / no_of_instalments, 2)
    schedule = []
    for i in range(no_of_instalments):
        due_date = add_months(start_date, i)
        schedule.append({
            "instalment_no": i + 1,
            "due_date": due_date,
            "amount": instalment_amount,
            "status": "Pending",
            "payment_reference": ""
        })
    # Adjust last instalment for rounding difference
    collected = instalment_amount * (no_of_instalments - 1)
    schedule[-1]["amount"] = flt(total_amount - collected, 2)
    return schedule


def calculate_trainer_commission(trainer, period_from, period_to):
    """
    Sum commission-eligible sessions for a trainer in the period.
    """
    trainer_doc = frappe.get_doc("Trainer Profile", trainer)
    # Count group sessions
    group_sessions = frappe.db.count("Class Attendance",
        filters={"trainer": trainer,
                 "session_date": ["between", [period_from, period_to]]})
    # Count PT sessions
    pt_sessions = frappe.db.count("Trainer Assignment",
        filters={"trainer": trainer,
                 "session_date": ["between", [period_from, period_to]]})
    if trainer_doc.commission_type == "Per Session":
        gross = (group_sessions + pt_sessions) * flt(trainer_doc.commission_rate)
    else:
        gross = flt(trainer_doc.commission_rate)
    tds = flt(gross * 0.10)  # 10% TDS
    return {
        "gross_commission": gross,
        "tds_deducted": tds,
        "net_payable": gross - tds,
        "group_sessions_taken": group_sessions,
        "pt_sessions_taken": pt_sessions
    }
