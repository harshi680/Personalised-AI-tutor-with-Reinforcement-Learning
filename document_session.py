# document_csv.py
import csv

def save_doc_session(data, filename="doc_session.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        for key, value in data.items():
            writer.writerow([key, value])

def load_doc_session(filename="doc_session.csv"):
    session = {}
    try:
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    session[row[0]] = row[1]
    except FileNotFoundError:
        pass
    return session
