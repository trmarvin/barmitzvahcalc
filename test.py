# from datetime import datetime

# print("Trying with %Y-%m-%d:")
# try:
#     print(datetime.strptime("1978-23-06", "%Y-%m-%d"))
# except ValueError as e:
#     print("Error:", e)

# print("\nTrying with %Y-%d-%m:")
# print(datetime.strptime("1978-23-06", "%Y-%d-%m"))

from datetime import datetime
print(datetime.strptime("1978-23-06", "%Y-%m-%d"))