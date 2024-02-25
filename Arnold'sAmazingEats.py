# Name:                     ArnoldsAmazingEatsIIPOS.py
# Author:                   Andre Lima
# Date Created:             Febuary 2, 2023
# Date Last Modified:       April 1, 2023
#
# Purpose:
# To take customers orders, tally's their total, and prints a receipt 

# Function: styleMoney
# Description: creates string with money value as $0.00
# Parameters:
#       value: amount of money
#       subtract: if add '-' or not
# Return Value:
#       dollar: formated value
def styleMoney(value, subtract = False):
    if subtract:
        dollar = "-${0:.2f}".format(value)
    else:
        dollar = "${0:.2f}".format(value)

    return dollar

# Function: stylePhoneNumber
# Description: creates string with phone number as 123-456-7890
# Parameters:
#       phoneNumber: phone number
# Return Value:
#       newPhoneNumber: fromated phone number
def stylePhoneNumber(phoneNumber):
    stylePhoneNumber = "("

    for c in phoneNumber:
        stylePhoneNumber += c

        if len(stylePhoneNumber) == 4:
            stylePhoneNumber += ")"
        
        if len(stylePhoneNumber) == 8:
            stylePhoneNumber += "-"
    
    return stylePhoneNumber

# Function: styleMenu
# Description: creates string with menu items and prices in columns
# Parameters:
#       menu: menu item names and prices
# Return Value:
#       menuStyle: formated menu
def styleMenu(menu):
        menuStyle = "\n{0:-^28}".format("Menu")

        for mealNum in menu:
                menuStyle += "\n{0:>3d}. {1:<13} {2:>6}".format(mealNum, (menu[mealNum]['meal']).capitalize(), styleMoney(menu[mealNum]['price']))
        
        menuStyle += "\n{0:-^28}\n".format('-')

        return menuStyle

# Function: styleCustomer
# Description: creates a string with the customer's information
# Parameters:
#       customerInfo: Customer's information
# Return value:
#       styleInfo: customer's information formatted
def styleCustomerInfo(customerInfo):
    styleInfo = ""

    for info in customerInfo:
        if info != 'specialInstructions':
            styleInfo += "\n{}".format(customerInfo[info])
        else:
            styleInfo += "\n***{}***".format(customerInfo[info])

    return styleInfo

# Function: styleReceipt
# Description: creates string with receipt for order made
# Parameters:
#       menu: meal names and prices
#       order: contains customer's order
#       student: if cutomer is student
#       delivery: if the order is for delivery
#       customerInfo: customer's information
# Return Value:
#       receiptStyle: formated receipt
def styleReceipt(menu, order, student, delivery, customerInfo):
    #add customer's information to receipt
    receiptStyle = "\nOrder for:{}\n".format(styleCustomerInfo(customerInfo))

    #specify if order is for delivery or pickup
    if delivery:
        receiptStyle += "\nFor Delivery"
    else:
        receiptStyle += "\nFor Pickup"

    receiptStyle += "\n{0:>24}{0:>9}".format("Item") +\
        "\n{0:<20}{1:>4}{2:>9}{3:>11}".format("Order", "Amt", "Price", "Total") +\
        "\n{0:-<14}{0:<6}{0:-<4}{0:<3}{0:-<6}{0:<3}{0:-<8}".format("")

    #add meals ordered and their totals to the receipt
    for i in range(len(order['mealSelection'])):
        receiptStyle += "\n{0:<20}{1:>4}{2:>9}{3:>11}".format(menu[order['mealSelection'][i]]['meal'].capitalize(),
                                                                order['quantity'][i],
                                                                styleMoney(menu[order['mealSelection'][i]]['price']),
                                                                styleMoney(menu[order['mealSelection'][i]]['price'] * order['quantity'][i]))
    
    #create subTotal and add to receipt
    order.update({'subTotal' : getSubTotal(menu, order)})

    receiptStyle += "\n{0:<31}{1:>13}".format("Sub Total", styleMoney(order['subTotal']))

    #apply discount to receipt
    order.update({'discount' : getDiscount(order['subTotal'])})
    order.update({'total' : order['subTotal'] - order['discount'][1]})

    receiptStyle += "\n%{0:2} {1:<27}{2:>13}".format(order['discount'][0], "Discount", styleMoney(order['discount'][1], True))

    #apply student discount to receipt if applicable
    if student:
        order.update({'studentDiscount' : [10, order['subTotal'] * 0.1]})
        order['total'] -= order['studentDiscount'][1]

        receiptStyle += "\n%{0:2} {1:<27}{2:>13}".format(order['studentDiscount'][0], "Student Discount", styleMoney(order['studentDiscount'][1], True))

    #add delivery charges and driver tip if order is for delivery
    if delivery:
        if order['subTotal'] >= 30:
            order.update({'deliveryFee' : 0})
        else:
            order.update({'deliveryFee' : 5})

        order['total'] += order['deliveryFee']
        order.update({'tip' : getTip()})

        if order['tip']:
            receiptStyle += "\n%{0:>2} {1:<27}{2:>13}".format(order['tip'][0], "Tip", styleMoney(order['subTotal'] * order['tip'][1]))

            order['total'] += order['subTotal'] * order['tip'][1]
        
        receiptStyle += "\n{0:<31}{1:>13}".format("Delivery Fee", styleMoney(order['deliveryFee']))

    #add hst and total to receipt
    order.update({'hst' : order['subTotal'] * 0.13})
    order['total'] += order['hst']

    receiptStyle += "\n{0:<31}{1:>13}".format("HST", styleMoney(order['hst'])) +\
        "\n{0:>36}{0:->8}".format("") +\
        "\n{0:>33}{1:>11}".format("TOTAL", styleMoney(order['total']))

    return receiptStyle

