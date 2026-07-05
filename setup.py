import random
import string

from api.database.sqlite import database

def random_string(length=12):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def random_port():
    """Generate a random port between 1024 and 65535."""
    return random.randint(1024, 65535)


def setup(manual=False):
    cursor, conn = database()

    if manual:
        username = input("Enter username: ")
        password = input("Enter password: ")
        port = int(input("Enter port: "))
    else:
        username = random_string(8)
        password = random_string(12)
        port = 1990
        
    key = random_string(16)
    secret = random_string(32)

    # Insert into USERS
    cursor.execute(
        "INSERT INTO USERS (username, password) VALUES (?, ?)",
        (username, password)
    )

    # Insert into CONFIGS
    configs = [
        ("port", str(port)),
        ("key", key),
        ("secret", secret),
    ]

    cursor.executemany(
        "INSERT INTO CONFIGS (key, value) VALUES (?, ?)",
        configs
    )

    conn.commit()
    conn.close()

    print("Setup completed successfully!")
    print(f"User: {username}")
    print(f"Password: {password}")
    print(f"Port: {port}")
    print(f"Key: {key}")
    print(f"Secret: {secret}")

if __name__ == "__main__":
    setup(manual=False)
