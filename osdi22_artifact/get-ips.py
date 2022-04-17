import ray
import socket
ray.init(address="auto")
d = ray.cluster_resources()
my_addr = socket.gethostbyname(socket.gethostname())
with open("ips", "w") as ips:
    for k in d:
        if k.startswith('node'):
            ip = k.split(':')[1]
            ips.write(ip + "\n")
            print(ip)
