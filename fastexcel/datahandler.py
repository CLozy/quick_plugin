import pandas as pd



def excel_to_csv(file):
    extracted_data = pd.read_excel(file)
    extracted_data.to_csv(f"fastexcel\data\{file.name[:-4]}.csv", index=False)
