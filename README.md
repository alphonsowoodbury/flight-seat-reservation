# Flight Seat Reservation System

Command-line tool for managing flight seat reservations on a single plane configuration.

## Requirements

- Python 3.6+
- Linux environment

## Installation

Clone the repository and make the script executable:

```bash
git clone https://github.com/alphonsowoodbury/flight-seat-reservation
cd flight-seat-reservation
chmod +x reservation.py
```

## Usage

```bash
./reservation.py [ACTION] [SEAT] [COUNT]
```

- **ACTION**: `BOOK` or `CANCEL`
- **SEAT**: Row letter (A-T) + position number (0-7), e.g., `A0`, `B5`
- **COUNT**: Number of consecutive seats to book/cancel

## Plane Configuration

- 20 rows (A through T)
- 8 seats per row (positions 0-7)
- Layout: `| xx _ xxxx _ xx |`
  - Positions 0-1: Left section
  - Positions 2-5: Middle section
  - Positions 6-7: Right section

## Example Usage

```bash
# Book 2 seats in left section
./reservation.py BOOK A0 2
SUCCESS

# Try to book across aisle (fails - aisle between positions 1 and 2)
./reservation.py BOOK A1 2
FAIL

# Book 4 seats in middle section
./reservation.py BOOK A2 4
SUCCESS

# Try to book seats that cross sections (fails)
./reservation.py BOOK A5 3
FAIL

# Try to book already reserved seat
./reservation.py BOOK A2 1
FAIL

# Cancel reserved seats
./reservation.py CANCEL A0 2
SUCCESS

# Try to cancel unreserved seats
./reservation.py CANCEL A0 1
FAIL

# Invalid input examples (errors go to stderr)
./reservation.py BOOK Z9 1
Error: Invalid seat format

./reservation.py BOOK A1 0
Error: COUNT must be a valid integer greater than 0
```

## Output

- **SUCCESS**: Operation completed successfully
- **FAIL**: Operation could not be completed (seat unavailable, invalid consecutive range, etc.)
- Error messages go to STDERR for invalid inputs

## Storage

Reservations are stored in `reservations.txt` in the current directory. Each line contains one reserved seat ID.

## Design Decisions

See [DESIGN.md](DESIGN.md) for detailed information about implementation choices and trade-offs.
