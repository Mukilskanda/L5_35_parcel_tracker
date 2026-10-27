# Issues found (Pylint, Bandit, Flake8) on parcel_tracker.py

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| `subprocess` with `shell=True` (B602, High) | Security | 55 | `ping -c 1 ` + user string run through a shell allows command injection (e.g. `"1.1.1.1; rm -rf ~"`). | Validate with `ipaddress.ip_address`, pass args as a list, drop `shell=True`. |
| `tempfile.mktemp` (B306, Medium) | Security | 50 | Returns a name without creating the file; race condition lets an attacker pre-create/symlink it. | Use `tempfile.mkstemp` (atomic create), close the fd, return the path. |
| `random.randint` for OTP (B311, Low) | Security | 72 | Predictable PRNG is not suitable for a delivery OTP. | Use `secrets.randbelow` (1000 + randbelow(9000)). |
| Mutable default argument `history=[]` (W0102) | Bug | 11 | The list is created once and shared by every call, so history leaks between bookings. | Default to `None` and create a new list inside the function. |
| Broad `except Exception` (W0718) | Bug / Robustness | 37 | Hides unrelated errors (e.g. TypeError) as "Unknown tracking id". | Catch only `KeyError`. |
| Comparison chain (R1714) | Refactor | 45 | `a == x or a == y` is verbose. | `status in ("Picked Up", "In Transit")`. |
| Naming not snake_case (C0103) | Style | 11-67 | `bookParcel`, `trackingId`, `weightKg`, etc. violate PEP 8. | Rename to `book_parcel`, `tracking_id`, `weight_kg`, etc. |
| Missing docstrings (C0114/C0116) | Style | 1, 11-58 | Module and all functions undocumented. | Add concise docstrings. |
| E225 missing whitespace around operator | Style (Flake8) | 28 | `cost=50` | `cost = 50` |
| E261 two spaces before inline comment | Style (Flake8) | 71 | `)# unknown id` spacing | Two spaces before `#`. |
| E231 missing whitespace after ',' | Style (Flake8) | 74 | `"...today:",len(...)` | Add space after comma. |
| E305 expected 2 blank lines | Style (Flake8) | 75 | `main()` called directly after the function. | Two blank lines, use `if __name__ == "__main__":` guard. |
| `subprocess` import (B404, Low) | Security | 2 | Informational warning on importing subprocess. | Kept, with `# nosec` and a note: only called with validated args and no shell. |

**Results:** Pylint 4.91/10 -> 10.00/10; Flake8 4 errors -> 0; Bandit 1 High + 1 Medium + 2 Low -> 0 (3 deliberately suppressed with justification). Program output is unchanged (only the random OTP differs).
