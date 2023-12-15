# Zenchef Table Booking finder

## 💭 About
Automatically checks for booking tables for a restaurant using Zenchef. Refreshes every 30 seconds.

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
                        ID of the restaurant
  --guests GUESTS, -g GUESTS
                        Number of guests
  --date-begin DATE_BEGIN, -b DATE_BEGIN
                        Date begin to search for (format: YYYY-MM-DD)
  --date-end DATE_END, -e DATE_END
                        Date end to search for (format: YYYY-MM-DD)
```

## 🛠️ Dependencies

- [requests](https://pypi.org/project/requests/)
- [pync](https://pypi.org/project/pync/)

## 🤝 Contributing

If you are interested in helping contribute to this repository, do not hesitate to create a pull request!

## 📝 License

Copyright © 2023-present, [Contributors](https://github.com/AkdM/ZenchefBookingFinder/graphs/contributors).<br>
This project is [GNU LGPLv3](https://github.com/AkdM/ZenchefBookingFinder/blob/master/LICENSE) licensed.