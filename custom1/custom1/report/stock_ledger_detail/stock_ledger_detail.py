# Copyright (c) 2013, jonathan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe import msgprint, _

def execute(filters=None):
	columns = get_columns()
	sl_entries = get_stock_ledger_entries(filters)
	item_details = get_item_details(filters)
	opening_row = get_opening_balance(filters, columns)
        party_details = {}
	party = []
	
	data = []
	
	if opening_row:
		data.append(opening_row)

	for sle in sl_entries:
		item_detail = item_details[sle.item_code]
                
		party_details = get_party_details(sle.item_code, sle.voucher_type, sle.voucher_no)
		if sle.voucher_type in ("Sales Invoice", "Purchase Invoice", "Purchase Receipt", "Delivery Note"): 
			party = party_details[sle.voucher_no]
			data.append([sle.date, sle.item_code, item_detail.item_name, item_detail.item_group,
				item_detail.brand, item_detail.description, sle.warehouse,
				item_detail.stock_uom, sle.actual_qty, sle.qty_after_transaction,
				(sle.incoming_rate if sle.actual_qty > 0 else 0.0), party.outgoing_rate, 
				sle.valuation_rate, sle.stock_value, party.party, 
				sle.voucher_type, sle.voucher_no, party.party_type,
				sle.batch_no, sle.serial_no, sle.company])
		else:
			data.append([sle.date, sle.item_code, item_detail.item_name, item_detail.item_group,
				item_detail.brand, item_detail.description, sle.warehouse,
				item_detail.stock_uom, sle.actual_qty, sle.qty_after_transaction,
				(sle.incoming_rate if sle.actual_qty > 0 else 0.0), 0.0, 
				sle.valuation_rate, sle.stock_value, "",
				sle.voucher_type, sle.voucher_no, "",
				sle.batch_no, sle.serial_no, sle.company])
	
	return columns, data

def get_columns():
	return [_("Date") + ":Datetime:95", _("Item") + ":Link/Item:130", _("Item Name") + "::100", _("Item Group") + ":Link/Item Group:100",
		_("Brand") + ":Link/Brand:100", _("Description") + "::200", _("Warehouse") + ":Link/Warehouse:100",
		_("Stock UOM") + ":Link/UOM:100", _("Qty") + ":Float:50", _("Balance Qty") + ":Float:100",
		_("Incoming Rate") + ":Currency:110", _("Outgoing Rate") + ":Currency:110", 
		_("Valuation Rate") + ":Currency:110", _("Balance Value") + ":Currency:110",
		_("Customer/Supplier") + ":Dynamic Link/Party Type:150",
		_("Voucher Type") + "::110", _("Voucher #") + ":Dynamic Link/Voucher Type:100", 
		_("Party Type") + "::100",
		_("Batch") + ":Link/Batch:100",	_("Serial #") + ":Link/Serial No:100", _("Company") + ":Link/Company:100"
	]

def get_stock_ledger_entries(filters):
	return frappe.db.sql("""select concat_ws(" ", posting_date, posting_time) as date,
			item_code, warehouse, actual_qty, qty_after_transaction, incoming_rate, valuation_rate,
			stock_value, voucher_type, voucher_no, batch_no, serial_no, company
		from `tabStock Ledger Entry`
		where company = %(company)s and 
			posting_date between %(from_date)s and %(to_date)s
			{sle_conditions}
			order by posting_date asc, posting_time asc, name asc"""\
		.format(sle_conditions=get_sle_conditions(filters)), filters, as_dict=1)

def get_item_details(filters):
	item_details = {}
	for item in frappe.db.sql("""select name, item_name, description, item_group,
			brand, stock_uom from `tabItem` {item_conditions}"""\
			.format(item_conditions=get_item_conditions(filters)), filters, as_dict=1):
		item_details.setdefault(item.name, item)

	return item_details

def get_party_details(item_code,voucher_type,voucher_no):
	party_details = {}
 	params = {
		'item_code' : item_code,
		'voucher_no' : voucher_no,
         	'voucher_type' : voucher_type
	}

	if voucher_type == "Sales Invoice":
       		for party in frappe.db.sql("""select dt_item.parent, dt_item.item_code, dt.customer as party, 'Customer' as party_type, dt_item.rate as outgoing_rate
			from `tabSales Invoice` dt, `tabSales Invoice Item` dt_item
			where dt.name = dt_item.parent and dt_item.parent = %(voucher_no)s and dt_item.item_code = %(item_code)s""", params, as_dict=1):
			party_details.setdefault(party.parent, party) 
	elif voucher_type == "Delivery Note":
       		for party in frappe.db.sql("""select dt_item.parent, dt_item.item_code, dt.customer as party, 'Customer' as party_type, dt_item.rate as outgoing_rate
			from `tabDelivery Note` dt, `tabDelivery Note Item` dt_item
			where dt.name = dt_item.parent and dt_item.parent = %(voucher_no)s and dt_item.item_code = %(item_code)s""", params, as_dict=1):
			party_details.setdefault(party.parent, party)
	elif voucher_type == "Purchase Invoice":
       		for party in frappe.db.sql("""select dt_item.parent, dt_item.item_code, dt.supplier as party, 'Supplier' as party_type, 0.0 as outgoing_rate
			from `tabPurchase Invoice` dt, `tabPurchase Invoice Item` dt_item
			where dt.name = dt_item.parent and dt_item.parent = %(voucher_no)s and dt_item.item_code = %(item_code)s""", params, as_dict=1):
			party_details.setdefault(party.parent, party)
	elif voucher_type == "Purchase Receipt":
       		for party in frappe.db.sql("""select dt_item.parent, dt_item.item_code, dt.supplier as party, 'Supplier' as party_type, 0.0 as outgoing_rate
			from `tabPurchase Receipt` dt, `tabPurchase Receipt Item` dt_item
			where dt.name = dt_item.parent and dt_item.parent = %(voucher_no)s and dt_item.item_code = %(item_code)s""", params, as_dict=1):
			party_details.setdefault(party.parent, party)

	return party_details


def get_party_conditions(item_code, voucher_no):
	conditions = []
	if item_code:
		conditions.append("dt_item.item_code=''")
	if voucher_no:
		conditions.append("dt_item.parent=''")

	return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_item_conditions(filters):
	conditions = []
	if filters.get("item_code"):
		conditions.append("name=%(item_code)s")
	if filters.get("brand"):
		conditions.append("brand=%(brand)s")

	return "where {}".format(" and ".join(conditions)) if conditions else ""

def get_sle_conditions(filters):
	conditions = []
	item_conditions=get_item_conditions(filters)
	if item_conditions:
		conditions.append("""item_code in (select name from tabItem
			{item_conditions})""".format(item_conditions=item_conditions))
	if filters.get("warehouse"):
		conditions.append("warehouse=%(warehouse)s")
	if filters.get("voucher_no"):
		conditions.append("voucher_no=%(voucher_no)s")

	return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_opening_balance(filters, columns):
	if not (filters.item_code and filters.warehouse and filters.from_date):
		return

	from erpnext.stock.stock_ledger import get_previous_sle
	last_entry = get_previous_sle({
		"item_code": filters.item_code,
		"warehouse": filters.warehouse,
		"posting_date": filters.from_date,
		"posting_time": "00:00:00"
	})
	
	row = [""]*len(columns)
	row[1] = _("'Opening'")
	for i, v in ((9, 'qty_after_transaction'), (11, 'valuation_rate'), (12, 'stock_value')):
			row[i] = last_entry.get(v, 0)
		
	return row