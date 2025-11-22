# 🤖 Job Scraper & Email Notifier

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
</p>

An intelligent job scraper that automatically finds entry-level positions (0-2 years experience) from **Naukri.com** and **Indeed.com**, and sends you a beautifully formatted HTML email digest with the results.

---

## ✨ Features

- 🎯 **Experience-Based Filtering**: Automatically filters jobs for 0-2 years of experience
- 🔍 **Dual-Platform Scraping**: Fetches jobs from both Naukri and Indeed
- 🚀 **Smart Defaults**: Works even without URLs using default entry-level searches
- 📄 **Intelligent Pagination**: Scans up to 15 pages per site, collecting up to 50 relevant jobs
- 💌 **Beautiful HTML Emails**: Clean, modern, mobile-friendly email reports
- 🔒 **Secure Credentials**: Uses `.env` file for safe credential management
- 🛡️ **Robust Scraping**: Multiple CSS selectors for reliable data extraction
- 🔄 **Duplicate Detection**: Prevents duplicate job listings in results

---

## 📸 Screenshots

### Email Digest Example
*Beautiful HTML email with job listings, company info, and direct application links*

### Terminal Output
*Real-time progress updates as the scraper finds jobs*

---

## 🔧 Prerequisites

- **Python 3.8+**
- **Google Chrome** browser
- **Gmail account** with App Password enabled

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Job_Scraper.git
cd Job_Scraper
```

### 2. Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example email_password.env
   ```

2. Edit `email_password.env` with your credentials:
   ```ini
   SENDER_EMAIL="your_email@gmail.com"
   SENDER_PASSWORD="your_16_digit_app_password"
   ```

> **🔐 Getting Your Google App Password:**
> 1. Go to [Google Account Settings](https://myaccount.google.com/)
> 2. Navigate to **Security** → **2-Step Verification** (enable if needed)
> 3. Scroll to **App Passwords**
> 4. Select **Mail** and **Other (Custom name)**
> 5. Enter "Job Scraper" and generate
> 6. Copy the 16-digit password to your `.env` file

---

## ▶️ Usage

### Basic Usage
```bash
python main.py
```

The script will prompt you for:
- **Receiver's email address**
- **Naukri URL** (optional - press Enter for default)
- **Indeed URL** (optional - press Enter for default)

### Example Run
```
--- Job Scraper & Notifier (0-2 Years Experience) ---
✉️  Enter the receiver's email address: yourname@example.com
🔗 Enter Naukri URL (or press Enter to use default): 
🔗 Enter Indeed URL (or press Enter to use default): 
------------------------------
🔍 Searching for jobs with 0-2 years experience requirement...
🚀 Starting Naukri scraper...
Scraping page 1: https://www.naukri.com/jobs-0-to-2-years-experience
✅ Found 25 jobs on Naukri.
🚀 Starting Indeed scraper...
✅ Found 30 jobs on Indeed.

🎯 Found a total of 55 jobs matching 0-2 years experience criteria.
📧 Preparing email...
📬 Sending email to yourname@example.com...
✅ Email sent successfully!
🎉 Process finished.
```

---

## 📁 Project Structure

```
Job_Scraper/
├── main.py                    # Main script
├── scrapers/
│   ├── __init__.py
│   ├── naukri_scraper.py     # Naukri.com scraper
│   └── indeed_scraper.py     # Indeed.com scraper
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── email_password.env        # Your credentials (gitignored)
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🛠️ Troubleshooting

### Issue: "No jobs found"
- **Solution**: Check your internet connection and verify the job sites are accessible
- Try running without headless mode (comment out `options.add_argument("--headless")`)

### Issue: "Failed to send email"
- **Solution**: Verify your App Password is correct (16 digits, no spaces)
- Ensure 2-Step Verification is enabled on your Google account
- Check if Gmail is blocking the login attempt

### Issue: "ChromeDriver issues"
- **Solution**: The script auto-downloads ChromeDriver via `webdriver-manager`
- Ensure Chrome browser is installed and up-to-date

### Issue: "Website structure changed"
- **Solution**: CSS selectors may need updating in scraper files
- Open an issue on GitHub with details

---

## 🔮 Future Roadmap

- [ ] **Configuration File**: YAML/JSON config for search parameters
- [ ] **Job Deduplication**: SQLite database to track seen jobs
- [ ] **Scheduled Execution**: Cron job support for daily automation
- [ ] **CSV Export**: Save job history to spreadsheet
- [ ] **Smart Notifications**: Email only NEW jobs
- [ ] **Telegram/Slack Integration**: Alternative notification channels
- [ ] **Advanced Filters**: Salary range, remote jobs, keywords
- [ ] **Multi-site Support**: LinkedIn, Glassdoor, etc.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Web scraping may violate the Terms of Service of some websites. Use this script responsibly and ethically. Website structures change frequently, which may require updating the CSS selectors.

---

## 🙏 Acknowledgments

- Built with [Selenium](https://www.selenium.dev/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- Email functionality powered by Python's `smtplib`

---

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

**Happy Job Hunting! 🎯**