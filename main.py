#!/usr/bin/env python
import time
import requests
import pync
import argparse
import datetime
import sys
from dateutil.relativedelta import relativedelta
import urllib3

def restaurant_informations(restaurant_id):
  restaurant_request = requests.request(
    method='GET',
    url='https://bookings-middleware.zenchef.com/getWidgetParams',
    params={'restaurantId': restaurant_id}
  )
  if restaurant_request.status_code == 200:
     response_restaurant = restaurant_request.json()
     restaurant_name = response_restaurant.get('name')
     return restaurant_name
  return None

def check_availabilities(restaurant_id, guests, date_begin, date_end):
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

  availableSlots = {}
  url = f"https://bookings.zenchef.com/results?rid={restaurant_id}"

  if r.status_code == 200:
    response_availabilities = r.json()
    if not isinstance(response_availabilities, list):
      print ("Unable to reach ZenChef API, please check network connectivity or configuration")
      return
    for runningDate in response_availabilities:
      for shift in runningDate.get('shifts', []):
        for slot in shift.get('shift_slots'):
          available = True if guests in slot.get('possible_guests') else False
          hour = slot.get('name')
          if available:
            formatted_date = datetime.datetime.strptime(runningDate.get('date'), '%Y-%m-%d').strftime('%A %d %b %Y')
            if shift.get("id") not in availableSlots:
              availableSlots[shift.get("id")] = {"slots": [], "date" : formatted_date, "name": shift.get('name')}
            availableSlots[shift.get("id")]["slots"].append(hour)

  return availableSlots

def main():
    print("Starting…")

    parser = argparse.ArgumentParser(description='Zenchef Table Booking finder')
    parser.add_argument('--restaurant', '-r', dest='restaurant_id', required=True,
                        help='ID of the restaurant (several IDs can be provided separated with a comma)')
    parser.add_argument('--guests', '-g', dest='guests', type=int, required=True,
                        help='Number of guests')
    parser.add_argument('--date-begin', '-b', dest='date_begin', required=False,
                        help='Date begin to search for (format: YYYY-MM-DD)', default=datetime.date.today().strftime('%Y-%m-%d'))
    parser.add_argument('--date-end', '-e', dest='date_end', required=False,
                        help='Date end to search for (format: YYYY-MM-DD)', default = (datetime.date.today()+ relativedelta(months=3)).strftime('%Y-%m-%d') )
    parser.add_argument('--frequency', '-f', dest='frequency', type=int, required=False,
                        help='Frequency in minute between each check', default = 3 )
    parser.add_argument('--telegram', dest='telegram', required=False,
                        help='Telegram token and chat ID (format: token:chatId separated by a colon)' )
    parser.add_argument('--mode', '-m', dest='mode', required=False,
                        help='Mode of alert (if telegram token is provided only)', choices=["NotificationCenter", "Telegram", "Both"], default= "Both")
    
    args = parser.parse_args()
    date_begin_formatted = datetime.datetime.strptime(args.date_begin, '%Y-%m-%d').strftime('%x')
    date_end_formatted = datetime.datetime.strptime(args.date_end, '%Y-%m-%d').strftime('%x')
    restaurants_splits = args.restaurant_id.split(",")
    restaurants = {}
    restaurant_names = []
    for restaurant in restaurants_splits:
      restaurant_name = restaurant_informations(restaurant_id=restaurant)
      if restaurant_name:
        restaurants[restaurant] = restaurant_name
        if restaurant_name not in restaurant_names:
          restaurant_names.append(restaurant_name)
  
    if len(restaurants.keys()):
      pync.notify(f"Between {date_begin_formatted} and {date_end_formatted}", title="Search initiated for {}".format( ", ".join(restaurant_names)))
    knownSlots = {}
    while True:
      tmpSlots = {}
      isBreaked = False
      for restaurant in restaurants:
        url = f"https://bookings.zenchef.com/results?rid={restaurant}"
        isNotified = False
        tmpBegin = datetime.datetime.strptime(args.date_begin, "%Y-%m-%d")
        while tmpBegin <= datetime.datetime.strptime(args.date_end, "%Y-%m-%d"):
          if isBreaked:
            break
          tmpEnd = min(tmpBegin + relativedelta(days=40), datetime.datetime.strptime(args.date_end, "%Y-%m-%d"))
          try:
            availableSlots = check_availabilities(
              restaurant_id=restaurant,
              guests=args.guests,
              date_begin=tmpBegin.strftime('%Y-%m-%d'),
              date_end=tmpEnd.strftime('%Y-%m-%d'),
            )
          except (urllib3.exceptions.HTTPError, requests.RequestException) as e:
            isBreaked = True
            print ("ERROR - Unable to retrieve booking availability, retrying later")
            break
          toNotify = False
          for shift in availableSlots:
            message = f"☑️ {availableSlots[shift]['date']} - {{hour}} ({availableSlots[shift]['name']}) - {args.guests} guests - {restaurants[restaurant]}\n{url}\n"
            
            if shift in knownSlots.get(restaurant, {}):
              for slot in availableSlots[shift]["slots"]:
                if slot not in knownSlots[restaurant][shift]["slots"]:
                  toNotify = True
                  print(message.format(hour=slot))
            else:
              toNotify = True
              for slot in availableSlots[shift]["slots"]:
                print(message.format(hour=slot))

          tmpSlots[restaurant] = tmpSlots.get(restaurant, {}) | availableSlots
          if toNotify and not isNotified:
            isNotified = True
            if args.mode == "Both" or args.mode == "NotificationCenter": 
              pync.notify("Click to check", title=f"✅ Slots found at {restaurants[restaurant]}", open=url)
            if args.mode == "Both" or args.mode == "Telegram": 
              token = args.telegram.split(":")
              if len(token) < 3:
                print("Telegram API token invalid! Format -> token:chatId")
                sys.exit(2)
              api_url = f'https://api.telegram.org/bot{token[0]}:{token[1]}/sendMessage'
              urlEscape = url.replace("\\", '\\').replace('-', '\-').replace('*', '\*').replace('[','\[').replace(']','\]').replace("(", "\(").replace(")", "\)").replace(".", "\.").replace("~", "\~").replace('`', '\`').replace('>', '\>').replace('<', '\<').replace("&", "\&").replace("#", "\#").replace("+", "\+").replace("+", "\+").replace("-", "\-").replace("=", "\=").replace("|", "\|").replace("{", "\{").replace("}", "\}").replace("!", "\!")

              api_params = {
                  'chat_id': token[2],
                  'text': f"✅ Slots found at {restaurants[restaurant]} click to check : [{urlEscape}]({urlEscape})",
                  'parse_mode': 'MarkdownV2'
              }
              try:
                rqst = requests.post(api_url, json=api_params, timeout=10)
                if not rqst or not rqst.ok:
                  print("Unable to send Telegram message, please check network or configuration")
              except (urllib3.exceptions.HTTPError, requests.RequestException) as e:
                isBreaked = True
                print ("ERROR - Unable to send Telegram message, retrying later")
                break
          time.sleep(5)
          tmpBegin = tmpEnd + relativedelta(days=1)
      if not isBreaked:
        knownSlots = tmpSlots
      time.sleep(60 * args.frequency)

if __name__ == '__main__':
    main()