# Function: getSubTotal
# Description: calculates the sub total of the customers order
# Parameters:
#       menu: contains menu pricing and order quantity
# Return Value:
#       subTotal: sub total
def getSubTotal(menu, order):
    subTotal = 0

    for i in range(len(order['mealSelection'])):
        subTotal += menu[order['mealSelection'][i]]['price'] * order['quantity'][i]

    return subTotal

#Function: getTip
# Description: asks customer how much they want to tip the delivery driv
# Return value:
#       tip: either False if no tip is given or list containg tip % and tip .
def getTip():
    tip = confirmationDialog("Would you like to leave the driver a tip?")

    if tip:
        tip = inputCheck("How much would you like to tip in %? [10, 15, 20]: ", tip = True)

        if tip == 10:
            return [10, 0.1]
        elif tip == 15:
            return [15, 0.15]
        elif tip == 20:
            return [20, 0.2]

    return tip

# Function: getDiscount
# Description: determines the discount to be applied at checkout
# Parameters:
#       subTotal: sub total of customers order
# Return Value:
#       int: % discount applied
#       discount: amount being discounted
def getDiscount(subTotal):
    if subTotal > 500:
        discount = subTotal * .25

        return(25, discount)
    elif subTotal > 100:
        discount = subTotal * .2

        return(20, discount)
    else:
        discount = subTotal * .15

        return(15, discount)

# Function: confimationDialog
# Description: presents the user with a y/n dialog
# Parameters:
#       inputString: yes or no question
#       yesString: prints if user enters 'y'
#       noString: prints if user enters 'n'
# Return Value: 
#       boolean
def confirmationDialog(inputString, yesString = "", noString = ""):
    #prompt the user for 'y' or 'n'
    confirmation = input("\n{} [Y/N]: ".format(inputString)).upper()

    #loops until user gives a valid input and prints applicable string
    while True:
        if confirmation == "Y":
            if yesString:
                print("\n" + yesString)

            return True
        elif confirmation == "N":
            if yesString:
                print("\n" + noString)

            return False
        else:
            confirmation = input("Please enter a valid input: ").upper()

