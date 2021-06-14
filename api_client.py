import pdb
import datetime as dt
import requests

AVAILABLE_DAYS_URL = "https://www.passport.gov.ph/appointment/timeslot/available"

AVAILABLE_SLOTS_URL = "https://www.passport.gov.ph/appointment/timeslot"


SITES = {
    "26": "PUERTO PRINCESA (ROBINSONS PALAWAN)",
}

def get_available_dates(response_data):

    available_dates = []

    for date_data in response_data:
        if date_data.get("IsAvailable", False) is False:
            continue

        # datetime expects the timestamp to be in seconds
        # while passport.gov.ph returns a timestamp
        # in milliseconds
        timestamp = date_data["AppointmentDate"] / 1000

        # AVAILABLE_DAYS_URL returns the dates as timestamps
        # while AVAILABLE_SLOTS_URL expects yyyy-mm-dd
        # so we convert them here
        date_str = dt.datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d"
        )
        available_dates.append(date_str)
    return available_dates



def main():

    request_data = {
        "fromDate": "2021-06-17",
        "toDate": "2021-12-31",
        "siteId": "26",
        "requestedSlots": "1",
    }

    response = requests.post(AVAILABLE_DAYS_URL, data=request_data)

    response_data = response.json()
    available_dates = get_available_dates(response_data)
    for dates in available_dates:
        print(dates)


if __name__ == "__main__":
    main()
