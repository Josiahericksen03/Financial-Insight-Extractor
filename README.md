# Financial Insight Extractor

# Project Setup Instructions

## Initial Setup

1. **Install MongoDB:**
   Open your terminal and run these commands to install MongoDB on macOS:
   ```bash
   brew tap mongodb/brew
   brew install mongodb-community
   brew services start mongodb/brew/mongodb-community
   ```

## Configuration Steps

2. **Setup Python Environment:**
   In the project root directory create a venv and install the necessary Python packages:

   - Install Flask:
     ```bash
     pip install flask
     ```
   
   - Install PyMongo:
     ```bash
     pip3 install pymongo
     ```

   - Install yFinance:
     ```bash
     pip3 install yfinance
     ```
   - Install matplotlib:
     ```bash
     pip3 install matplotlib
     ```
   - Install PyMuPDF:
     ```bash
     pip install pymupdf
     ```

     ```
     flask run
     ```

## Optional Tools

3. **Install and Use MongoDB Shell (mongosh):**
   - To install `mongosh`, run:
     ```bash
     brew install mongosh
     ```
   - To start `mongosh`, simply type:
     ```bash
     mongosh
     ```
   - Once `mongosh` is running, connect to our database:
     ```bash
     use("userDatabase")
     ```
   - Example usage to view registered users:
     ```bash
     db.users.find({}, { password: 0, _id: 0 })
     ```

## Note

- A `.gitignore` file has been created to ensure that `venv` and other  files are not tracked by our git pushes.

change

## Purpose
The purpose of this project is to make 10q reports easier to understand for a normal person, as well as being able to compare and analyze different data from these reports purely by uploading a pdf. This program also supports account creation to save and view history of 10qs analyzed.

## List of Libraries

- flask, yfinance, matplotlib, concurrent.futures, io, base64, fitz(pymupdf), re
- Database, passwordhashing

Here is the text with improved spacing and minor corrections for clarity and readability:

Here is the complete text with the additional section included and formatted for clarity:

## Separation of Work

- **Account MongoDB Database Setup: Eli Bendavid**
  - Develop a secure MongoDB database to store user account information.
  - Allow for Role-Based Access.
  - Focuses on data encryption and secure login.
  - Password hashing.
  - Note: I have changed this requirement to comply with the Role-Based Access requirement (previously used SQLite).

- **PDF Mounting for Scanner: Eli Bendavid**
  - Create a page that allows registered users to add PDF reports for scanning.
  - Allow users to preview these files before uploading.
  - Allow these files to be saved in the profile section.

- **Earning Report Scanner: Edgar Guerrero and Gabriel Romanini**
  - Develop the scanner functionality of the program. The scanner should accept 10Q reports in PDF format.
  - Focus on extracting key financial information in a consistent format.
  - Note: Changed requirements to use publicly available 10Q reports instead of a standardized template. This shouldn’t violate any Terms of Service.

- **Live Market Data Section: Edgar Guerrero and Gabriel Romanini**
- **General Stock Information Section: Edgar Guerrero and Gabriel Romanini**
- **Comparison Page and Functionality: Trent Fetzer**
  - Uses the yfinance import to get the average variables of different sectors.
  - This will eventually be used as a tool to allow users to compare scanned 10Qs to industry averages.
  - (NEW)

- **Profile Page and Scan History: Josiah Ericksen**
  - Create a profile page where registered users can view and change their information.
  - Create a scan history page where users can view documents that they have scanned in the past.

- **Simple Graphs/Analysis:**
  - Once a document has been scanned, we will produce relevant charts/graphs of their respective variables.
  - Year-over-Year Growth (Trent, Gabe): Bar graph comparing current earnings to the same quarter in previous years.
  - Segment Performance (Josiah, Eli): Bar or pie charts showing revenue or profit by business segment.
  - Revenue and Net Income Trends (Eli and Edgar): Line graphs showing quarterly or annual trends over several years.

- **Flask HTML Webpages (so far):**
  - Eli Bendavid: index.html, register.html, login.html, instructions.html
  - Trent Fetzer: compare.html
  - Josiah Ericksen: change_password.html, profile.html