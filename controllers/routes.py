from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models.models import db, User, ParkingLot, ParkingSpot, Reservation
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Home page ka route
@app.route('/')
def home():
    return render_template('home.html')

# Login ka route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

# Register ke liye route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        address = request.form['address']
        pin_code = request.form['pin_code']
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, fullname=fullname, address=address, pin_code=pin_code)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Logout ka route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out!')
    return redirect(url_for('home'))

# Admin Dashboard ke liye route
@app.route('/admin')
def admin_dashboard():
    lots = ParkingLot.query.all()
    for lot in lots:
        lot.spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
        lot.occupied_count = sum(1 for s in lot.spots if s.is_occupied)
    return render_template('admin_dashboard.html', lots=lots)

# Admin Add Lot
@app.route('/admin/add_lot', methods=['GET', 'POST'])
def add_lot():
    if request.method == 'POST':
        name = request.form['prime_location_name']
        price = request.form['price']
        address = request.form['address']
        pin_code = request.form['pin_code']
        max_spots = request.form['maximum_number_of_spots']
        lot = ParkingLot(prime_location_name=name, price=price, address=address, pin_code=pin_code, maximum_number_of_spots=max_spots)
        db.session.add(lot)
        db.session.commit()
        for i in range(1, int(max_spots) + 1):
            spot = ParkingSpot(lot_id=lot.id, spot_number=str(i), is_occupied=False)
            db.session.add(spot)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_add_lot.html')

# Admin Edit Lot
@app.route('/admin/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
def admin_edit_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    if request.method == 'POST':
        lot.prime_location_name = request.form['prime_location_name']
        lot.address = request.form['address']
        lot.pin_code = request.form['pin_code']
        lot.price = int(request.form['price'])
        lot.maximum_number_of_spots = int(request.form['maximum_number_of_spots'])
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit_lot.html', lot=lot)

# Admin Delete Lot
@app.route('/admin/delete_lot/<int:lot_id>', methods=['POST'])
def admin_delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id, is_occupied=True).count()
    if spots == 0:
        ParkingSpot.query.filter_by(lot_id=lot.id).delete()
        db.session.delete(lot)
        db.session.commit()
        flash('Parking lot deleted!', 'success')
    else:
        flash('Cannot delete lot: Some spots are still occupied!', 'danger')
    return redirect(url_for('admin_dashboard'))

# Admin View Spots
@app.route('/admin/view_spots/<int:lot_id>')
def admin_view_spots(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    return render_template('admin_view_spots.html', lot=lot, spots=spots)

# Admin Spot Details
@app.route('/admin/spot_details/<int:spot_id>')
def admin_spot_details(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    reservation = Reservation.query.filter_by(spot_id=spot_id, status='parked').first()
    return render_template('admin_spot_details.html', spot=spot, reservation=reservation)

# Admin Users
@app.route('/admin/users')
def admin_users():
    users = User.query.filter(User.role != 'admin').all()
    return render_template('admin_users.html', users=users)

# Admin Search
@app.route('/admin/search', methods=['GET'])
def admin_search():
    search = request.args.get('search', '')
    results = ParkingLot.query.filter(ParkingLot.prime_location_name.contains(search)).all() if search else []
    return render_template('admin_search.html', results=results)

# Admin Summary
@app.route('/admin/summary')
def admin_summary():
    return render_template('admin_summary.html')

# User Dashboard
@app.route('/user_dashboard')
def user_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    user = User.query.get_or_404(user_id)
    reservations = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.timestamp.desc()).all()
    for r in reservations:
        r.spot = ParkingSpot.query.get(r.spot_id)
        r.lot = ParkingLot.query.get(r.spot.lot_id) if r.spot else None
    return render_template('user_dashboard.html', user=user, reservations=reservations)

# Book Parking 
@app.route('/book_parking/<int:lot_id>', methods=['GET', 'POST'])
def book_parking(lot_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    user = User.query.get_or_404(user_id)
    lot = ParkingLot.query.get_or_404(lot_id)
    spot = ParkingSpot.query.filter_by(lot_id=lot.id, is_occupied=False).first()
    if not spot:
        flash('No available spots in this lot.', 'danger')
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST':
        vehicle_no = request.form['vehicle_no']
        spot.is_occupied = True
        reservation = Reservation(user_id=user.id, spot_id=spot.id, vehicle_no=vehicle_no, status='parked')
        db.session.add(reservation)
        db.session.commit()
        flash('Spot booked successfully!', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('book_user.html', spot=spot, lot=lot, user=user)

# Release Parking 
@app.route('/release_parking/<int:reservation_id>', methods=['GET', 'POST'])
def release_parking(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    if reservation.status != 'parked':
        flash('Already released.', 'info')
        return redirect(url_for('user_dashboard'))
    spot = ParkingSpot.query.get(reservation.spot_id)
    if request.method == 'POST':
        reservation.status = 'parked_out'
        spot.is_occupied = False
        db.session.commit()
        flash('Parking released!', 'success')
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST':
        reservation = Reservation.query.get(reservation_id)
        reservation.status = 'released'
        reservation.releasing_time = datetime.now()
        reservation.total_cost = reservation.calculate_total_cost()
        db.session.commit()
        flash('Parking spot released successfully!', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('release_user.html', reservation=reservation)

# Edit Profile
@app.route('/edit_profile')
def edit_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    user = User.query.get_or_404(user_id)
    return render_template('edit_profile.html', user=user)

# User Search
@app.route('/user_search', methods=['GET'])
def user_search():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    user = User.query.get_or_404(user_id)
    search = request.args.get('search', '')
    from sqlalchemy import or_
    lots = ParkingLot.query.filter(
        or_(
            ParkingLot.prime_location_name.contains(search),
            ParkingLot.address.contains(search),
            ParkingLot.pin_code.contains(search)
        )
    ).all() if search else []
    for lot in lots:
        total_spots = lot.maximum_number_of_spots
        occupied = ParkingSpot.query.filter_by(lot_id=lot.id, is_occupied=True).count()
        lot.available_spots = total_spots - occupied
    return render_template('user_search.html', user=user, lots=lots, search=search)
