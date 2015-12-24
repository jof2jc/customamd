# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		"Custom1": {
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Reports"),
                        "system_manager": 1
		},
                "Stock Ledger": {
			"color": "#AA784D",
			"icon": "icon-truck",
			"icon": "octicon octicon-file-text",
			"label": _("Stock Ledger"),
			"link": "query-report/Stock Ledger Detail",
			"type": "query-report"
                },
		 "Stock Entry": {
			"color": "#B1F53B",
			"icon": "icon-truck",
			"icon": "octicon octicon-file-text",
			"label": _("Stock Entry"),
			"link": "List/Stock Entry",
			"type": "List"
                },
                 "Stock Balance": {
			"color": "#FF888B",
			"icon": "icon-truck",
			"icon": "octicon octicon-law",
			"label": _("Stock Balance"),
			"link": "query-report/Stock Balance",
			"type": "query-report"
                },
		"Quotation": {
			"color": "#33cc33",
			"icon": "icon-truck",
			"icon": "octicon octicon-bookmark",
			"label": _("Quotation"),
			"link": "Report/Quotation",
			"type": "Report"
                },
                "Sales Order": {
			"color": "#ff5b33",
			"icon": "icon-truck",
			"icon": "octicon octicon-terminal",
			"label": _("Sales Order"),
			"link": "Report/Sales Order",
			"type": "Report"
                },
                 "Sales Invoice": {
			"color": "#9900cc",
			"icon": "icon-truck",
			"icon": "octicon octicon-checklist",
			"label": _("Sales Invoice"),
			"link": "Report/Sales Invoice",
			"type": "Report"
                },
                 "Purchase Invoice": {
			"color": "#2ecc71",
			"icon": "icon-truck",
			"icon": "octicon octicon-file-submodule",
			"label": _("Purchase Invoice"),
			"link": "Report/Purchase Invoice",
			"type": "Report"
                },
                 "Purchase Receipt": {
			"color": "#2c3e50",
			"icon": "icon-truck",
			"icon": "octicon octicon-clippy",
			"label": _("Purchase Receipt"),
			"link": "Report/Purchase Receipt",
			"type": "Report"
                },
                "Purchase Order": {
			"color": "#EBE894",
			"icon": "icon-truck",
			"icon": "octicon octicon-browser",
			"label": _("Purchase Order"),
			"link": "Report/Purchase Order",
			"type": "Report"
                },
                 "Delivery Note": {
			"color": "#A7FAD1",
			"icon": "icon-truck",
			"icon": "octicon octicon-gift",
			"label": _("Delivery Note"),
			"link": "Report/Delivery Note",
			"type": "Report"
                },
                "Payment Tool": {
			"color": "#8e44ad",
			"icon": "icon-truck",
			"icon": "octicon octicon-credit-card",
			"label": _("Payment Tool"),
			"link": "Form/Payment Tool",
			"type": "Form"
                },
                "Item": {
			"color": "#EF4DB6",
			"icon": "icon-truck",
			"icon": "octicon octicon-list-ordered",
			"label": _("Item List"),
			"link": "List/Item",
			"type": "List"
                },
                "Item Group": {
			"color": "#3498db",
			"icon": "icon-truck",
			"icon": "octicon octicon-git-merge",
			"label": _("Item Group"),
			"link": "Sales Browser/Item Group",
                        "type": "Page"
			
                },
                "Customer": {
			"color": "#EB94C2",
			"icon": "icon-truck",
			"icon": "octicon octicon-organization",
			"label": _("Customer"),
			"link": "List/Customer",
                        "type": "List"
                },
                "Supplier": {
			"color": "#94DBEB",
			"icon": "icon-truck",
			"icon": "octicon octicon-organization",
			"label": _("Supplier"),
			"link": "List/Supplier",
                        "type": "List"
                },
                "Price List Rate": {
			"color": "#B1F53B",
			"icon": "icon-truck",
			"icon": "octicon octicon-list-unordered",
			"label": _("Price List Rate"),
			"link": "Report/Item Price",
                        "type": "Report"
			
                }
	}
