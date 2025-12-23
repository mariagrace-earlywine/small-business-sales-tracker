import csv

#This list will hold all your sales while the program is running
sales = []
FILENAME = "sales.csv" # this file will live in the same folder as main.py

def save_sales_to_csv():
    """
    Save all sales to a CSV file in the project folder.
    """
    with open(FILENAME, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["date", "customer", "description", "amount"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()  # first row: column names
        for sale in sales:
            writer.writerow(sale)

    print(f"Saved {len(sales)} sale(s) to {FILENAME}.")

def load_sales_from_csv():
    """
    Load sales from the CSV file (if it exist) into the sales list.
    """
    try:
        with open(FILENAME, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # row values are strings, so convert amount to float
                try:
                    amount = float(row["amount"])
                except (KeyError, ValueError):
                    continue #skip bad rows

                sale = {
                    "date": row.get("date", ""),
                    "customer": row.get("customer", ""),
                    "description": row.get("description", ""),
                    "amount": amount,
                }
                sales.append(sale)

        if sales:
            print(f"Loaded {len(sales)} sale(s) from {FILENAME}.")
        else:
            print("Sales file is empty. Starting fresh.")
    except FileNotFoundError:
        print("No previous sales file found. Starting fresh.")


def add_sale():
    """
    Asks the user to enter their sales and adds them to the sales list.
    """
    print("\n=== Add a new sale ===")
    date = input("Date (YYYY-MM-DD): ")
    customer = input("Customer name: ")
    description = input("Products / notes: ")
    amount_str = input("Total amount (just numbers, e.g. 45.50): ")

    # Try to turn the amount into a number (float).
    # If it fails, we don't add the sale.
    try:
        amount = float(amount_str)
    except ValueError:
        print("Invalid amount. Sale not saved.")
        return

    sale = {
        "date": date,
        "customer": customer,
        "description": description,
        "amount": amount,
    }

    sales.append(sale)
    print("✅ Sale added!")
    save_sales_to_csv()


def list_sales():
    """
    Display all recorded sales and show the total.
    """
    print("\n=== Sales so far ===")
    if not sales:
        print("No sales recorded yet.")
        return

    total = 0.0
    for idx, sale in enumerate(sales, start=1):
        print(f"{idx}. {sale['date']} | {sale['customer']} | "
              f"{sale['amount']:.2f} | {sale['description']}")
        total += sale["amount"]

    print(f"\nTotal sales: ${total:2f}")


def show_summary():
    """
    Show a quick summary of all recorded sales.
    """
    print("\n=== Sales Summary ===")
    if not sales:
        print("No sales recorded yet.")
        return

    total = 0.0
    count = len(sales)
    max_sale = sales[0]

    for sale in sales:
        total += sale["amount"]
        if sale["amount"] > max_sale["amount"]:
            max_sale = sale

    average = total / count

    print(f"Number of sales: {count}")
    print(f"Total sales: ${total:.2f}")
    print(f"Average sale: ${average:.2f}")
    print(f"Biggest sale: ${max_sale['amount']:.2f} "
          f"({max_sale['date']} - {max_sale['customer']})")


def show_monthly_total():
    """
    Show total sales for a specific year and month.
    """
    print("\n=== Monthly Total ===")
    if not sales:
        print("No sales recorded yet.")
        return

    year = input("Year (e.g. 2025): ").strip()
    month_str = input("Month (1-12): ").strip()

    # validate month (must be an integer from 1 to 12)
    try:
        month_num = int(month_str)
        if not 1 <= month_num <= 12:
            raise ValueError
    except ValueError:
        print("Invalid month. Please enter a number from 1-12.")
        return

    # Format month as two digits, e.g. 1 -> "01", 11 -> "11"
    month_formatted = f"{month_num:02d}"

    # We'll look for dates that start with "YYYY-MM-"
    prefix = f"{year}-{month_formatted}-"

    total = 0.0
    count = 0

    for sale in sales:
        date = sale.get("date", "")
        if date.startswith(prefix):
            count += 1
            total += sale["amount"]

    if count == 0:
        print(f"No sales found for {year}-{month_formatted}.")
    else:
        print(f"\nSales for {year}-{month_formatted}:")
        print(f"Number of sales: {count}")
        print(f"Total sales: ${total:.2f}")
        print(f"Average sale: ${total / count:.2f} ")

def main():
    """
    Main menu loop.
    """
    load_sales_from_csv() # Loads saved sales (if any) when the app starts

    while True:
        print("\n--- Mary Kay Sales Tracker ---")
        print("1) Add a sale")
        print("2) List sales")
        print("3) Show summary")
        print("4) Show monthly total")
        print("5) Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            add_sale()
        elif choice == "2":
            list_sales()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            show_monthly_total()
        elif choice == "5":
            print("Goodbye! 💗")
            break
        else:
            print("Please enter 1, 2, 3, 4 or 5.")

if __name__ == "__main__":
    main()
