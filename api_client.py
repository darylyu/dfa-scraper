import pdb
import datetime as dt
import requests

AVAILABLE_DAYS_URL = "https://www.passport.gov.ph/appointment/timeslot/available"

AVAILABLE_SLOTS_URL = "https://www.passport.gov.ph/appointment/timeslot"


SITES = {
    "26": "PUERTO PRINCESA (ROBINSONS PALAWAN)",
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
        date_str = dt.datetime.fromtimestamp(timestamp).strftime(
            "%Y-%m-%d"
        )
        available_dates.append(date_str)
    return available_dates



def main():

    request_data = {
        "fromDate": "2021-06-14",
        "toDate": "2022-06-14",
        "siteId": "17",
        "requestedSlots": "10",
    }

    response = requests.post(AVAILABLE_DAYS_URL, data=request_data)

    response_data = response.json()
    available_dates = get_available_dates(response_data)
    for dates in available_dates:
        print(dates)


if __name__ == "__main__":
    main()
