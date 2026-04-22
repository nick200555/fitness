# fitness_wellness/utils/notifications.py
# Placeholder — SMS / email trigger utilities
import frappe


def send_sms(mobile, message):
    """Placeholder for SMS integration."""
    pass


def send_email_notification(email, subject, message):
    """Send email notification via Frappe."""
    frappe.sendmail(recipients=[email], subject=subject, message=message)
