from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import logging
from flask_pywebpush import webpush

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)
DATABASE = "users.db"


# Database initialization
def create_user_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, location TEXT, address TEXT, subscription_info TEXT)"
    )
    conn.commit()
    conn.close()


def insert_user(username, password, location, address):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, location, address) VALUES (?, ?, ?, ?)",
        (username, password, location, address),
    )
    conn.commit()
    conn.close()


# Create the disaster table
def create_disaster_table():
    conn = sqlite3.connect("disaster.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS disaster (username TEXT, signal TEXT, address TEXT, location TEXT)"
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        location = request.form["location"]
        address = request.form["address"]
        password = request.form["password"]
        insert_user(username, password, location, address)
        return redirect(url_for("welcome", username=username))
    return render_template("signup.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        username = request.form["username"]
        password = request.form["password"]

        # Retrieve user details from the database
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            # Verify the password
            stored_password = user[1]
            if password == stored_password:
                print("Login successful")
                return redirect(url_for("welcome", username=username))

        error_message = "Login details incorrect. Please try again."
        logging.debug("User details incorrect.")
        logging.debug(f"Username: {username}")
        logging.debug(f"Password: {password}")
        return render_template("signin.html", error_message=error_message)

    return render_template("signin.html")


@app.route("/welcome")
def welcome():
    username = request.args.get("username")
    return render_template("welcome.html", username=username)


# Route for the checklist page
@app.route("/checklist")
def checklist():
    # Define the checklist items
    checklist_items = [
        {
            "heading": "Severe Weather Alerts",
            "section_items": [
                {
                    "id": "item1",
                    "label": "Sign up for severe weather alerts in your area.",
                }
            ],
        },
        {
            "heading": "Emergency Preparedness",
            "section_items": [
                {"id": "item2", "label": "Program emergency numbers into your phone."},
                {
                    "id": "item3",
                    "label": "Decide on a meeting place for your family to gather.",
                },
                {
                    "id": "item4",
                    "label": "Plan escape routes from your home and neighborhood. Remember, roads could be blocked in large-scale disasters. Have at least one alternate route — or more if possible.",
                },
                {
                    "id": "item5",
                    "label": "Be sure all adult and teenage family members know how to shut off gas, electric and water lines if there's a leak or electrical short. Keep the necessary tools easily accessible, and make sure everyone knows where these are.",
                },
                {
                    "id": "item6",
                    "label": "Consider learning CPR and first aid training.",
                },
                {
                    "id": "item7",
                    "label": "Remember your pets. Bring dogs and cats inside during a catastrophe or make a plan for how you'll evacuate with them. Make sure they have ID tags.",
                },
            ],
        },
        {
            "heading": "Emergency Kit",
            "section_items": [
                {
                    "id": "item8",
                    "label": "Drinking water (at least one gallon per person per day)",
                },
                {
                    "id": "item9",
                    "label": "Nonperishable food, such as canned veggies and protein bars",
                },
                {"id": "item10", "label": "Manual can opener"},
                {
                    "id": "item11",
                    "label": "Flashlights or portable lanterns and extra batteries",
                },
                {"id": "item12", "label": "First aid kit"},
                {"id": "item13", "label": "A crank- or battery-powered radio"},
                {
                    "id": "item14",
                    "label": "Sanitation supplies: toilet paper, moist towelettes, soap, trash bags and disinfectants",
                },
                {"id": "item15", "label": "Local maps"},
                {
                    "id": "item16",
                    "label": "Depending on your situation, your kit might also include:",
                },
                {"id": "item17", "label": "- Baby food, bottles and diapers"},
                {"id": "item18", "label": "- Pet food"},
                {"id": "item19", "label": "- Prescription medications"},
                {
                    "id": "item20",
                    "label": "- Extra eyeglasses or contact lenses and solution",
                },
                {"id": "item21", "label": "- Dry clothing and blankets"},
            ],
        },
        {
            "heading": "Evacuation Plan",
            "section_items": [
                {"id": "item22", "label": "Where to shelter"},
                {"id": "item23", "label": "A route for evacuation"},
                {"id": "item24", "label": "Getting emergency alerts and warnings"},
                {"id": "item25", "label": "Family communication"},
                {"id": "item26", "label": "Conditions that make evacuations necessary"},
                {
                    "id": "item27",
                    "label": "Chains of command that clearly designate roles and responsibilities during an evacuation",
                },
                {
                    "id": "item28",
                    "label": "Instructions the public receives about how and when to evacuate",
                },
                {"id": "item29", "label": "Evacuation routes"},
                {
                    "id": "item30",
                    "label": "Using different channels of communication with community members, such as social media, print media, television, and radio",
                },
                {
                    "id": "item31",
                    "label": "Coordinating with utility companies to include evacuation maps alongside utility bills or posting major and alternate evacuation routes on government websites",
                },
                {
                    "id": "item32",
                    "label": "Emergency and rescue equipment (life vests, rescue trucks, emergency lighting)",
                },
                {
                    "id": "item33",
                    "label": "Personal safety and protection gear (respiratory masks, safety helmets, fire-retardant footwear)",
                },
                {
                    "id": "item34",
                    "label": "Food and cooking supplies (preserved foods, disposable kitchenware)",
                },
                {
                    "id": "item35",
                    "label": "Cleanup and rebuilding products (water treatments, disinfecting solutions, waste containers)",
                },
                {
                    "id": "item36",
                    "label": "Familiarizing emergency management teams with the procedures of the plan",
                },
                {"id": "item37", "label": "Identifying training needs"},
                {
                    "id": "item38",
                    "label": "Assessing the effectiveness of the plan in practice",
                },
                {"id": "item39", "label": "Clarifying roles"},
                {"id": "item40", "label": "Correct use of equipment"},
                {"id": "item41", "label": "Specific skills"},
                {"id": "item42", "label": "Adherence to specific policies"},
            ],
        },
    ]

    return render_template("checklist.html", checklist_items=checklist_items)


# Route for the store page
@app.route("/store")
def store():
    # Retrieve the username from the query parameters
    username = request.args.get("username")
    # Pass the username as a parameter to the store.html template
    return render_template("store.html", username=username)


# Route for the beacon page
@app.route("/beacon", methods=["GET", "POST"])
def beacon():
    username = request.args["username"]
    if request.method == "POST":
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user:
            password = user[1]
            location = user[2]
            address = user[3]
        signal = request.form["signal"]
        subscription_info = request.form.get("subscription_info")
        store_distress_signal(username, signal, address, location)
        send_browser_notification(
            username, signal, address, location, subscription_info
        )
        logging.debug("Stored distress signal and sent browser notification.")
        return redirect("/welcome?username=" + username)
    return render_template("beacon.html", username=username)


def retrieve_user_data(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT location, address FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    if result:
        location, address = result
        return location, address
    return None, None


# Store the distress signal, username, address, and location in the disaster.db database
def store_distress_signal(username, signal, address, location):
    logging.debug(
        f"Storing distress signal: {signal}, username: {username}, address: {address}, location: {location}"
    )
    conn = sqlite3.connect("disaster.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO disaster (username, signal, address, location) VALUES (?, ?, ?, ?)",
        (username, signal, address, location),
    )
    conn.commit()
    conn.close()


# Send a browser notification to the user with the distress signal, address, and location
def send_browser_notification(username, signal, address, location, subscription_info):
    logging.debug(
        f"Sending browser notification to {username}: {signal}, {address}, {location}, {subscription_info}"
    )
    if subscription_info:
        try:
            webpush(
                subscription_info,
                data=signal,
                vapid_private_key="your_vapid_private_key",
                vapid_claims={"sub": "mailto:your_email@example.com"},
            )
            logging.debug("Browser notification sent successfully.")
        except Exception as e:
            logging.debug("Error sending browser notification:", str(e))
    else:
        logging.debug("Subscription info not provided.")


if __name__ == "__main__":
    create_user_table()
    create_disaster_table()
    app.run()
