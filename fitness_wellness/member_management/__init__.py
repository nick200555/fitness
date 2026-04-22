# fitness_wellness/member_management/__init__.py
import frappe


def handle_subscription_cancel(doc, method=None):
    """Update Member status on subscription cancellation."""
    member_doc = frappe.get_doc("Member", doc.member)
    other_active = frappe.db.exists("Member Subscription", {
        "member": doc.member,
        "status": "Active",
        "name": ["!=", doc.name]
    })
    if not other_active:
        member_doc.db_set("status", "Cancelled")
