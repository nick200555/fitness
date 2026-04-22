# fitness_wellness/class_management/__init__.py
import frappe


def update_class_capacity(doc, method=None):
    """Decrement available capacity on Class Schedule when enrollment is submitted."""
    enrolled_count = frappe.db.count("Class Enrollment", {
        "class_schedule": doc.class_schedule,
        "session_date": doc.session_date,
        "status": ["in", ["Confirmed", "Waitlisted"]]
    })
    schedule = frappe.get_doc("Class Schedule", doc.class_schedule)
    if enrolled_count > (schedule.max_capacity or 0):
        if schedule.waitlist_enabled:
            doc.db_set("status", "Waitlisted")
        else:
            frappe.throw(f"Class {doc.class_schedule} is fully booked.")
