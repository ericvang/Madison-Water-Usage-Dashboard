# the main data is about water usage throughout madison
import pandas as pd
from flask import Flask, request, jsonify, send_file, Response
import time
import re


import matplotlib
# Set the backend to 'Agg'
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

# TODO: Add a comment about your data source
# This main.py is about the Madison water usage throughout the city

app = Flask(__name__)
df = pd.read_csv("main.csv")

# Dictionary to track when users last accessed browse.json
last_access = {}
# List to track visitors to browse.json
visitors = []

# Counters for A/B testing
homepage_visits = 0
donations_from_A = 0
donations_from_B = 0

@app.route('/')
def home():
    global homepage_visits, donations_from_A, donations_from_B
    homepage_visits += 1

    # Alternate between versions A and B for the first 10 visits
    if homepage_visits <= 10:
        if homepage_visits % 2 == 0:
            version = 'A'
            link_color = 'blue'
        else:
            version = 'B'
            link_color = 'red'
    else:
        # Choose the best version based on donations
        if donations_from_A >= donations_from_B:
            version = 'A'
            link_color = 'blue'
        else:
            version = 'B'
            link_color = 'red'

    with open("index.html") as f:
        html = f.read()
    html = html.replace("VERSION", version)
    html = html.replace("COLOR", link_color)

    return html

@app.route('/index.html')
def index():
    return home()

@app.route('/browse.html')
def browse():
    # Convert the dataframe to an HTML table with full float precision
    table_html = df.to_html(float_format='%.10g')

    html = f"""
    <html>
      <head>
        <title>Browse Madison Water Usage Data</title>
      </head>
      <body>
        <h1>Madison Water Usage Data</h1>
        {table_html}
      </body>
    </html>
    """
    return html

@app.route('/browse.json')
def browse_json():
    # Check if the client IP has made a request in the last 60 seconds
    client_ip = request.remote_addr
    current_time = time.time()

    # Add to visitors list if not already there
    if client_ip not in visitors:
        visitors.append(client_ip)

    # Check if rate limit applies
    if client_ip in last_access and current_time - last_access[client_ip] < 60:
        # Return 429 error with Retry-After header
        response = jsonify({"error": "Rate limit exceeded. Try again later."})
        response.status_code = 429
        retry_after = int(60 - (current_time - last_access[client_ip]))
        response.headers["Retry-After"] = str(retry_after)
        return response

    # Update last access time
    last_access[client_ip] = current_time

    # Return the data as JSON
    return jsonify(df.to_dict(orient='records'))

@app.route('/visitors.json')
def get_visitors():
    return jsonify(visitors)

@app.route('/donate.html')
def donate():
    global donations_from_A, donations_from_B
    from_version = request.args.get('from')
    if from_version == 'A':
        donations_from_A += 1
    elif from_version == 'B':
        donations_from_B += 1

    html = """
    <html>
      <head>
        <title>Donate to Madison Water Research</title>
      </head>
      <body>
        <h1>Support Our Madison Water Usage Research</h1>
        <p>Our mission is to track, analyze, and visualize water usage patterns throughout Madison to promote conservation and sustainable water management practices. Your generous donation will help us:</p>
        <ul>
          <li>Develop interactive visualization tools to help residents understand their water consumption</li>
          <li>Create educational programs focused on water conservation for schools and community groups</li>
          <li>Analyze seasonal patterns and identify opportunities for water savings</li>
          <li>Work with city officials to develop data-driven water conservation policies</li>
          <li>Extend our research to study the relationship between water usage and demographic factors</li>
        </ul>
        <p>Water is one of our most precious resources, and understanding how we use it is the first step toward ensuring its sustainability for future generations.</p>
        <p>Every contribution, no matter the size, helps us continue this important work for the Madison community.</p>
        <p>Thank you for considering a donation to our project!</p>
      </body>
    </html>
    """
    return html

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    # Validate email using regex
    if len(re.findall(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{3}$", email)) > 0:
        with open("emails.txt", "a") as f:
            f.write(email + "\n")  # Write email to file
        # Count the number of subscribers
        with open("emails.txt", "r") as f:
            num_subscribed = len(f.readlines())
        return jsonify(f"Thanks, your subscriber number is {num_subscribed}!")
    return jsonify("WRONG EMAIL FORMAT DO BETTER DUMBASS!!")

@app.route("/dashboard1.svg")
def dashboard1():
    fig, ax = plt.subplots()
    ax.hist(df["total_gallons"], bins=50, edgecolor="black")
    ax.set_xlabel("Total Gallons")
    ax.set_ylabel("Frequency")
    ax.set_title(f"Distribution of Total Water Usage with 50 Bins")

    # Save the plot to a BytesIO object
    img_data = io.BytesIO()
    fig.savefig(img_data, format="svg")
    img_data.seek(0)
    
    # Save locally for grading
    fig.savefig("dashboard1.svg", format="svg")
    plt.close(fig)

    # Return the image with the correct Content-Type header
    resp = Response(img_data, mimetype="image/svg+xml")
    resp.headers["Content-Type"] = "image/svg+xml"
    return resp


@app.route("/dashboard2.svg")
def dashboard2():
    fig, ax = plt.subplots()

    # Boxplot comparing residential, commercial, and industrial water usage
    ax.boxplot([df["residential_gallons"], df["commercial_gallons"], df["industrial_gallons"]],
               labels=["Residential", "Commercial", "Industrial"])
    ax.set_ylabel("Gallons")
    ax.set_title("Water Usage by Consumer Type")

    # Save the plot to a BytesIO object
    img_data = io.BytesIO()
    fig.savefig(img_data, format="svg")
    img_data.seek(0)
    
    # Save locally for grading
    fig.savefig("dashboard2.svg", format="svg")
    plt.close(fig)

    # Return the image with the correct Content-Type header
    resp = Response(img_data, mimetype="image/svg+xml")
    resp.headers["Content-Type"] = "image/svg+xml"
    return resp


@app.route("/dashboard3.svg")
def dashboard3():
    fig, ax = plt.subplots()

    # Create a scatter plot for residential vs commercial water usage
    ax.scatter(df["residential_gallons"], df["commercial_gallons"], alpha=0.5)
    ax.set_xlabel("Residential Gallons")
    ax.set_ylabel("Commercial Gallons")
    ax.set_title("Residential vs Commercial Water Usage")

    # Save the plot to a BytesIO object
    img_data = io.BytesIO()
    fig.savefig(img_data, format="svg")
    img_data.seek(0)
    
    # Save locally for grading
    fig.savefig("dashboard3.svg", format="svg")
    plt.close(fig)

    # Return the image with the correct Content-Type header
    resp = Response(img_data, mimetype="image/svg+xml")
    resp.headers["Content-Type"] = "image/svg+xml"
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=8080)

# NOTE: app.run never returns (it runs forever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.