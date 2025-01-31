class CommandHandler:
    COMMANDS = {
        'help': 'Show available commands',
        'balance': 'Check account balance',
        'history': 'View transaction history',
        'exit': 'Exit the program'
    }

    @staticmethod
    def is_command(text):
        return text.startswith('/')

    @staticmethod
    def handle_command(text, db_manager):
        cmd = text[1:].lower()
        
        if cmd == 'help':
            return "\n".join([f"/{cmd}: {desc}" for cmd, desc in CommandHandler.COMMANDS.items()])
        
        elif cmd == 'balance':
            balance = db_manager.get_balance(1)  # Using demo user_id
            return f"Your current balance is ${balance:.2f}"
        
        elif cmd == 'history':
            transactions = db_manager.get_transactions(1)  # Using demo user_id
            if not transactions:
                return "No recent transactions found."
            
            response = "Recent transactions:\n"
            for trans in transactions:
                response += f"- {trans[0]}: ${trans[1]:.2f} on {trans[2]}\n"
            return response
        
        elif cmd == 'exit':
            raise KeyboardInterrupt
        
        return f"Unknown command. Type /help for available commands."
