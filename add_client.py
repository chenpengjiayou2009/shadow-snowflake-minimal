import argparse

def add_client(start:int, num:int):
    with open("snowflake.yaml", 'a') as f:
        for i in range(start, start+num):
            f.write(f"""
  snowflakeclient-{i}:
    network_node_id: 0
    processes:
    - path: ~/.local/bin/snowflake-client
      environment:
        TOR_PT_MANAGED_TRANSPORT_VER: "1"
        TOR_PT_CLIENT_TRANSPORTS: snowflake
      args: -ice "stun:stun:3478" -url "http://broker:8080" -keep-local-addresses -log "pt.log" -unsafe-logging
      start_time: {90+i*5}
      shutdown_time: {130+i*5}
    # The following snippet was developed by the proteus authors and used with their permission
    # https://github.com/unblockable/proteus/blob/99751539b78782d4477411786e4df03b68213e5d/tests/linux/shadow/tgen/shadow.yaml.template#L53-L69
    - path: python3
      args: |
        -c "def getport():
          with open('snowflake-client.1000.stdout', 'r') as fin:
            for line in fin:
              if line.startswith('CMETHOD snowflake socks5 127.0.0.1:'):
                return line.strip().split(' ')[3].split(':')[1]
          return '0'
        with open('../../../conf/tgen.client.graphml.xml','r') as fin:
          data = fin.read().replace('SOCKS5LISTENPORT', getport())
        with open('tgen.client.graphml.xml','w') as fout:
          fout.write(data)"
      environment: {{ PYTHONUNBUFFERED: "1" }}
      start_time: {100+i*5}
      shutdown_time: {130+i*5}
      expected_final_state: {{exited: 0}}
    - path: ~/.local/bin/tgen
      args: tgen.client.graphml.xml
      start_time: {120+i*5}
""")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample script demonstrating argument parsing.")
    parser.add_argument("--clients", type=int, help="number of clients to append.", default=500)
    args = parser.parse_args()
<<<<<<< Updated upstream
    add_client(501, args.clients)
=======
    add_client(0, args.clients)
>>>>>>> Stashed changes
