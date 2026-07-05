# 📚 Terminal-Based Library Management System

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Cryptography](https://img.shields.io/badge/Security-Fernet_Cryptography-black?style=for-the-badge&logo=letsencrypt)
![CLI](https://img.shields.io/badge/Interface-Command_Line-4D4D4D?style=for-the-badge&logo=gnometerminal)

> A robust, secure, and interactive Command Line Interface (CLI) application for managing library inventories, borrowing transactions, and visitor logs.

---

## 📖 About The Project

![App Screenshot](https://via.placeholder.com/800x400?text=Insert+Terminal+Screenshot+Here)
*Caption: A snapshot of the main terminal interface.*

This project is a comprehensive Python-based Terminal Library System designed to handle standard library operations securely. It was built to manage book inventories, track borrower deadlines (enforcing a strict 7-day borrowing policy), and log all visitor transactions. 

One of the core highlights of this system is its **data persistence and security**. All text-based databases (`library.txt`, `borrow_list.txt`, `logbook.txt`) are dynamically generated and encrypted at rest using symmetric encryption. This ensures that sensitive library data cannot be manually tampered with or read outside of the application interface.

### ✨ Key Features

* **🔐 File Encryption:** Utilizes the `cryptography.fernet` library to encrypt local files upon exit and decrypts them instantly upon application launch.
* **📦 Inventory Management:** Add, edit, delete, view, and search books dynamically. Contains logic to prevent the duplication of identical titles and authors.
* **🧠 Smart Borrowing Logic:** Validates leap years, dynamically calculates days in specific months, and enforces a strict 7-day return policy without relying on external date libraries.
* **📝 Digital Logbook:** Logs all user visits, borrowing, and returning actions with strict time and date validation.
* **🛡️ Error Handling:** Built-in safeguards against corrupt files, missing data, and invalid user string/integer inputs to prevent terminal crashes.

---

## 🚀 Getting Started

Follow these steps to set up the project locally on your machine.

### Prerequisites
* **Python 3.x** installed on your machine.
* **pip** (Python package installer).

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vinvin-prog/library-system-python.git
   ```

2. **Navigate to the project directory**
   ```bash
   cd library-system-python
   ```

3. **Install the required dependency**
   ```bash
   pip install cryptography
   ```

4. **Run the application**
   ```bash
   python DeCastro_main.py
   ```

> **Note:** On the first run, the system automatically generates the required database files (`library.txt`, `borrow_list.txt`, `logbook.txt`) as well as the `key.key` encryption file.

---

## 💻 Usage

When you launch the system, you will be greeted by the **Main Interface**.

- **[1] Go to Library** – Access the core CRUD operations for the book inventory.
- **[2] Borrow Books** – Authenticate with your name to borrow an available book. The system automatically calculates your exact return deadline.
- **[3] Logbook** – View daily transactions or log a non-borrowing visit.

> **⚠️ Security Note:** Do **not** delete or modify the `key.key` file generated in the project directory. Doing so will permanently lock the data stored in the encrypted `.txt` database files.

---

## 💡 Key Learnings

- **State & File Management:** Safely handled file I/O operations using `try`/`except` blocks and `with open()` context managers to prevent data corruption.
- **Data Security:** Implemented the `cryptography` library (Fernet) to encrypt local database files and learned the importance of secure encryption key management.
- **Data Structures:** Used Python dictionaries and lists extensively to manage relationships between books, borrowers, and transaction records in a local file-based system.

---

## 📬 Contact

**Amiel**

- GitHub: https://github.com/vinvin-prog
- Email: avdc02@example.com

**Project Repository:** https://github.com/vinvin-prog/library-system-python