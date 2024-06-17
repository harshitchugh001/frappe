# Copyright (c) 2024, demo and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta
from datetime import datetime



class Program(Document):
	pass

	def validate(self):
		
		if self.start_date>=self.end_date:
			frappe.throw("Start date must be before end date")
		start_date = datetime.strptime(self.start_date,'%Y-%m-%d')
		print(start_date)
		end_date = datetime.strptime(self.end_date,'%Y-%m-%d')
		print(end_date)
		self.duration = self.calculate_duration(start_date, end_date)
		self.total_credits=self.calculate_total_credits()

	def calculate_duration(self, start_date, end_date):
		delta= relativedelta(end_date,start_date)
		months=delta.years*12+delta.months+delta.days/30.0
		return round(months,2)

	def calculate_total_credits(self):
		total_credits = 0.0
		for co in self.courses:
			print(co)
			course_doc = frappe.get_doc("course",co).credits
			print("doc",course_doc)
			print("credit",course_doc)
			print(course_doc)
			credits = float(course_doc)
			total_credits+=credits
		return total_credits
		



        
		

    



	
        
