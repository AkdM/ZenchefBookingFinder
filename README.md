# Zenchef Table Booking finder

## 💭 About
Automatically checks for booking tables for a restaurant using Zenchef.

## 🚀 Installation

1. Create a specific virtual environment with venv using `python3 -m venv env`
2. Then source it with `source ./env/bin/activate`
3. Install requirements with `pip install -r requirements.txt`

## 🔥 Usage

```
Zenchef Table Booking finder

options:
  -h, --help            show this help message and exit
  --restaurant RESTAURANT_ID, -r RESTAURANT_ID
                        ID of the restaurant (several IDs can be provided separated with a comma)
  --guests GUESTS, -g GUESTS
                        Number of guests
  --date-begin DATE_BEGIN, -b DATE_BEGIN
                        Date begin to search for (format: YYYY-MM-DD)
  --date-end DATE_END, -e DATE_END
                        Date end to search for (format: YYYY-MM-DD)
  --frequency FREQUENCY, -f FREQUENCY
                        Frequency in minute between each check
  --telegram TELEGRAM   Telegram token and chat ID (format: token:chatId separated by a colon)
  --mode {NotificationCenter,Telegram,Both}, -m {NotificationCenter,Telegram,Both}
                        Mode of alert (if telegram token is provided only)

```

## 🛠️ Dependencies

- [requests](https://pypi.org/project/requests/)
- [pync](https://pypi.org/project/pync/)
- [dateutil](https://pypi.org/project/python-dateutil/)

## 🤝 Contributing

If you are interested in helping contribute to this repository, do not hesitate to create a pull request!

## 📝 License

Copyright © 2023-present, [Contributors](https://github.com/AkdM/ZenchefBookingFinder/graphs/contributors).<br>
This project is [GNU LGPLv3](https://github.com/AkdM/ZenchefBookingFinder/blob/master/LICENSE) licensed.