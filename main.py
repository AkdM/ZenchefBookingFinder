#!/usr/bin/env python
import time
import requests
import pync
import argparse
from datetime import datetime

def restaurant_informations(restaurant_id, guests, date_begin, date_end):
  restaurant_request = requests.request(
    method='GET',
    url='https://bookings-middleware.zenchef.com/getWidgetParams',
    params={'restaurantId': restaurant_id}
  )

  date_begin_formatted = datetime.strptime(date_begin, '%Y-%m-%d').strftime('%x')
  date_end_formatted = datetime.strptime(date_end, '%Y-%m-%d').strftime('%x')

  if restaurant_request.status_code == 200:
     response_restaurant = restaurant_request.json()
     restaurant_name = response_restaurant.get('name')
     pync.notify(f"Between {date_begin_formatted} and {date_end_formatted}", title=f"Search initiated for {restaurant_name}")
     return restaurant_name

def check_availabilities(restaurant_name, restaurant_id, guests, date_begin, date_end):
  parameters = {
    'restaurantId': int(restaurant_id),
    'date_begin': date_begin,
    'date_end': date_end
  }

  r = requests.request(
    method='GET',
    url='https://bookings-middleware.zenchef.com/getAvailabilities',
    params=parameters
  )

  is_available = False
  url = f"https://bookings.zenchef.com/results?rid={restaurant_id}"

  if r.status_code == 200:
    response_availabilities = r.json()
    for runningDate in response_availabilities:
      for shift in runningDate.get('shifts', []):
        for slot in shift.get('shift_slots'):
          available = True if int(guests) in slot.get('possible_guests') else False
          hour = slot.get('name')
          if available:
            is_available = True
            formatted_date = datetime.strptime(runningDate.get('date'), '%Y-%m-%d').strftime('%A %d %b %Y')
            message = f"☑️ {formatted_date} - {hour} ({shift.get('name')}) - {guests} guests\n{url}\n"
            print(message)
    if is_available:
      pync.notify("Click to check", title=f"✅ Slots found at {restaurant_name}", open=url)

def main():
    print("Starting…")

    parser = argparse.ArgumentParser(description='Zenchef Table Booking finder')
    parser.add_argument('--restaurant', '-r', dest='restaurant_id', required=True,
                        help='ID of the restaurant')
    parser.add_argument('--guests', '-g', dest='guests', required=True,
                        help='Number of guests')
    parser.add_argument('--date-begin', '-b', dest='date_begin', required=True,
                        help='Date begin to search for (format: YYYY-MM-DD)')
    parser.add_argument('--date-end', '-e', dest='date_end', required=True,
                        help='Date end to search for (format: YYYY-MM-DD)')

    args = parser.parse_args()
    restaurant_name = restaurant_informations(
      restaurant_id=args.restaurant_id,
      guests=args.guests,
      date_begin=args.date_begin,
      date_end=args.date_end
    )

    while True:
      check_availabilities(
        restaurant_name=restaurant_name,
        restaurant_id=args.restaurant_id,
        guests=args.guests,
        date_begin=args.date_begin,
        date_end=args.date_end
      )
      time.sleep(30)

    return

if __name__ == '__main__':
    main()