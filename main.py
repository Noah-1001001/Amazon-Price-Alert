import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import smtplib

load_dotenv()

emailId = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
TARGET_PRICE = 70000

URL = "https://www.amazon.in/dp/B0DSKL9MQ8?ref_=Br_MuCl_QAHzEditorial_en_IN_test_multiAk_1_1_1&pf_rd_r=9V10X8PT41K9AG56P10W&pf_rd_p=03a2cabb-8841-4e5e-bb79-d25cdbb744e6&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=merchandised-search-3&pf_rd_t=&pf_rd_i=1389401031&th=1"

response = requests.get(url=URL, headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                        "Chrome/151.0.0.0 Safari/537.36", "Accept-Language": "en-US"})
text = response.content.decode('utf-8', errors='ignore')

soup = BeautifulSoup(text, "html.parser")

price = float(soup.find(class_="a-price-whole").get_text().split(".")[0].strip().replace(",",""))
product_name = " ".join(soup.find(id="productTitle").get_text().split())


if price < TARGET_PRICE:
    msg = f"Subject: Price Drop Alert!\n\n{product_name} \nis now at ₹{price} BUY NOW!\n{URL}"
    try:
        with smtplib.SMTP("smtp.gmail.com") as email:
            email.starttls()
            email.login(user=emailId, password=password)
            email.sendmail(from_addr=emailId, to_addrs=emailId, msg=msg.encode('utf-8'))
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


