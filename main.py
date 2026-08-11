# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


from datetime import datetime as dt
import pandas as pd
import random
import smtplib
import os

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("namantyagidpsg@gmail.com")
MY_PASSWORD = os.environ.get("skaxpovwlsprhbep")

df = pd.read_csv("./birthdays.csv")
now = dt.now()

receiver_data = df[(df['day'] == now.day) & (df['month'] == now.month)]


if not receiver_data.empty:
    receiver_name = receiver_data.iloc[0, 0]
    receiver_email = receiver_data.iloc[0, 1]

    random_number = random.randint(1, 3)
    with open(f"./letter_templates/letter_{random_number}.txt", mode='r') as file:
        chosen_template = file.read()
        birthday_letter = chosen_template.replace("[NAME]", str(receiver_name))

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(MY_EMAIL, receiver_email, msg=f"Subject:Happy Birthday!\n\n{birthday_letter}")
