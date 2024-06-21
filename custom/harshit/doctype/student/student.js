// Copyright (c) 2024, demo and contributors
// For license information, please see license.txt

frappe.ui.form.on("Student", {
    refresh(frm) {
        // Code inside refresh function (if any)
    },

    savebutton(frm) {
       
        console.log(frm.doc);

        
        frappe.call({
            method: 'frappe.client.insert',
            args: {
                doc: {
                    'doctype': 'User',
                    'email': frm.doc.email,
                    'first_name': frm.doc.first_name,
                    'last_name': frm.doc.last_name,
                    'enabled': 1,
                    'user_type': 'System User',
                    'roles': [{
                        'role': 'Student'
                    }]
                }
            },
            callback: function (response) {
                if (response.message) {
                    frappe.msgprint(__('User created successfully'));
                }
            }
        });
    },

    your_address(frm) {
        if (frm.doc.your_address) {
            
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Address",
                    name: frm.doc.your_address
                },
                callback: function(r) {
                    if (r.message) {
                        
                        frm.fields_dict['combined_address'].html('<p>' + r.message.address_line1 + '<span>,</span>' + r.message.address_line2 + '<span>,</span> ' + r.message.city + '<span>,</span>' + r.message.state + ' <span>,</span>' + r.message.country + ' <span>,</span>' + r.message.pincode + '</p>');
                    }
                }
            });
        }
    }
});
