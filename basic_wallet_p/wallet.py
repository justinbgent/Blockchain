import requests
import json
import sys

id = input("To get information about a particular user, enter their id: ")

if len(sys.argv) > 1:
    node = sys.argv[1]
else:
    node = "http://localhost:5000"

def check_for_json(stuff):
    # Handle non-json response
    try:
        data = stuff.json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(stuff)
        return
    return data


#r = requests.get(url=node + "/chain")
#data = check_for_json(r)
def get_transactions():
    r = requests.get(url=node + "/transactions")
    data = check_for_json(r)
    if data:
        return data['transactions']

def get_my_transactions(id):
    transactions = get_transactions()
    if transactions:
        my_transactions = []
        for action in transactions:
            if action['recipient'] == id:
                my_transactions.append(action)
            elif action['sender'] == id:
                my_transactions.append(action)
        
        return my_transactions
    else:
        print('\nError')
        
def get_my_balance(id):
    my_transactions = get_my_transactions(id)

    amount = 0
    for action in my_transactions:
        if action['recipient'] == id:
            amount += action['amount']
        elif action['sender'] == id:
            amount -= action['amount']

    print(f'\n{id}: {amount}')
    return my_transactions


while True:
    text = input("\n'b' balance, 't' transactions, 'bt' for both, 'i user_id' to change id, or 'q' quit: ")
    if text == 'b':
        get_my_balance(id)
    elif text == 't':
        for action in get_my_transactions(id):
            print(action)
    elif text == 'bt':
        for action in get_my_balance(id):
            print(action)
    elif text[:2] == 'i ':
        id = text[2:]
    elif text == 'q':
        break
    else:
        print("Error: Bad Input")