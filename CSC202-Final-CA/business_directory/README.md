# local-business-directory

A Flask web application where users can view, search, and add local businesses.
Built as a portfolio project combining **OOP**, **Data Structures**, and **Flask** web development.

---

## What the App Does

- Browse all listed businesses on the home page
- Search businesses by name, city, or description
- Filter by category (Restaurant, Retail, Technology, etc.)
- Add a new business using a simple web form
- See the **5 most recently added** businesses highlighted at the top (Stack / LIFO)
- Remove a business from the directory

---

## How to Run the App on Your Computer

Follow these steps exactly. You do not need any prior experience.

### Step 1 — Make sure Python is installed

Open your **Terminal** (Mac/Linux) or **Command Prompt** (Windows) and type:

```
python --version
```

You should see something like `Python 3.10.x`. If you get an error, download Python from https://www.python.org/downloads/ and install it first.

---

### Step 2 — Download or copy the project files

Make sure you have the project folder (`business_directory/`) saved somewhere on your computer, for example on your Desktop.

---

### Step 3 — Open the project folder in your terminal

On **Mac/Linux**:
```
cd ~/Desktop/business_directory
```

On **Windows**:
```
cd C:\Users\YourName\Desktop\business_directory
```

---

### Step 4 — Create a virtual environment

A virtual environment keeps this project's packages separate from the rest of your computer.

```
python -m venv venv
```

Now activate it:

- **Mac / Linux:**
  ```
  source venv/bin/activate
  ```
- **Windows:**
  ```
  venv\Scripts\activate
  ```

You will see `(venv)` appear at the start of your terminal line. That means it worked.

---

### Step 5 — Install Flask

```
pip install -r requirements.txt
```

This installs Flask, which is the only dependency.

---

### Step 6 — Run the app

```
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
```

---

### Step 7 — Open the app in your browser

Open any web browser (Chrome, Firefox, Edge) and go to:

```
http://127.0.0.1:5000
```

The app is now running on your computer. No internet connection is needed.

To stop the app, go back to the terminal and press **Ctrl + C**.

---

## Project Structure

```
business_directory/
├── app.py          # Flask routes (the web server logic)
├── models.py       # Python OOP classes + SQLite database helpers
├── requirements.txt
├── .gitignore
├── README.md
└── templates/
    ├── base.html   # Shared page layout (navbar, footer)
    ├── index.html  # Home page — browse & search businesses
    ├── add.html    # Form to add a new business
    └── about.html  # About page
```

---

## OOP & Data Structures Used

### `Business` class (`models.py`)
A pure Python class (no third-party ORM) that models a real-world business:

```python
biz = Business("Kano Suya Spot", "Restaurant", "Ahmadu Bello Way", "Kano", ...)
print(biz.get_summary())      # one-line summary string
print(biz.formatted_date())   # human-readable timestamp
print(biz.to_dict())          # plain dictionary of all fields
```

- `__init__` sets all attributes including `self.created_at = datetime.now()`
- Uses Python's built-in `datetime` module for timestamping

### `RecentlyAddedStack` class (`models.py`)
A **Stack (LIFO)** built on a plain Python list:

```python
stack = RecentlyAddedStack()
stack.push(biz)       # uses list.append()
stack.undo_last()     # uses list.pop()
stack.peek()          # returns newest-first view
```

Stores the last 5 businesses added. Displayed on the home page.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | Flask 3.x |
| Database | SQLite (stdlib `sqlite3`, no ORM) |
| Frontend | Bootstrap 5 (CDN) |
| Language | Python 3 |
