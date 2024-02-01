# Whole-Foods-Grocery-Delivery-Script
Proof of concept for my Senior Capstone Project in CS. **Requires Subscription to Amazon Prime to be functional**

## Overview

This Python script is designed to automate the process of ordering groceries from Amazon Fresh. It utilizes the Selenium library to interact with the Amazon Fresh website, searching for specific ingredients and adding them to the cart.

## Prerequisites

Before running the script, make sure you have the following installed:

- [Python](https://www.python.org/)
- [Selenium](https://www.selenium.dev/documentation/en/)
- [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

## Getting Started

1. Clone this repository to your local machine:
   ```bash git clone https://github.com/your-username/amazon-fresh-bot.git```
2. Navigate to the project directory:
   ```bash cd amazon-fresh-bot```
3. Install the required Python packages:
   ```bash pip install selenium```
4. Download and place the Microsoft Edge WebDriver executable in the project directory. You can download it from [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH).
5. Edit the INGREDIENTS_FILE variable in the script (amazon_fresh_bot.py) to point to your ingredient list file (default is "ingredients.txt").
6. Run the script:
   ```bash python amazon_fresh_bot.py```

## Usage

1. The script will prompt you to enter "cont" to continue at various points. This is to ensure that you review and confirm each step.

2. The script reads the list of ingredients from the specified file, filters out common ingredients you already have, and then proceeds to order the remaining items from Amazon Fresh.

3. The ordering process involves searching for each ingredient, selecting a non-sponsored product, adding it to the cart, and completing the checkout process. You can customize the exclusion list of common ingredients in the script.

4. By default, the script is set to perform a trial run without actually submitting the order. Uncomment the relevant code at the end of the order function if you want to enable the actual order submission.

## First-Time Setup

- Set the boolean value in the main function to False.
- Run the script, manually navigate to Amazon, sign in, and wait for cookies to save. The script will then save the cookies to the file cookies.json.

## Disclaimer

This script is provided for educational purposes only. Use it responsibly and at your own risk. The authors are not responsible for any consequences of misuse.

Note: Ensure that you comply with the terms of service of the websites you are interacting with and that your actions do not violate any applicable laws or policies.
