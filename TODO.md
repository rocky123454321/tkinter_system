# TODO - Sidebar & Booking UI refactor

## Goal
User sidebar should have only 3 buttons: Dashboard, Booking, Rooms. Rooms and Booking should be shown together in right side flow. Booking form should have NO dropdown; user should pick room by clicking a room card (Rooms list).

## Steps
- [ ] Update `views/components/user_sidebar.py` to only include 3 nav buttons: Dashboard, Booking, Rooms.
- [ ] Update `views/components/user/booking_form.py` to remove the Room Number dropdown/OptionMenu and instead show room selection as read-only text/label (based on `selected_room_number`) or an entry without dropdown.
- [ ] Update `views/pages/user/user_dashboard.py` so clicking Rooms sets the `selected_room_number_holder` and directly renders Booking form with that room (no dropdown selection).
- [ ] Ensure edge-cases: if user opens Booking without selecting a room, show a warning or prompt to go to Rooms.
- [ ] Run the app (`python main.py`) to smoke test navigation (Dashboard <-> Rooms -> Booking) and confirm booking works.

