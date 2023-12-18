# Crunchbase Scraper

## Overview
The Crunchbase Scraper is a tool designed to extract funding round information from Crunchbase, a leading platform for finding business information about private and public companies. This script is particularly useful for researchers, investors, and analysts who need up-to-date data on company funding rounds.

## Prerequisites
Before using the Crunchbase Scraper, ensure you have the following prerequisites:

1. **Crunchbase Premium Account**: Access to the data requires a Crunchbase premium account. You can sign up for a free 7-day trial of Crunchbase Premium to test the functionality of this scraper.
2. **Python Environment**: The script is written in Python and requires Python 3 to run.
3. **Required Python Packages**: The script depends on several Python packages which can be installed using the provided requirements file.

## Setup and Installation
Follow these steps to set up the Crunchbase Scraper:

1. **Clone the Repository**: Start by cloning this repository to your local machine.
   
   ```bash
   git clone https://github.com/FredericoBaker/crunchbase-scraper
   ```

2. **Install Dependencies**: Navigate to the cloned repository's directory and install the required Python packages.

   ```bash
   pip install -r requirements.txt
   ```

3. **Crunchbase Account Login**: Before running the script, log in to your Crunchbase premium account in chrome web browser. This step is crucial as the scraper relies on your account's access permissions to retrieve data.

## Usage
To run the Crunchbase Scraper, execute the following command in the terminal:

```bash
python3 main.py
```

This command initiates the scraping process, which will gather data on funding rounds from Crunchbase based on your account's access privileges.
