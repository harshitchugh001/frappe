import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def handle_request():
    """
    Handle different HTTP methods (GET, POST, PUT, DELETE) on a single URL.
    """
    method = frappe.local.request.method

    if method == "GET":
        return get_tasks()
    elif method == "POST":
        return create_record()
    elif method == "PUT":
        return update_record()
    elif method == "DELETE":
        if 'fieldname' in frappe.local.form_dict:
            return delete_specific_field()
        else:
            return delete_record()
    else:
        return {"error": "Invalid request method"}, 405

def get_tasks():
    """
    Fetch tasks or a specific record and include child data if any.
    """
    data = frappe.local.form_dict
    doctype = data.get('doctype')
    name = data.get('name')

    if not doctype:
        return {"error": "doctype is required"}, 400

    try:
        if name:
            
            document = frappe.get_doc(doctype, name)
            return document.as_dict()
        else:
            
            records = frappe.get_all(doctype, fields=["name"])
            detailed_records = [frappe.get_doc(doctype, record.name).as_dict() for record in records]
            return detailed_records
    except Exception as e:
        frappe.log_error(message=str(e), title="Error Fetching Tasks")
        return {"error": str(e)}, 500

def create_record():
    """
    Create a new record for the specified doctype.
    """
    data = frappe.local.form_dict
    doctype = data.get('doctype')

    if not doctype:
        return {"error": "doctype is required"}, 400

    try:
        doc = frappe.get_doc({
            "doctype": doctype,
            **data
        })
        doc.insert()
        frappe.db.commit()  
        return doc.as_dict()
    except Exception as e:
        frappe.db.rollback() 
        frappe.log_error(message=str(e), title="Error Creating Record")
        return {"error": str(e)}, 500

def update_record():
    """
    Update a specific record and its fields.
    """
    data = frappe.local.form_dict
    doctype = data.get('doctype')
    name = data.get('name')

    if not doctype or not name:
        return {"error": "doctype and name are required"}, 400

    try:
        doc = frappe.get_doc(doctype, name)
        for key, value in data.items():
            if key not in ['doctype', 'name']:
                if hasattr(doc, key):
                    setattr(doc, key, value)
                else:
                    return {"error": f"Field '{key}' does not exist in doctype '{doctype}'"}, 400
        doc.save()
        frappe.db.commit()  
        return doc.as_dict()
    except Exception as e:
        frappe.db.rollback()  
        frappe.log_error(message=str(e), title="Error Updating Record")
        return {"error": str(e)}, 500

def delete_record():
    """
    Delete a specific record.
    """
    data = frappe.local.form_dict
    doctype = data.get('doctype')
    name = data.get('name')

    if not doctype or not name:
        return {"error": "doctype and name are required"}, 400

    try:
        frappe.delete_doc(doctype, name)
        frappe.db.commit()  
        return {"message": f"Record '{name}' deleted successfully"}
    except Exception as e:
        frappe.db.rollback()  
        frappe.log_error(message=str(e), title="Error Deleting Record")
        return {"error": str(e)}, 500

def delete_specific_field():
    """
    Delete a specific field from a specific record.
    """
    data = frappe.local.form_dict
    doctype = data.get('doctype')
    name = data.get('name')
    fieldname = data.get('fieldname')

    if not doctype or not name or not fieldname:
        return {"error": "doctype, name, and fieldname are required"}, 400

    try:
        doc = frappe.get_doc(doctype, name)
        if hasattr(doc, fieldname):
            setattr(doc, fieldname, None)  
            doc.save()
            frappe.db.commit()  
            return {"message": f"Field '{fieldname}' from record '{name}' deleted successfully"}
        else:
            return {"error": f"Field '{fieldname}' does not exist in doctype '{doctype}'"}, 400
    except Exception as e:
        frappe.db.rollback()  
        frappe.log_error(message=str(e), title="Error Deleting Field")
        return {"error": str(e)}, 500
