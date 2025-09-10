import argparse

def add_proxy(num:int):
    with open("snowflake.yaml", 'a') as f:
        for i in range(num):
            f.write(f"  proxy{i}: *proxy\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample script demonstrating argument parsing.")
    parser.add_argument("--proxies", type=int, help="number of clients to append.", default=29)
    args = parser.parse_args()
    add_proxy(args.proxies)