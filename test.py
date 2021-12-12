import os

curr = os.getcwd()
root = os.path.dirname(curr)

folder_name = "finance_data_getter\\files"
stored_file_loc = os.path.join(root, folder_name)
print(stored_file_loc)
