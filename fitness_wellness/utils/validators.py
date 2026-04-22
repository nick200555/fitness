# fitness_wellness/utils/validators.py
# Placeholder — validation utilities
import frappe


def validate_mobile(mobile):
    """Validate Indian mobile number format."""
    import re
    pattern = r"^[6-9]\d{9}$"
    if mobile and not re.match(pattern, mobile):
        frappe.throw("Invalid mobile number format.")


def validate_date_range(start_date, end_date):
    """Ensure end_date is after start_date."""
    if start_date and end_date and end_date < start_date:
        frappe.throw("End Date cannot be before Start Date.")
