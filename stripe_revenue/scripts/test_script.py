'''This is just a test script written to test certain things which 
trying to figure out how this project can be done
'''

api_key = '<YOUR-API-KEY>'
import stripe
import logging
from pandora.utils import enable_console_logging
from datetime import datetime
import calendar

if __name__ == '__main__':
    # init stripe
    stripe.api_key = api_key

    # Try to get all the customers
    start_index = 0 # This is the start index
    count = 100
    customers = []
    while True:
	c = list(stripe.Customer.all(offset = start_index, count = count).get('data'))
	if c:
	    customers = customers + c
	    start_index = start_index + count
	else:
	    break
    print 'number of customers: %s' %(len(customers))
    for customer in customers:
	# print the IDs
	# get the number of charges for the time period defined below
	start_date = datetime.strptime('2013-04-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
	end_date = datetime.strptime('2013-04-05T23:59:59Z', '%Y-%m-%dT%H:%M:%SZ')
	charges = []
	charge_start_index = 0
	charge_count = 100
	while True:
	    ch = list(stripe.Charge.all(customer = customer.id, created = {
		'gte' : calendar.timegm(start_date.utctimetuple()),
		'lte' : calendar.timegm(end_date.utctimetuple())
		}, offset = charge_start_index, count = charge_count).get('data'))
	    if ch:
		charges = charges + ch
		charge_start_index = charge_start_index + charge_count
	    else:
		break
	print 'id: %s, name: %s, num_charges: %s' %(customer.id, customer.active_card.get('name') \
		if customer.active_card else '', len(charges))
