// Copyright (c) 2013, jonathan and contributors
// For license information, please see license.txt


frappe.query_reports["Transaction Logs"] = {
	"filters": [
		{
			fieldname:"company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: frappe.defaults.get_user_default("company")
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -6),
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: get_today()
		},
		{
			fieldname:"party_type",
			label: __("Party Type"),
			fieldtype: "Select",
			options: "Customer\nSupplier",
			default: "Customer"
		},
		{
			"fieldname":"party",
			"label": __("Party"),
			"fieldtype": "Dynamic Link",
			"get_options": function() {
				var party_type = frappe.query_report.filters_by_name.party_type.get_value();
				var party = frappe.query_report.filters_by_name.party.get_value();
				if(party && !party_type) {
					frappe.throw(__("Please select Party Type first"));
				}
				return party_type;
			}
		},
                {
			"fieldname":"item_code",
			"label": __("Search Item"),
			"fieldtype": "Link",
			"options": "Item",
                        "width": "300px"
		}
	]
}
