# Design Decisions

## Problem Interpretation

Prompt: Build a CLI seat reservation system for an airline with a fixed plane configuration: 20 rows (A–T), 8 seats per row, layout `| xx _ xxxx _ xx |` (positions 0–7).

Main ambiguity: "consecutive seats." I defined this as consecutive *within a section*, not across aisles. Example: `BOOK A1 2` fails because it would span the aisle. This rule applies symmetrically to booking and canceling, operations must respect section boundaries.

## Implementation

### File Storage

State is persisted as plain text, one seat per line. With only 160 seats, JSON or a database would be needless overhead. Writes use `tempfile.mkstemp()` + `os.replace()` for atomic updates so the file is never half-written.

### Data Structures

- **In-memory:** Python `set` for O(1) lookup and uniqueness.  
- **Sections:** Defined as `[(0,1), (2,5), (6,7)]` for simple boundary checks.  

### Reservation Logic

1. Identify the section for the requested seat.  
2. Check that `start + count - 1` is within the section.  
3. Verify each seat is available (for BOOK) or reserved (for CANCEL).  
4. If all checks pass, commit. Otherwise, fail. No partial operations.  

### Error Handling

- **Business failures** (seat already booked, crossing aisle, invalid range): print `FAIL` to STDOUT, exit 0.  
- **Program errors** (bad input format, invalid seat ID, file issues): message to STDERR, exit 1.  

This separation avoids mixing user logic errors with system errors.  

## Trade-offs and Scope

- **No file locking:** Parallel writers could clash, but concurrency was not in scope.  
- **No customer IDs:** The system only tracks which seats are reserved, not by whom.  
- **Idempotency:** Double-booking or double-canceling fails cleanly.  
- **Audit/history:** None. Reservations disappear once canceled. Acceptable at this scale.  
- **Scalability:** Fits easily in memory for 160 seats. For larger systems a database would be required.  
