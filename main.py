import requests
import xlsxwriter
from bs4 import BeautifulSoup

def scrape_rent_prices(url, target_zones):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        prices = []
        listings = soup.find('div', {'data-cy': 'search.listing.organic'}).find_all('article', class_='css-136g1q2 e17ey1dw0')
        for listing in listings:
            zone = listing.find('p', class_='css-1dvtw4c e1qxnff70').text.strip()
            surface = float(listing.find('dt', string='Suprafață').find_next_sibling('dd').text.strip().replace(',','.').split()[0])
            rooms = int(listing.find('dt', string='Numărul de camere').find_next_sibling('dd').text.strip().replace(',','').split()[0])

            # It can be in RON or EURO so we'll convert RON to EURO if necessary
            priceRE = listing.find('span', class_='css-1uwck7i ewvgbgo0').contents[0].replace('.', '') # replacing to avoid confusion in float '.' for thousands
            if priceRE.split()[1] == 'RON':
                # price = convert_ron_to_eur(float(priceRE.split()[0]))
                price = float(priceRE.split()[0])/5
            else:
                price = float(priceRE.split()[0])

            # It can be in RON or EURO so we'll convert RON to EURO if necessary
            m2price = price / surface
            hyperlink = f"https://www.storia.ro/{listing.find('a', class_='css-16vl3c1 e1njvixn0').get('href')}"

            for target_zone in target_zones:
                if target_zone.lower() in zone.lower():
                    prices.append((zone, price, surface, m2price, rooms, hyperlink))
                    break
        return prices

    elif response.status_code == 403:
        print("Access is forbidden. The server might require authentication, or your IP address might be blocked.")
        return None
    else:
        print(f"Failed to fetch page. Status code: {response.status_code}, Reason: {response.reason}")
        return None


def scrape_all_rent_prices(base_url, num_pages, target_zones):
    total_prices = []
    total_count = 0
    for page in range (1, num_pages + 1):
        url = f"{base_url}&page={page}"
        prices = scrape_rent_prices(url, target_zones)
        if prices:
            total_prices.extend(prices)
            total_count += len(prices)
        else:
            break
    return total_prices, total_count



def generate_excel(workbook_name: str, worksheet_name: str, headers_list: list, data: list):
    # Creating workbook
    workbook = xlsxwriter.Workbook(workbook_name)

    # Creating worksheet
    worksheet = workbook.add_worksheet(worksheet_name)

    # Adding headers and adjusting column width
    for index, header in enumerate(headers_list):
        worksheet.write(0, index, str(header).capitalize())
        # Adjusting column width based on header length
        worksheet.set_column(index, index, len(str(header)) + 2)

    # Adding data and adjusting column width
    max_lengths = [len(str(header)) for header in headers_list]
    for entry in data:
        for index, item in enumerate(entry):
            # Update maximum length for each column
            max_lengths[index] = max(max_lengths[index], len(str(item)))

    for index, max_length in enumerate(max_lengths):
        # Adjust column width based on maximum length of data in that column
        worksheet.set_column(index, index, max_length + 2)

    # Write data to worksheet
    for index1, entry in enumerate(data):
        for index2, item in enumerate(entry):
            worksheet.write(index1 + 1, index2, item)

    # Close workbook
    workbook.close()


def convert_ron_to_eur(amount_ron):
    # It takes longer with the conversion function, so in the code, we estimated 1 EUR ~ 5 RON
    conversionURL = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=RON&To=EUR'
    conversionSoup = BeautifulSoup(requests.get(conversionURL).text, 'html.parser')
    rate = float(conversionSoup.find('p', class_='result__BigRate-sc-1bsijpp-1 dPdXSB').text.split()[0])
    amount_eur = amount_ron * rate
    return amount_eur


# Example of usage:
if __name__ == '__main__':
    base_url = 'https://www.storia.ro/ro/rezultate/inchiriere/apartament/cluj/cluj--napoca?limit=72'
    target_zones = ['gheorgheni','marasti','centru','zorilor','buna ziua','grigorescu']  # list of desired zones (modifiable)
    num_pages = 40 # number of pages to scrape (modifiable)

    rent_prices, total_count = scrape_all_rent_prices(base_url, num_pages, target_zones)

    if rent_prices:
        for zone, price, surface, m2price, rooms, hyperlink in rent_prices:
            print(f"Zone: {zone}, Rent Price: {price}, Surface: {surface}, Price/m^2: {m2price}, Number of Rooms: {rooms}, Link: {hyperlink}")
        print(total_count)
    else:
        print("Data extraction failed.")

    # Generate an Excel file with the extracted data
    generate_excel('RentCluj.xlsx','firstSheet',['Zone','Rent Price (€)','Surface','Price per m^2 (€)','Number of Rooms','Link'],rent_prices)
