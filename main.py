import smtplib
import datetime
from pymongo import MongoClient

# Information about the email sender and receiver and the app password to access the sender email
EMAIL_RECEIVER = "ENTER_YOUR_PHONE_NUMBER_AS_AN_EMAIL"
EMAIL_SENDER = "EMAIL_YOU_SEND_WORKOUTS_FROM"
EMAIL_PASSWORD = "APP_PASSWORD_FOR_SENDER_EMAIL"

# MongoDB connection details
MONGO_URI = "mongodb://your_mongo_db_uri"
DB_NAME = "your_db_name"
COLLECTION_NAME = "your_collection_name"

# Establish connection to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Checks how many days have passed from any starting date to see what workout is scheduled for today
today = datetime.date.today()
days_passed = (today - datetime.date(2024, 2, 27)).days
workout_index = days_passed % 6

# Query the workout for the day from MongoDB
workout_doc = collection.find_one({"day": workout_index})

if workout_doc:
    workout = workout_doc.get("workout_name", "Unknown Workout")
    workout_list = workout_doc.get("exercises", [])
else:
    workout = "No Workout Found"
    workout_list = ["No exercises found for today."]

# Converts the message from a list to a string with each workout on a new line
sep = "\n"
message = sep.join(workout_list)

connection = smtplib.SMTP('smtp.gmail.com', 587)
connection.starttls()

# Tries logging in to the email and sending email, throws error if any exception, closes connection at the end
try:
    connection.login(EMAIL_SENDER, EMAIL_PASSWORD)
    connection.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, f"Subject:{workout}\n\n\n{message}")
    print("Email sent successfully!")
except Exception as e:
    print("An error occurred:", e)
finally:
    connection.close()
