import os
import pandas as pd
import sqlite3
import requests

url1 = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/sdg_13_10?format=TSV&compressed=false"
url2 = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nrg_ind_ren?format=TSV&compressed=false"


data_dir = "data"
csv_paths = {
    "Neelima_data1": os.path.join(data_dir, "net_greenhouse_gas_emissions.csv"),
    "Neelima_data2": os.path.join(data_dir, "share_of_energy_from_renewable_sources.csv")
}
database_paths = {
    "database1": os.path.join(data_dir, "database1.db"),
    "database2": os.path.join(data_dir, "database2.db")
}


if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def download_file(url, file_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


download_file(url1, csv_paths["Neelima_data1"])
download_file(url2, csv_paths["Neelima_data2"])


df1 = pd.read_csv(csv_paths["Neelima_data1"], delimiter='\t')
df2 = pd.read_csv(csv_paths["Neelima_data2"], delimiter='\t')


df1.fillna(0, inplace=True)
df2.fillna(0, inplace=True)


df1.columns = [col.strip().lower() for col in df1.columns]
df2.columns = [col.strip().lower() for col in df2.columns]

def save_to_sqlite(df, db_path, table_name):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

save_to_sqlite(df1, database_paths["database1"], "net_greenhouse_gas_emissions")
save_to_sqlite(df2, database_paths["database2"], "share_of_energy_from_renewable_sources")

print("Data pipeline execution completed.")
