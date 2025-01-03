# README.md

# My Python Project

This project is a Python application that interacts with the Facebook API to post messages to a Facebook page. It utilizes environment variables for configuration and includes automation for testing and deployment using GitHub Actions.

## Overview

The application allows users to post messages and links to a specified Facebook page using the Facebook Graph API. It is designed to be simple and easy to use, making it suitable for developers looking to integrate Facebook posting functionality into their applications.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/my-python-project.git
   cd my-python-project
   ```

2. Create a `.env` file in the root directory and add your Facebook API credentials:
   ```
   FACEBOOK_PAGE_ACCESS_TOKEN=your_access_token
   FACEBOOK_PAGE_ID=your_page_id
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To post a message to your Facebook page, modify the `src/script.py` file with your desired message and link, then run the script:
```
python src/script.py
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.