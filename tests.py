from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

def main():
    #print(f"Result for current directory:\n{get_files_info("calculator", ".")}")
    #print(f"Result for 'pkg' directory:\n{get_files_info("calculator", "pkg")}")
    #print(f"Result for '/bin' directory:\n{get_files_info("calculator", "/bin")}")
    #print(f"Result for '../' directory:\n{get_files_info("calculator", "../")}")

    #print(get_file_content("calculator", "lorem.txt"))
    #print(f"Test 1:\n{get_file_content("calculator", "main.py")}\n")
    #print(f"Test 2:\n{get_file_content("calculator", "pkg/calculator.py")}\n")
    #print(f"Test 3:\n{get_file_content("calculator", "/bin/cat")}")

    
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    
if __name__ == "__main__":
    main()