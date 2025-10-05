import argparse

def add_proxy(start:int, num:int):
    with open("snowflake.yaml", 'a') as f:
        for i in range(start, start+num):
            f.write(f"  standalone-proxy{i}: *standalone-proxy\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample script demonstrating argument parsing.")
    parser.add_argument("--proxies", type=int, help="number of clients to append.", default=38)
    args = parser.parse_args()
    add_proxy(3, args.proxies)
