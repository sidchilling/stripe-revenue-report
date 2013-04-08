'''This file is for testing the stripe revenue report
'''

from stripe_revenue import StripeRevenue
from datetime import datetime

if __name__ == '__main__':>
    api_key = '<YOUR-API-KEY'
    start_date = '2012-01-01T00:00:00Z'
    end_date = '2013-04-07T23:59:59Z'
    start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ')
    end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%SZ')
    stripe_revenue = StripeRevenue(api_key = api_key,
	    start_date = start_date, end_date = end_date)
    print 'start_date: %s, end_date: %s' %(start_date.strftime('%Y-%m-%d %H:%M:%S'),
	    end_date.strftime('%Y-%m-%d %H:%M:%S'))
    print stripe_revenue.get()
