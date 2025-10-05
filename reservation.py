#!/usr/bin/env python3

import sys
import os
import tempfile

ROWS = 'ABCDEFGHIJKLMNOPQRST'  # 20 rows
SECTIONS = [(0, 1), (2, 5), (6, 7)]  # xx _ xxxx _ xx
RESERVATION_FILE = 'reservations.txt'


def load_reservations():
    reserved = set()
    if os.path.exists(RESERVATION_FILE):
        with open(RESERVATION_FILE, 'r') as f:
            for line in f:
                seat = line.strip()
                if seat:
                    reserved.add(seat)
    return reserved


def save_reservations(reserved_seats):
    dir_name = os.path.dirname(RESERVATION_FILE) or '.'
    fd, tmp_filename = tempfile.mkstemp(dir=dir_name, text=True)

    try:
        with os.fdopen(fd, 'w') as tmp_file:
            for seat in sorted(reserved_seats):
                tmp_file.write(f"{seat}\n")

        os.replace(tmp_filename, RESERVATION_FILE)
    except:
        try:
            os.unlink(tmp_filename)
        except:
            pass
        raise

def parse_seat_request(request):

    if len(request) < 2:
        return None, None

    row = request[0]
    seat_number_str = request[1:]

    if row not in ROWS:
        return None, None

    try:
        seat_number = int(seat_number_str)
        if not (0 <= seat_number <= 7):
            return None, None
    except ValueError:
        return None, None

    return row, seat_number

def get_section(seat_number):
    for start, end in SECTIONS:
        if start <= seat_number <= end:
            return (start, end)
    return None


def evaluate_reservation(reserved_seats, row, starting_seat, count, action):
    section = get_section(starting_seat)
    if not section:
        return False, []

    start, end = section
    if starting_seat + count - 1 > end:
        return False, []

    seats = []
    for i in range(count):
        seat = f"{row}{starting_seat+i}"
        seats.append(seat)

        if action == 'BOOK' and seat in reserved_seats:
            return False, []
        elif action == 'CANCEL' and seat not in reserved_seats:
            return False, []

    return True, seats


def main():

    # Capture, parse, and validate arguments
    if len(sys.argv) < 4:
        print("Usage: reservation.py [ACTION] [SEAT] [COUNT]", file=sys.stderr)
        sys.exit(1)

    action = sys.argv[1].upper()
    seat_request = sys.argv[2].upper()

    try:
        count = int(sys.argv[3])
        if count < 1:
            raise ValueError()
    except ValueError:
        print("Error: COUNT must be a valid integer greater than 0", file=sys.stderr)
        sys.exit(1)

    if action not in ['BOOK','CANCEL']:
        print(f"Error: Unknown action '{action}'", file=sys.stderr)
        sys.exit(1)


    reserved_seats = load_reservations()

    row, seat_number = parse_seat_request(seat_request)
    if row is None or seat_number is None:
        print("Error: Invalid seat format", file=sys.stderr)
        sys.exit(1)


    success, seats = evaluate_reservation(reserved_seats, row, seat_number, count, action)

    if success:
        if action == 'BOOK':
            reserved_seats.update(seats)
        else:
            reserved_seats.difference_update(seats)

        save_reservations(reserved_seats)
        print("SUCCESS")
    else:
        print("FAIL")


if __name__ == '__main__':
    main()
