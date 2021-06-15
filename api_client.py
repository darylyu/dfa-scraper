import datetime as dt
import requests

from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

AVAILABLE_DAYS_URL = "https://www.passport.gov.ph/appointment/timeslot/available"

AVAILABLE_SLOTS_URL = "https://www.passport.gov.ph/appointment/timeslot"


SITES = {
    "10": "Angeles (MarQuee Mall,Angeles, Pampanga)",
    "486": "Antipolo (SM Cherry, Antipolo City, Rizal)",
    "11": "Bacolod (Robinsons Bacolod)",
    "12": "Baguio (SM City Baguio)",
    "14": "Butuan (Robinsons Butuan)",
    "15": "Cagayan De Oro (Centrio Mall, CDO City)",
    "16": "Calasiao (Robinsons Calasiao, Pangasinan)",
    "17": "Cebu (Pacific Mall Metro Mandaue, Cebu)",
    "487": "Clarin (Town Center,,Clarin, Misamis OCC)",
    "18": "Cotabato (Mall of Alnor, Cotabato City)",
    "4": "DFA Manila (Aseana)",
    "516": "DFA Manila (Aseana-Courtesy Lane)",
    "5": "DFA NCR Central (Robinsons Galleria EDSA)",
    "6": "DFA NCR East (SM Megamall, Mandaluyong City)",
    "423": "DFA NCR North (Robinsons Novaliches, Quezon City)",
    "7": "DFA NCR Northeast (Ali Mall Cubao, Quezon City)",
    "8": "DFA NCR South (Metro ATC, Muntinlupa City)",
    "9": "DFA NCR West (SM City, Manila)",
    "488": "Dasmariñas ( SM City Dasmariñas)",
    "19": "Davao (SM City Davao)",
    "20": "Dumaguete (Robinsons Dumaguete)",
    "21": "General Santos (Robinsons Gen. Santos City)",
    "424": "Ilocos Norte (Robinsons Place, San Nicolas)",
    "22": "Iloilo (Robinsons Iloilo)",
    "23": "La Union (CSI Mall San Fernando, La Union)",
    "24": "Legazpi (Pacific Mall Legazpi)",
    "13": "Lipa (Robinsons Lipa)",
    "25": "Lucena (Pacific Mall, Lucena)",
    "489": "Malolos (CTTCH.,Xentro Mall, Malolos City)",
    "27": "Pampanga (Robinsons StarMills San Fernando)",
    "553": "Paniqui,  Tarlac (WalterMart)",
    "26": "Puerto Princesa (Robinsons Palawan)",
    "490": "San Pablo ( Sm City San Pablo)",
    "425": "Santiago, Isabela (Robinsons Place Santiago)",
    "28": "Tacloban (Robinsons N. Abucay, Tac. City)",
    "491": "Tagum ( Gaisano Mall of Tagum )",
    "29": "Tuguegarao (Reg. Govt Center, Tuguegarao City)",
    "30": "Zamboanga (Go-Velayo Bldg. Vet. Ave. Zambo)",
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
        date_str = dt.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        available_dates.append(date_str)
    return available_dates


def get_available_slots(date, site_id, requested_slots):
    request_data = {
        "preferredDate": date,
        "siteId": site_id,
        # AVAILABLE_DAYS_URL uses "requestedSlots"
        # while AVAILABLE_SLOTS_URL "requiredSlots"
        "requiredSlots": requested_slots,
    }
    response = requests.post(AVAILABLE_SLOTS_URL, data=request_data)
    soup = BeautifulSoup(response.text, "html.parser")
    slots = soup.find_all("label")
    for slot in slots:
        sched = slot.find_all("span")[2].text
        availability = slot.find_all("span")[3].text.strip()

        if availability == "Available":
            print(f" * {sched}")


def get_site_schedule(site_id, requested_slots):

    today = dt.datetime.today()

    # This is required, but their API doesn't actually respect this
    # and just gives the next 3 months regardless of what you give.
    #
    # Just giving this a good buffer if they end up actually fixing this.
    a_year_later = dt.datetime.today() + relativedelta(years=1)

    request_data = {
        "fromDate": today.strftime("%Y-%m-%d"),
        "toDate": a_year_later.strftime("%Y-%m-%d"),
        "siteId": site_id,
        "requestedSlots": requested_slots,
    }

    response = requests.post(AVAILABLE_DAYS_URL, data=request_data)

    response_data = response.json()
    available_dates = get_available_dates(response_data)

    site_name = SITES[site_id]
    print(f"Available slots for {site_name}")
    for date in available_dates:
        print(date)
        available_slots = get_available_slots(date, site_id, requested_slots)


def main():

    # Yes, their API wants ints as strings.
    site_ids = SITES.keys()
    requested_slots = "1"

    for site_id in site_ids:
        get_site_schedule(site_id, requested_slots)


if __name__ == "__main__":
    main()
