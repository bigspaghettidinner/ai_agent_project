from functions.get_file_content import get_file_content
from config import MAX_CHARS

result = get_file_content("calculator", "lorem.txt")
expected_end = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
print (len(result))
print (result.endswith(expected_end))

result = get_file_content("calculator", "main.py")
print(result)

result = get_file_content("calculator", "pkg/calculator.py")
print(result)

result = get_file_content("calculator", "/bin/cat")
print(result)

result = get_file_content("calculator", "pkg/does_not_exist.py")
print(result)
