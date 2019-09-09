#Import class from the other file
from bot import telegram_chatbot
from datetime import datetime
from budgettracker import BudgetTracker
from robinhood import Robinhood

update_id = None

#Instantiate objects - telegram_chatbot and BudgetTracker
bot = telegram_chatbot('config.cfg')
tracker = BudgetTracker()
robinhood = Robinhood()

def make_reply(msg):
    try:
        if msg is not None:
            #Splits message into list of items
            output = msg.split(', ')

            #Get the command (1st item in the comma-separated list)
            command = output[0]

            #Get the arguments (if any) (subsequent items in the comma-separated list)
            if len(output) > 1:
                args = output[1:]
            else:
                args = None

            #Returns help text
            if command == 'Help':
                help_text = '''
                This is Isaac's budget bot.
                Commands:
                Add, summary, amount - add expense to database
                Summary, (n_days_before) - gives a summary of expenses in the past n days
                Stock, Positions
                Stock, Symbol, (Symbol)
                '''
                return help_text
            #Add expense to bot
            elif command == 'Add':
                
                time_now = datetime.now()
                reply = tracker.add_expense(args[0], time_now, float(args[1]))

            #Get expense summary
            elif command == 'Summary':
                try:
                    if args:
                        reply = tracker.get_expense_summary(int(args[0]))
                    else:
                        reply = tracker.get_expense_summary()
                except:
                    reply = 'Error'


            #Stocks - Positions (to get my positions), Symbol (to find symbol)
            elif command == 'Stock':
                
                if args[0] == 'Positions':
                    reply = robinhood.get_my_positions()
                elif args[0] == 'Symbol':
                    reply = robinhood.get_symbol(args[1])

            else:
                reply = 'Okay'
            return reply
    except:
        return 'Error'
    
while True:
    print('...')
    updates = bot.get_updates(offset = update_id)
    updates = updates['result']

    if updates:
        #Item is a nested dictionary for each message
        for item in updates:
            update_id = item['update_id']
            try:
                message = str(item['message']['text'])
            except:
                message = None
            from_ = item['message']['from']['id']
            reply = make_reply(message)

            #Send the message
            bot.send_message(reply, from_)