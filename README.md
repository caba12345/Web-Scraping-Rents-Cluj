## Project Overview
This Python script is designed to scrape rental property data from the Storia website for apartments in Cluj-Napoca, Romania. It gathers information such as rental price, surface area, number of rooms, and calculates the price per square meter. The collected data is then stored in an Excel file.

## Functionality
1. **Web Scraping:** Utilizes the `requests` library to fetch HTML content from Storia, and `BeautifulSoup` for parsing the HTML content.
2. **Data Extraction:** Extracts relevant information including zone, rental price, surface area, number of rooms, and hyperlink.
3. **Data Conversion:** Converts rental prices from Romanian Leu (RON) to Euro (EUR) if necessary.
4. **Excel File Generation:** Generates an Excel spreadsheet with the extracted data, using the `xlsxwriter` library.
5. **User Interaction:** The user can specify target zones and the number of pages to scrape.

## Requirements
- Python 3.x
- Required Python libraries: `requests`, `bs4` (BeautifulSoup), `xlsxwriter`

## Usage
1. Clone or download the script to your local machine.
2. Make sure you have Python installed.
3. Install the required libraries using pip:
    ```
    pip install requests beautifulsoup4 xlsxwriter
    ```
4. Modify the target zones and the number of pages to scrape as per your requirements in the `if __name__ == '__main__':` section.
5. Run the script:
    ```
    python script_name.py
    ```
6. The script will print the extracted data to the console and generate an Excel file named `RentCluj.xlsx` containing the data.

## Disclaimer
- This script is intended for educational purposes only.
- Use responsibly and ensure compliance with website terms of service and legal regulations.
- The accuracy and reliability of the data retrieved depend on the website structure and stability, which may change over time.
