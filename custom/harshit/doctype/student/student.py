# Copyright (c) 2024, demo and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
import re
from datetime import datetime
# class Student(Document):
#   pass
class Student(Document):
   
    def validate(self):
        self.full_name = f"{self.first_name} {self.middle_name or '' } {self.last_name}"  
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            frappe.throw("Invalid email address format. Please enter a valid email address.")
        self.validate_date_of_birth_dob()



    def validate_date_of_birth_dob(self):
        if self.date_of_birth_dob:
            dob = datetime.strptime(self.date_of_birth_dob, '%Y-%m-%d').date()
            today = datetime.today().date()
            max_allowed_date = datetime.strptime('2023-12-31','%Y-%m-%d').date()
            if dob > max_allowed_date:
                frappe.throw("DAte of Birth cannot be greater than 2023-12-31")
            if dob > today:
                frappe.throw("Date of Birth cannot be in the future.")


    # def before_load(self):
    #     if not self.joining_date:
    #         self.joining_date=datetime.today().date()
