from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime


app = Flask(__name__)

# Sample bus data
buses = [
    {"id": 1, "name": "GreenLine AC Sleeper", "type": "AC Sleeper", "seats": 30, "price": 1200, "source": "City A", "destination": "City X"},
    {"id": 2, "name": "BlueStar Express", "type": "Non-AC Sleeper", "seats": 40, "price": 900, "source": "City A", "destination": "City X"},
    {"id": 3, "name": "Comfort Travels", "type": "AC Seater", "seats": 35, "price": 1100, "source": "City B", "destination": "City Y"},
    {"id": 4, "name": "RapidRide Deluxe", "type": "Sleeper", "seats": 28, "price": 1000, "source": "City A", "destination": "City Z"},
    {"id": 5, "name": "CityConnect", "type": "Seater", "seats": 40, "price": 800, "source": "City B", "destination": "City X"},
    {"id": 6, "name": "MetroLink AC", "type": "AC Seater", "seats": 32, "price": 1150, "source": "City A", "destination": "City X"},
    {"id": 7, "name": "SuperFast Bus Co.", "type": "AC Sleeper", "seats": 30, "price": 1250, "source": "City C", "destination": "City Y"},
    {"id": 8, "name": "EcoBus Express", "type": "Non-AC Seater", "seats": 45, "price": 750, "source": "City B", "destination": "City Z"},
    {"id": 9, "name": "Royal Roadlines", "type": "Luxury Sleeper", "seats": 25, "price": 1500, "source": "City A", "destination": "City Y"},
    {"id": 10, "name": "Urban Traveller", "type": "Mini Bus", "seats": 20, "price": 700, "source": "City C", "destination": "City Z"}
]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # For now, just a simple check (you can enhance this)
        if username == 'admin' and password == 'admin':
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/select_route', methods=['GET', 'POST'])
def select_route():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        return redirect(url_for('available_buses', source=source, destination=destination))
    return render_template('select_route.html')

@app.route('/available_buses')
def available_buses():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination:
        return redirect(url_for('select_route'))

    # Just show all buses ignoring route
    filtered_buses = buses

    return render_template('available_buses.html', buses=filtered_buses, source=source, destination=destination)

@app.route('/all_buses')
def all_buses():
    return render_template('all_buses.html', buses=buses)

# List to store bookings
bookings = []

@app.route('/book/<int:bus_id>', methods=['GET', 'POST'])
def book(bus_id):
    bus = next((b for b in buses if b["id"] == bus_id), None)
    if not bus:
        return "Bus not found", 404

    if request.method == 'POST':
        passenger_name = request.form.get('passenger_name')
        travel_date = request.form.get('travel_date')
        if not passenger_name or not travel_date:
            return "Missing details", 400

        pnr = f"PNR{bus_id}{datetime.now().strftime('%H%M%S')}"

        bookings.append({
            "pnr": pnr,
            "bus_id": bus_id,
            "passenger_name": passenger_name,
            "travel_date": travel_date
        })

        return redirect(url_for('booking_confirmation', pnr=pnr))

    return render_template('booking.html', bus=bus)

@app.route('/booking_confirmation')
def booking_confirmation():
    pnr = request.args.get('pnr')
    if not pnr:
        return "PNR not found", 400

    booking = next((b for b in bookings if b['pnr'] == pnr), None)
    if not booking:
        return "Booking not found", 404

    bus = next((b for b in buses if b['id'] == booking['bus_id']), None)

    return render_template('booking_confirmation.html', booking=booking, bus=bus)
@app.route('/view_bookings')
def view_bookings():
    full_bookings = []
    for b in bookings:
        bus = next((bus for bus in buses if bus['id'] == b['bus_id']), None)
        if bus:
            full_bookings.append({
                "bus_id": bus["id"],
                "bus_name": bus["name"],
                "type": bus["type"],
                "source": bus["source"],
                "destination": bus["destination"],
                "passenger_name": b["passenger_name"],
                "travel_date": b["travel_date"],
                "pnr": b["pnr"]
            })
    return render_template("view_bookings.html", bookings=full_bookings)
@app.route('/cancel_ticket', methods=['GET', 'POST'])
def cancel_ticket():
    message = None
    if request.method == 'POST':
        pnr = request.form.get('pnr')
        global bookings
        initial_count = len(bookings)
        bookings = [b for b in bookings if b["pnr"] != pnr]
        if len(bookings) < initial_count:
            message = f"Ticket with PNR {pnr} has been cancelled successfully."
        else:
            message = "PNR not found. Please check and try again."

    return render_template('cancel_ticket.html', message=message)


if __name__ == '__main__':
    app.run(debug=False,port=7004)
