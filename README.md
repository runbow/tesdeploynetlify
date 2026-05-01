# org-analyzer

Proyek sederhana untuk mengolah data ORG dan menghasilkan tabel csv/xls sebagai output


## 📂 Project Structure

* **`app.py`**: The "Front Door." Handles Flask initialization, user authentication, and login sessions.
* **`main_dashboard.py`**: The "Workroom." Contains the dashboard routes and the `Task Handler` that connects the UI to the engine.
* **`engine.py`**: The "Laboratory." Contains pure Pandas logic for data resampling and calculation. No Flask code lives here. <- TBC
* **`init_db.py`**: A setup script to initialize the SQLite database and seed initial user data.
* **`templates/`**: HTML files (`login.html`, `dashboard.html`).

---

## 🚀 Getting Started

### 1. Prerequisites

Python3.x.

### 2. Install Dependencies

Install library yang dibutuhkan:

```bash
pip install flask flask-login pandas

```

### 3. Initialize the Database

Buat database untuk pertama kalinya:

```bash
python init_db.py

```

### 4. Run the Application

Jalankan Flask:

```bash
python app.py

```

Buka dengan mengunjungi `http://127.0.0.1:5000/login` dari browser.

---

## 🔐 Credentials (Development/Test)

| Username | Password | 
| --- | --- | 
| **admin** | `admin123` | 
| **researcher_john** | `hydro2024` | 

---
## Diagram
### Sequence Diagram User
```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant D as main_dashboard.py
    participant E as engine.py
    participant DB as SQLite Database

    U->>D: Click "Kumulatif Jam/Hari/Pola Diurnal"
    Note right of U: Sends JSON: {files: [...], method: process_data'}
    
    D->>D: Check @login_required
    
    alt Authorized
        D->>E: Call process_data(paths)
        Note right of E: Pandas: pd.read_csv() & resample()
        E-->>D: Return Result DataFrame
        D->>D: Convert DF to CSV String (io.StringIO)
        D-->>U: Return JSON {success: True, csv_content: "..."}
        U->>U: Trigger Browser Download (.csv)
    else Unauthorized
        D-->>U: Redirect to /login
    end
```

###Sequence Diagram Admin
```mermaid
sequenceDiagram
    participant A as Admin (Browser)
    participant AD as admin_dashboard.py
    participant DB as SQLite Database


    AD->>AD: Check @login_required
    alt Authorized
        A->>AD: Create new user
        A->>AD: Select desired temporal value

        Note right of A: Parse temporal value as path
        AD->>DB: Insert user acc and path
    
        
    else Unauthorized
        AD-->>A: Redirect to /login
    end
```

### Eentity Relationship Diagram
```mermaid
erDiagram
    USERS ||--o{ ALLOWED_DATA : "has"
    USERS }|--|| ROLES : "assign"
    USERS {
        int id PK
        string username
        string password_hash
        int role_id
    }
    ALLOWED_DATA {
        int id PK
        int user_id FK
        datetime start_date
		datetime end_date
    }
    ROLES {
        int id PK
        string role_name
    }
```
