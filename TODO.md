# TODO

- [ ] (Plan confirmed) Update user booking confirmation flow to reset selected room after success.
- [ ] Implement reset in `views/components/user/booking_form.py` via callback or return value.
- [ ] Update `views/pages/user/user_dashboard.py` to clear `selected_room_number_holder["room"]` and rerender Rooms view after booking success.
- [ ] Quick manual test: select available room, confirm reservation, verify room selection cleared and room list updates.

