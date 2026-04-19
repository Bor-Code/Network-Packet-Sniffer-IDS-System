import queue
from scapy.all import sniff, IP, TCP, UDP

packet_queue = queue.Queue(maxsize=10000)

def extract_features(pkt):
    return {
        "timestamp": float(pkt.time),
        "src_ip":    pkt[IP].src,
        "dst_ip":    pkt[IP].dst,
        "src_port":  pkt[TCP].sport if TCP in pkt else pkt[UDP].sport if UDP in pkt else 0,
        "dst_port":  pkt[TCP].dport if TCP in pkt else pkt[UDP].dport if UDP in pkt else 0,
        "protocol":  pkt[IP].proto,
        "flags":     str(pkt[TCP].flags) if TCP in pkt else "",
    }

def packet_callback(pkt):
    if IP in pkt:
        packet_queue.put(extract_features(pkt))

def sniff_packets():
    print("[*] Ağ arayüzü dinleniyor, paketler yakalanıyor...")
    sniff(prn=packet_callback, store=False)
    