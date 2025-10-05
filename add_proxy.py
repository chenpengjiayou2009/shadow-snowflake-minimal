import argparse

def add_proxy(start:int, num:int):
    with open("snowflake.yaml", 'a') as f:
        for i in range(start, start+num):
            f.write(f"  proxy{i}: *proxy\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample script demonstrating argument parsing.")
<<<<<<< Updated upstream
    parser.add_argument("--proxies", type=int, help="number of clients to append.", default=450)
    args = parser.parse_args()
    add_proxy(150, args.proxies)
=======
    parser.add_argument("--proxies", type=int, help="number of clients to append.", default=570)
    args = parser.parse_args()
    add_proxy(30, args.proxies)
>>>>>>> Stashed changes
