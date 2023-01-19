import pandas as pd
import os

def populate_db():
    csv_file = "prev_data.csv"
    filename = os.path.dirname(os.path.abspath(__file__)) + "\\" + csv_file

    df = pd.read_csv(filename)
    for index, row in df.iterrows():
        # print(row)
        # print(row['entity_id'])
        # print(row['name'])
        # print(row['address'])
        # print(row['review_id'])
        # print(row['review'])
        # print("NEXT")
        pass

populate_db()