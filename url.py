import csv
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def save_link(root_url, output_csv):
    try:
        with urlopen(root_url, context=ssl_context) as response:
            body = response.read().decode('utf-8')
        soup = BeautifulSoup(body, 'html.parser')
        links = {urljoin(root_url, a['href']) for a in soup.find_all('a', href=True)}
        
        with open(output_csv, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["URL"])  # Header row
            for link in links:
                writer.writerow([link])
        print(f"Extracted {len(links)} links and saved to {output_csv}")
    except Exception as e:
        print(f"Error fetching {root_url}: {e}")

if __name__ == '__main__':
    root_url = input("Enter the root URL: ")
    output_csv = input("Enter the output CSV file name: ")
    save_link(root_url, output_csv)
