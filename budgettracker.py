import pandas as pd 
import numpy as np 
from datetime import datetime, timedelta

import os
import time


#Helper function to convert from loc result -> datetime64 -> datetime object
def get_datetime(loc_result):
    npdate = loc_result.values[0]
    npint = int(npdate) / 1e9
    date = datetime.utcfromtimestamp(npint)
    date = date.strftime('%m/%d')
    return date

class BudgetTracker():

    #Constructor method
    def __init__(self):
        
        try:
            self.df = pd.read_csv('expenses.csv', parse_dates = ['Date'])
            print(self.df)
        except:
            self.df = pd.DataFrame(columns = ['Date', 'Summary', 'Amount'])

    #Saves the dataframe into CSV file
    def save_csv(self):
        self.df.to_csv('expenses.csv', index = False)


    #Add expense to dataframe
    def add_expense(self, summary, date, amount):
        #Add row to dataframe
        self.df = self.df.append({'Date': date, 'Summary': summary, 'Amount': amount}, ignore_index= True)

        print(date)
        print(date.strftime('%m/%d %H:%M'))

        reply = '''Successfully added expense:
                Date: {}
                Summary: {}
                Amount: ${}

                '''.format(date.strftime('%m/%d %H:%M'), summary, amount)

        self.save_csv()
        print(self.df)

        return reply

    #Get summary of expenses in past x days
    def get_expense_summary(self, n_days_before = 7):

        #Get timeMax: time now
        date_now = datetime.now()

        #Get timeMin: time n_days_before before now
        date_min = date_now - timedelta(days = n_days_before)

        #Filtering df for expenses in timeframe
        is_filtered_dates = (self.df['Date'] > date_min) & (self.df['Date'] < date_now)
        df_filtered = self.df.loc[is_filtered_dates, :]

        #Print total expense

        max = df_filtered['Amount'].max()
        max_summary = df_filtered.loc[df_filtered['Amount'] == max, 'Summary'].values[0]
        max_date = get_datetime(df_filtered.loc[df_filtered['Amount'] == max, 'Date'])

        out = '''Expense Summary from {} to {}:
        Total: ${}
        Average per day: ${}
        Highest Expense: ${}, {}, {}
        Latest Expense: ${}, {}, {}
        '''.format(date_min.strftime('%m/%d'), date_now.strftime('%m/%d'), round(df_filtered['Amount'].sum(), 2), round(df_filtered['Amount'].sum() / n_days_before, 2),
        max, max_summary, max_date,
        df_filtered['Amount'].iat[-1], df_filtered['Summary'].iat[-1], df_filtered['Date'].iat[-1].strftime('%m/%d'))

        return out



    