# Function: inputCheck
# Description: checks user's input
# Parameters:
#       prompt: prompt for user input
# Return Value:
#   userInput: the user's input so long as checks
def inputCheck(prompt, psCode = False, phNum = False, num = False, tip = False, order = 0):
    userInput = input(prompt)

    if psCode:
        while True:
            if len(userInput) == 6:
                return userInput
            else:
                userInput = input("Please enter a valid input: ")
    elif phNum:
        while True:
            if userInput.isnumeric() and len(userInput) == 10:
                return userInput
            else:
                userInput = input("Please enter a vaid input: ")
    elif num:
        while True:
            if userInput.isnumeric():
                return int(userInput)
            else:
                userInput = input("Please enter a vaid input: ")
    elif tip:
        while True:
            if userInput == '10' or userInput == '15' or userInput == '20':
                return int(userInput)
            else:
                userInput = input("Please enter a valid input: ")
    elif order:
        while True:
            if userInput.isnumeric() and int(userInput) > 0 and int(userInput) <= order:
                return int(userInput)
            else:
                userInput = input("Please enter a vaid input: ")
    else:
        while True:
            if len(userInput) > 0:
                return userInput
            else:
                userInput = input("Pleae enter a valid input: ")

# Function: infoCustomer
# Description: gets the customer's information
# Parameters:
#       isDelivery: if order is for delivery
# Return Value:
#       customerInfo: customer's information
def infoCustomer(isDelivery):
    while True: 
        customerInfo = {
            'fistName' : inputCheck("\nPlease enter your first name (ex. John): ").capitalize(),
            'lastName' : inputCheck("Please enter your last name (ex. Smith): ").capitalize(),
            'phoneNumber' : stylePhoneNumber(inputCheck("Please enter your phone number (ex. 5191234567): ", phNum = True))
        }

        if isDelivery:
            customerInfo.update({'streetAddress' : inputCheck("Please enter the address (ex. 123 Main St. Unit 4): ").title()})
            customerInfo.update({'city' : inputCheck("Please enter the city (ex. Waterloo): ").capitalize()})
            customerInfo.update({'province' : input("Please enter the province (ex. Ontario): ").capitalize()})
            customerInfo.update({'postalCode' : inputCheck("Please enter the postal code (ex. A1A1A1): ", psCode = True).upper()})
            customerInfo.update({'specialInstructions' : input("Please enter any special instructions for deliveries to this address (Leave blank if none): ").capitalize()})

        print("\nThe information that you've provided us is:",
        styleCustomerInfo(customerInfo))

        if confirmationDialog("Do we have this correct?",
        "Thank you for providing us with that information. Let's take your order!",
        "Please enter your information again."):
            return customerInfo

# Function orderCustomer
# Description: takes the customer's order
# Parameters:
#       menu: meal names and prices
# Return Value:
#       order: dictionary conataining the customer's order
def orderCustomer(menu):
    order = {
        'mealSelection' : [],
        'quantity' : []
    }

    while True:
        while True:
            print(styleMenu(menu))

            mealSelection = inputCheck("Please select one of our menu items [#]: ", order = len(menu))
            mealQuantity = inputCheck("Please enter how many would you like to order [#]: ", num = True)

            if confirmationDialog("That's {} {}(s). Do we have that right?".format(mealQuantity, menu[mealSelection]['meal'])):
                order['mealSelection'].append(mealSelection)
                order['quantity'].append(mealQuantity)

                break
        if confirmationDialog("Will that be all for today?",
            "Thank you for your order!",
            "To continue you order..."):

            return order

menu = {
    1 : {'meal' : 'cheeseburger', 'price' : 9.5},
    2 : {'meal' : 'hotdog', 'price' : 7},
    3 : {'meal' : 'pizza slice', 'price' : 5},
    4 : {'meal' : 'fries', 'price' : 4.5},
    5 : {'meal' : 'poutine', 'price' : 5.5},
    6 : {'meal' : 'soda', 'price' : 2},
}

#welcome message
print("Hello! Thank you for choosing Arnold's Amazing Eats II!",
    "\nBefore we take your order, we're gonna need a few things to get started.")

#ask if order is for delivery
isDelivery = confirmationDialog("Is this order for delivery?")
#ask if customer is student
isStudent = confirmationDialog("Are you a student?")
#get customer's info
customerInfo = infoCustomer(isDelivery)
#take customer's order
order = orderCustomer(menu)
#print receipt to file and read back
receipt = (styleReceipt(menu, order, isStudent, isDelivery, customerInfo))

with open('receipt.txt', 'w') as aFile:
    aFile.write(receipt)
with open('receipt.txt') as aFile:
    print(aFile.read())