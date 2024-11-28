import csv
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import ssl

url = set()
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def phone_numbers(body):
    phone_pattern = re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b')
    phone_numbers = phone_pattern.findall(body)
    return set(phone_numbers)

def email_addresses(text):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    email_addresses = email_pattern.findall(text)
    return set(email_addresses)

def data(body, output_file):
    phone_numbers = phone_numbers(body)
    if phone_numbers:
        save_data(phone_numbers, f"{output_file}_phone_numbers.txt")
    
    email_addresses = email_addresses(body)
    if email_addresses:
        save_data(email_addresses, f"{output_file}_email_addresses.txt")

def save_data(data, file):
    with open(file, 'a') as f:
        for item in data:
            if not item_exists(item, file):
                f.write(f"{item}\n")

def item_exists(item, file):
    try:
        with open(file, 'r') as f:
            return any(item.strip() == line.strip() for line in f)
    except FileNotFoundError:
        return False

def crawl_page(url, output_file, depth=3):
    if depth == 0 or url in url:
        return
    url.add(url)
    try:
        with urlopen(url, context=ssl_context) as response:
            body = response.read().decode('utf-8')
            data(body, output_file)
        soup = BeautifulSoup(body, 'html.parser')
        links = (urljoin(url, a['href']) for a in soup.find_all('a', href=True))
        for link in links:
            crawl_page(link, output_file, depth - 1)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

def process_urls(input_csv, output_file):
    with open(input_csv, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            url = row[0]
            print(f"Processing URL: {url}")
            crawl_page(url, output_file)

if __name__ == '__main__':
    input_csv = input("Enter the input CSV file name: ")
    output_file_prefix = input("Enter the output file prefix: ")
    process_urls(input_csv, output_file_prefix)
