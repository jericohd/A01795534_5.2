"""
Module: compute_sales

This script reads a price catalogue and a sales record from JSON files,
computes the total sales, handles errors, and writes the results to a file.
"""

import sys
import json
import time


def load_json(file_path):
    """Loads and returns data from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Error loading {file_path}: {error}")
        sys.exit(1)



def compute_total_sales(price_catalogue, sales_record):
    """Computes total sales and identifies errors in the data."""
    total_sales = 0
    errors = []

    for sale in sales_record:
        product = sale.get("product")
        quantity = sale.get("quantity")

        if product not in price_catalogue:
            errors.append(
                f"Warning: Product '{product}' not found in price catalogue."
            )
            continue

        if not isinstance(quantity, (int, float)) or quantity < 0:
            errors.append(
                f"Warning: Invalid quantity for product '{product}'. Skipping entry."
            )
            continue

        total_sales += price_catalogue[product] * quantity

    return total_sales, errors



def save_results(total_sales, errors, elapsed_time):
    """Writes the sales report to a file."""
    with open("SalesResults.txt", "w", encoding="utf-8") as file:
        file.write("==== Sales Report ====\n")
        file.write(f"Total Sales: ${total_sales:.2f}\n")
        file.write(f"Execution Time: {elapsed_time:.4f} seconds\n\n")

        if errors:
            file.write("==== Errors ====\n")
            for error in errors:
                file.write(f"{error}\n")

    print("Results saved to SalesResults.txt")



def main():
    """Main function to read files, compute sales, and save results."""
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)

    price_catalogue_file, sales_record_file = sys.argv[1], sys.argv[2]

    start_time = time.time()
    price_catalogue = load_json(price_catalogue_file)
    sales_record = load_json(sales_record_file)

    total_sales, errors = compute_total_sales(price_catalogue, sales_record)
    elapsed_time = time.time() - start_time

    print(f"Total Sales: ${total_sales:.2f}")
    print(f"Execution Time: {elapsed_time:.4f} seconds")

    if errors:
        print("Warnings:")
        for error in errors:
            print(error)

    save_results(total_sales, errors, elapsed_time)


if __name__ == "__main__":
    main()
