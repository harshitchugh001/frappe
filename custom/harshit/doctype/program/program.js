frappe.ui.form.on('Program', {
    refresh: function(frm) {
        
        frm.fields_dict['participants'].grid.wrapper.on('click', 'button[data-fieldname="preview_button"]', function(e) {
            let row = $(e.currentTarget).closest('.grid-row');
            let doc = row.data('doc');

            if (doc && doc.participant) {
               
                frappe.call({
                    method: 'frappe.client.get',
                    args: {
                        doctype: 'Student',
                        name: doc.participant
                    },
                    callback: function(r) {
                        if (r.message && r.message.attach_image) {
                          
                            frappe.msgprint({
                                title: __('Profile Picture'),
                                message: `<img src="${r.message.attach_image}" alt="Profile Image" style="max-width:100%; max-height:400px;">`,
                                indicator: 'blue'
                            });
                        } else {
                            frappe.msgprint(__('No profile picture found for this participant.'));
                        }
                    }
                });
            } else {
                frappe.msgprint(__('Please select a participant first.'));
            }
        });
    },

    participants_add: function(frm, cdt, cdn) {
        
        let row = locals[cdt][cdn];
        if (row && row.preview_button) {
            frappe.ui.form.on('Program Participant', 'preview_button', function(frm, cdt, cdn) {
                let row = locals[cdt][cdn];

                if (row.participant) {
                    frappe.call({
                        method: 'frappe.client.get',
                        args: {
                            doctype: 'Student',
                            name: row.participant
                        },
                        callback: function(r) {
                            if (r.message && r.message.attach_image) {
                                frappe.msgprint({
                                    title: __('Attach Image'),
                                    message: `<img src="${r.message.attach_image}" alt="Profile Image" style="max-width:100%; max-height:400px;">`,
                                    indicator: 'blue'
                                });
                            } else {
                                frappe.msgprint(__('No profile picture found.'));
                            }
                        }
                    });
                }
            });
        }
    },
});
