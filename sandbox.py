# import requests
# import tempfile


# def get_image(url):
#     request = requests.get(url, stream=True)
import re
#     if request.status_code == 200:
#         file_name = "-".join((url.split('/')[-2::]))
#         print(file_name)

#         lf = tempfile.NamedTemporaryFile()

#         # Read the streamed image in sections
#         for block in request.iter_content(1024 * 8):

#             # If no more file then stop
#             if not block:
#                 break

#             # Write image block to temporary file
#             lf.write(block)

#         print(lf)


# t = get_image("https://images.pokemontcg.io/sm4/30.png")

# print(t)


t = ["Charizard-ex", "Charizard ex", "Charizard_ex"]

for i in t:
    print(re.split(r"[\W+|_']+", i))
