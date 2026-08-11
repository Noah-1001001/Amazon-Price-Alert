import os
import time
import random
import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv

load_dotenv()

emailId = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
TARGET_PRICE = 70000

URL = "https://www.amazon.in/dp/B0DSKL9MQ8?ref_=Br_MuCl_QAHzEditorial_en_IN_test_multiAk_1_1_1&pf_rd_r=9V10X8PT41K9AG56P10W&pf_rd_p=03a2cabb-8841-4e5e-bb79-d25cdbb744e6&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=merchandised-search-3&pf_rd_t=&pf_rd_i=1389401031&th=1"

# Hardened production-grade browser signature
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://google.com',
}

# Emulate human lag variations to lower the host firewall trigger risk
time.sleep(random.uniform(1.0, 3.5))

try:
    # Maintain session cookies across the connection handshake
    session = requests.Session()
    response = session.get(url=URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    
    text = response.content.decode('utf-8', errors='ignore')
    soup = BeautifulSoup(text, "html.parser")

    # Anti-Bot Safeguard: Check if Amazon dropped you into a CAPTCHA gate
    if "api-services-support@amazon.com" in text or (soup.title and "Robot Check" in soup.title.get_text()):
        print("Blocked by Amazon Anti-Bot Protection (CAPTCHA page served).")
        with open("captcha_page.html", "w", encoding="utf-8") as f:
            f.write(text)
        exit(1)

    # Multi-selector fallback for dynamic layout distributions
    price_element = soup.find(class_="a-price-whole") or soup.find(class_="a-color-price") or soup.find(id="priceblock_ourprice")
    title_element = soup.find(id="productTitle")

    if not price_element or not title_element:
        print("Failure: Structural elements missing from DOM.")
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(text)
        exit(1)

    # Bulletproof numeric cleanup extraction
    raw_price_text = price_element.get_text().split(".")[0]
    cleaned_digits = "".join(char for char in raw_price_text if char.isdigit())
    
    if not cleaned_digits:
        print(f"Parsing Failure: Could not extract digits from text content: '{price_element.get_text()}'")
        exit(1)
        
    price = float(cleaned_digits)
    product_name = " ".join(title_element.get_text().split())

    print(f"Extracted Product: {product_name}")
    print(f"Current Price Evaluated: ₹{price}")

    if price < TARGET_PRICE:
        msg = f"Subject: Price Drop Alert!\n\n{product_name} \nis now at ₹{price} BUY NOW!\n{URL}"
        # Port 587 with explicit modern SMTP connection handling
        with smtplib.SMTP("smtp.gmail.com", 587) as email:
            email.starttls()
            email.login(user=emailId, password=password)
            email.sendmail(from_addr=emailId, to_addrs=emailId, msg=msg.encode('utf-8'))
        print("Notification dispatch complete.")
    else:
        print(f"Price is still above target limit (Target: ₹{TARGET_PRICE})")

except requests.exceptions.RequestException as net_error:
    print(f"Network transport level connection fault: {net_error}")
except Exception as unexpected_err:
    print(f"Execution runtime error: {unexpected_err}")
