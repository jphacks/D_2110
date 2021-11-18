import sys


def main():
    """Insert API URL into index.html"""
    file = "index.html"
    api_url = sys.argv[1]

    with open(file, "r") as f:
        text = f.read()

    with open(file, "w") as f:
        f.write(text.replace("API_URL", api_url))


if __name__ == "__main__":
    main()
