import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'businesses.db')


class Business:
    def __init__(self, name, category, address, city, phone, email, website, description):
        self.id          = None          # set after DB insert
        self.name        = name
        self.category    = category
        self.address     = address
        self.city        = city
        self.phone       = phone
        self.email       = email
        self.website     = website
        self.description = description
        self.created_at  =  datetime.now()

    def get_summary(self):
        """Return a one-line summary of the business."""
        location = f"{self.address}, {self.city}" if self.address else self.city
        return f"{self.name} | {self.category} | {location}"

    def formatted_date(self):
        """Return created_at as a human-readable string."""
        return self.created_at.strftime("%A, %d %B %Y at %I:%M %p")

    def to_dict(self):
        """Return all fields as a plain dictionary."""
        return {
            "id":          self.id,
            "name":        self.name,
            "category":    self.category,
            "address":     self.address,
            "city":        self.city,
            "phone":       self.phone,
            "email":       self.email,
            "website":     self.website,
            "description": self.description,
            "created_at":  self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Business id={self.id} name={self.name!r}>"



class RecentlyAddedStack:
    MAX_SIZE = 5

    def __init__(self):
        self._stack = []

    def push(self, business):
        """Add a Business to the top of the stack (max 5 kept)."""
        self._stack.append(business)
        if len(self._stack) > self.MAX_SIZE:
            self._stack.pop(0)          # drop oldest when over capacity

    def undo_last(self):
        """Remove and return the most recently added Business."""
        if not self._stack:
            return None
        return self._stack.pop()

    def peek(self):
        """Return all entries newest-first (does not modify the stack)."""
        return list(reversed(self._stack))

    def __len__(self):
        return len(self._stack)



def init_db():
    """Create the businesses table if it does not already exist."""
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS businesses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            category    TEXT NOT NULL,
            address     TEXT,
            city        TEXT NOT NULL,
            phone       TEXT,
            email       TEXT,
            website     TEXT,
            description TEXT,
            created_at  TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()


def _row_to_business(row):
    """Convert a sqlite3 Row tuple into a Business object."""
    biz = Business(
        name        = row[1],
        category    = row[2],
        address     = row[3],
        city        = row[4],
        phone       = row[5],
        email       = row[6],
        website     = row[7],
        description = row[8],
    )
    biz.id         = row[0]
    biz.created_at = datetime.fromisoformat(row[9])
    return biz


def get_all_businesses(search="", category=""):
    """Return a list of Business objects, optionally filtered."""
    con = sqlite3.connect(DB_PATH)
    sql = "SELECT * FROM businesses WHERE 1=1"
    params = []

    if search:
        sql += " AND (name LIKE ? OR description LIKE ? OR city LIKE ?)"
        like = f"%{search}%"
        params += [like, like, like]

    if category:
        sql += " AND category = ?"
        params.append(category)

    sql += " ORDER BY name"
    rows = con.execute(sql, params).fetchall()
    con.close()
    return [_row_to_business(r) for r in rows]


def insert_business(biz):
    """Persist a Business object to SQLite; sets biz.id on success."""
    con = sqlite3.connect(DB_PATH)
    cur = con.execute(
        """INSERT INTO businesses
           (name, category, address, city, phone, email, website, description, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (biz.name, biz.category, biz.address, biz.city,
         biz.phone, biz.email, biz.website, biz.description,
         biz.created_at.isoformat())
    )
    biz.id = cur.lastrowid
    con.commit()
    con.close()
    return biz


def get_business_by_id(business_id):
    """Return a single Business object or None."""
    con = sqlite3.connect(DB_PATH)
    row = con.execute(
        "SELECT * FROM businesses WHERE id = ?", (business_id,)
    ).fetchone()
    con.close()
    return _row_to_business(row) if row else None


def delete_business(business_id):
    """Delete a business by id. Returns True if a row was removed."""
    con = sqlite3.connect(DB_PATH)
    cur = con.execute("DELETE FROM businesses WHERE id = ?", (business_id,))
    con.commit()
    con.close()
    return cur.rowcount > 0


def count_businesses():
    """Return total number of businesses in the database."""
    con = sqlite3.connect(DB_PATH)
    n = con.execute("SELECT COUNT(*) FROM businesses").fetchone()[0]
    con.close()
    return n
