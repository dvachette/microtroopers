import sys
from werkzeug.security import generate_password_hash

def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <password>')
        sys.exit(1)
    password = sys.argv[1]
    print(generate_password_hash(password))

if __name__ == '__main__':
    main()