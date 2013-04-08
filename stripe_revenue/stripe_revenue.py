'''stripe_revenue: Python library to get the stripe revenue customer-wise
'''

__version__ = '1.0'
__author__ = 'Siddharth Saha (sidchilling@gmail.com)'

import stripe
import calendar

class StripeRevenue(object):

    api_key = None
    start_date = None
    end_date = None

    def __init__(self, api_key, start_date, end_date):
	assert api_key, 'api_key is required'
	assert start_date, 'start_date is required'
	assert end_date, 'end_date is required'
	self.api_key = api_key
	self.start_date = start_date
	self.end_date = end_date
	stripe.api_key = self.api_key
    
    def _get_all_customers(self):
	# Returns a list of all the customers
	start_index = 0
	count = 100
	res = [] # This is the list of customers which will be returned
	while True:
	    c = list(stripe.Customer.all(offset = start_index, count = count).get('data'))
	    if c:
		res = res + c
		start_index = start_index + count
	    else:
		break
	return res

    def _get_all_charges(self, customer):
	# Returns a list of all the charges for this customer in the date range
	start_index = 0
	count = 100
	res = [] # This is the list of charges that will be returned
	while True:
	    ch = list(stripe.Charge.all(customer = customer.id, offset = start_index, 
		    count = count, created = {
			'gte' : calendar.timegm(self.start_date.utctimetuple()),
			'lte' : calendar.timegm(self.end_date.utctimetuple())
			}).get('data'))
	    if ch:
		for charge in ch:
		    if charge.paid:
			# will add only those charges which are actually paid
			res = res + [charge]
		start_index = start_index + count
	    else:
		break
	return res

    def _get_revenue_amount(self, customer):
	# This function returns the revenue of the customer
	# First get all the charges for the customer
	charges = self._get_all_charges(customer = customer)
	print 'num_charges: %s, customer: %s' %(len(charges), customer.id)
	amount = 0
	for ch in charges:
	    amount = amount + ch.amount
	return amount

    def get(self):
	'''This will return the revenue data from start_date and end_date. The format -
	{
	    'customer_id' : {
		'revenue-amount' : '<amount-in-cents>',
		'customer-name' : '<name-of-the-customer>'
	    }
	}
	'''
	res = {}
	customers = self._get_all_customers()
	print 'num_customers: %s' %(len(customers))
	for c in customers:
	    if c.id in res:
		res[c.id]['revenue-amount'] = res.get(c.id).get('revenue-report') + \
			self._get_revenue_amount(customer = c)
	    else:
		res[c.id] = {
			'revenue-amount' : self._get_revenue_amount(customer = c),
			'customer-name' : c.active_card.get('name') if c.active_card else ''
			}
	return res

