# Copyright (c) 2025, Cohenix and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class InsuranceApplication(Document):
    def validate(self):
        self.validate_email()
        self.validate_id_number()
        self.validate_account_number()
    
    def validate_email(self):
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            frappe.throw("Please enter a valid email address")
    
    def validate_id_number(self):
        # Basic validation based on ID type
        if self.id_type == "National ID" and len(self.id_number) < 6:
            frappe.throw("National ID number must be at least 6 characters")
        elif self.id_type == "Passport" and len(self.id_number) < 6:
            frappe.throw("Passport number must be at least 6 characters")
        elif self.id_type == "Driver's License" and len(self.id_number) < 6:
            frappe.throw("Driver's License number must be at least 6 characters")
    
    def validate_account_number(self):
        # Basic validation for account number
        if not self.account_number.isdigit():
            frappe.throw("Account number must contain only digits")
        if len(self.account_number) < 8:
            frappe.throw("Account number must be at least 8 digits")
    
    def on_submit(self):
        # Send email notification
        self.send_application_notification()
    
    def send_application_notification(self):
        subject = "Insurance Application Received - {0}".format(self.name)
        message = """
        <p>Dear {0} {1},</p>
        <p>Thank you for submitting your insurance application with InsureEase.</p>
        <p>Your application reference number is: <strong>{2}</strong></p>
        <p>We will review your application and get back to you shortly.</p>
        <p>Regards,<br>InsureEase Team</p>
        """.format(self.first_name, self.last_name, self.name)
        
        try:
            frappe.sendmail(
                recipients=[self.email],
                subject=subject,
                message=message
            )
        except Exception as e:
            frappe.log_error("Failed to send email notification: {0}".format(str(e)), "Insurance Application Email")