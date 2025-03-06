# -*- coding: utf-8 -*-
# Copyright (c) 2023, InsureEase and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.utils import now_datetime

@frappe.whitelist(allow_guest=True)
def create_insurance_application(data=None):
    """
    Create a new insurance application from frontend form data
    """
    if not data:
        return {"status": "error", "message": "No data provided"}
    
    if isinstance(data, str):
        data = json.loads(data)
    
    try:
        # Map frontend form data to Frappe doctype fields
        application = frappe.new_doc("Insurance Application")
        
        # Personal Information
        application.first_name = data.get("firstName")
        application.last_name = data.get("lastName")
        application.email = data.get("email")
        application.phone = data.get("phone")
        application.date_of_birth = data.get("dateOfBirth")
        application.address = data.get("address")
        application.city = data.get("city")
        application.postal_code = data.get("postalCode")
        
        # Identification
        id_type_map = {
            "national_id": "National ID",
            "passport": "Passport",
            "drivers_license": "Driver's License"
        }
        application.id_type = id_type_map.get(data.get("idType"), "National ID")
        application.id_number = data.get("idNumber")
        
        # Banking Details
        application.account_holder = data.get("accountHolder")
        application.bank_name = data.get("bankName")
        application.account_number = data.get("accountNumber")
        application.branch_code = data.get("branchCode")
        
        account_type_map = {
            "savings": "Savings",
            "checking": "Checking",
            "current": "Current"
        }
        application.account_type = account_type_map.get(data.get("accountType"), "Savings")
        
        # Package Details
        package_type_map = {
            "basic": "Basic Coverage",
            "standard": "Standard Coverage",
            "premium": "Premium Coverage"
        }
        application.package_type = package_type_map.get(data.get("packageType"), "Basic Coverage")
        
        coverage_amount_map = {
            "coverage_50k": "$50,000",
            "coverage_100k": "$100,000",
            "coverage_250k": "$250,000",
            "coverage_500k": "$500,000",
            "coverage_1m": "$1,000,000"
        }
        application.coverage_amount = coverage_amount_map.get(data.get("coverageAmount"), "$50,000")
        
        # Additional Options
        additional_options = data.get("additionalOptions", [])
        option_map = {
            "critical_illness": "Critical Illness Cover",
            "disability": "Disability Cover",
            "funeral": "Funeral Cover",
            "income_protection": "Income Protection"
        }
        
        for option_id in additional_options:
            option_name = option_map.get(option_id)
            if option_name:
                option = application.append("additional_options", {})
                option.option_name = option_name
                
                # Set default premium values
                premium_map = {
                    "critical_illness": 15,
                    "disability": 12,
                    "funeral": 8,
                    "income_protection": 20
                }
                option.monthly_premium = premium_map.get(option_id, 10)
        
        # Status
        application.application_status = "Pending"
        application.application_date = now_datetime().date()
        
        application.insert(ignore_permissions=True)
        
        return {
            "status": "success",
            "message": "Application submitted successfully",
            "application_id": application.name
        }
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Insurance Application Creation Error"))
        return {
            "status": "error",
            "message": "An error occurred while processing your application: {}".format(str(e))
        }

@frappe.whitelist(allow_guest=True)
def get_insurance_packages():
    """
    Get available insurance packages
    """
    packages = [
        {
            "id": "basic",
            "name": "Basic Coverage",
            "price": 29.99,
            "description": "Essential coverage for individuals"
        },
        {
            "id": "standard",
            "name": "Standard Coverage",
            "price": 49.99,
            "description": "Comprehensive coverage with additional benefits"
        },
        {
            "id": "premium",
            "name": "Premium Coverage",
            "price": 79.99,
            "description": "Complete coverage with premium benefits and priority service"
        }
    ]
    
    coverage_options = [
        {"id": "coverage_50k", "amount": "$50,000"},
        {"id": "coverage_100k", "amount": "$100,000"},
        {"id": "coverage_250k", "amount": "$250,000"},
        {"id": "coverage_500k", "amount": "$500,000"},
        {"id": "coverage_1m", "amount": "$1,000,000"}
    ]
    
    additional_options = [
        {"id": "critical_illness", "name": "Critical Illness Cover", "price": 15},
        {"id": "disability", "name": "Disability Cover", "price": 12},
        {"id": "funeral", "name": "Funeral Cover", "price": 8},
        {"id": "income_protection", "name": "Income Protection", "price": 20}
    ]
    
    return {
        "packages": packages,
        "coverage_options": coverage_options,
        "additional_options": additional_options
    }

@frappe.whitelist()
def get_application_status(application_id):
    """
    Get the status of an insurance application
    """
    if not application_id:
        return {"status": "error", "message": "No application ID provided"}
    
    try:
        application = frappe.get_doc("Insurance Application", application_id)
        return {
            "status": "success",
            "application_status": application.application_status,
            "application_date": application.application_date,
            "applicant_name": f"{application.first_name} {application.last_name}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error retrieving application: {str(e)}"
        }