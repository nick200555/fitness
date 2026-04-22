# fitness_wellness/billing/__init__.py
import frappe
from frappe.utils import today


def auto_create_membership_invoice(doc, method=None):
    """Create Membership Invoice when Member Subscription is submitted."""
    if frappe.db.exists("Membership Invoice", {"subscription": doc.name}):
        return
    plan_doc = frappe.get_doc("Membership Plan", doc.plan)
    inv = frappe.get_doc({
        "doctype": "Membership Invoice",
        "member": doc.member,
        "subscription": doc.name,
        "invoice_date": today(),
        "due_date": today(),
        "plan_amount": plan_doc.price,
        "discount_amount": doc.discount_amount or 0,
        "taxable_amount": (plan_doc.price - (doc.discount_amount or 0)),
        "gst_amount": 0,
        "total_amount": doc.actual_amount or plan_doc.price,
        "paid_amount": 0,
        "balance_due": doc.actual_amount or plan_doc.price,
        "payment_status": "Unpaid"
    })
    inv.insert(ignore_permissions=True)
    doc.db_set("membership_invoice", inv.name)


def create_sales_invoice(doc, method=None):
    """Create ERPNext Sales Invoice from Membership Invoice on submit."""
    if doc.sales_invoice:
        return
    member_doc = frappe.get_doc("Member", doc.member)
    if not member_doc.customer:
        return
    si = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": member_doc.customer,
        "posting_date": doc.invoice_date or today(),
        "due_date": doc.due_date or today(),
        "items": [{
            "item_code": "Membership Fee",
            "qty": 1,
            "rate": doc.total_amount,
            "description": f"Membership Invoice {doc.name}"
        }]
    })
    si.insert(ignore_permissions=True)
    doc.db_set("sales_invoice", si.name)
