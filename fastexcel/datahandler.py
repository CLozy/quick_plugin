
import pandas as pd



# def excel_to_csv(file):
#     extracted_data = pd.read_excel(file)
#     extracted_data.to_csv(f"fastexcel\files\{file.name[:-5]}.csv", index=False)

def extract_excel(file):
    # print(file)
    extracted_data = pd.read_excel(file['file'])
    return extracted_data.columns.tolist()


# print(extract_excel("files\P051133258U.xlsx"))