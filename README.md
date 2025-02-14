# Voice-Activated Banking Assistant

## Overview

This project is a voice-activated banking assistant that allows users to interact with a SQLite database using voice commands. The assistant can perform various banking operations such as checking balance, making deposits and withdrawals, creating new users, and transferring money between accounts.

## Demo Video

### Introduction
[Watch Here](https://www.loom.com/share/715529a97db746ff8de528e526e58014?sid=921f27d3-9b67-4106-b8db-259bbec989a5)

### Functionality
[Watch Here](https://www.loom.com/share/3452a391de424b3ea84a21a131b17840)

<video controls>
  <source src="demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Features

- **Voice Commands**: Interact with the bot using natural language.
- **Banking Operations**: Check balance, view recent transactions, make deposits and withdrawals, create new users, and transfer money.
- **User Management**: Create and switch between different user accounts.
- **Logging**: All interactions and transactions are logged for auditing purposes.
- **Database**: Uses SQLite for storing user data and transaction history.

## Setup Instructions

### Prerequisites

- Python 3.x
- `virtualenv` package (install using `pip install virtualenv`)

### Setting Up the Virtual Environment

#### On macOS and Linux

1. Open a terminal.
2. Navigate to the project directory.
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

#### On Windows

1. Open Command Prompt.
2. Navigate to the project directory.
3. Create a virtual environment:
   ```cmd
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```cmd
   venv\Scripts\activate
   ```

### Installing Dependencies

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the voice bot, run the following command in your terminal:

```bash
python main.py
```

## Functionalities

After running the application, you can interact with the voice bot using the following commands:

- **Check Balance**: Ask "What's my balance?" to get your current account balance.
- **Recent Transactions**: Say "Show my transactions" to view your recent transactions.
- **Make Deposit**: Use "Deposit $100" to add money to your account.
- **Make Withdrawal**: Use "Withdraw $50" to take money out of your account.
- **Create User**: Say "Create user John" to create a new user account.
- **Transfer Money**: Use "Transfer $100 to John" or "Send $100 to John" to transfer money to another user.
- **Help**: Say "Show help" to get a list of available commands.

These commands directly interact with the SQLite database, allowing you to manage your account and transactions through voice assistance.

## Logging and Database

- All interactions and transactions are logged in `app.log`.
- The SQLite database is set up automatically and includes tables for users, transactions, and conversation history.

## Exiting the Application

To exit the voice bot, press `Ctrl+C` in the terminal.

## Cleanup

The application will automatically clean up temporary audio files and close the database connection upon exit.

## Troubleshooting

- Ensure your microphone is working properly for voice commands.
- Check `app.log` for any errors or issues during execution.
- Ensure all dependencies are installed correctly.

## Acknowledgments

- OpenAI for providing the language model used in this project.
- SQLite for the database management system.

