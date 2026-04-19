import time
from scapy.all import IP, TCP, send

TARGET_IP = "127.0.0.1"

def simulate_port_scan():
    print(f"[*] {TARGET_IP} hedefine Port Taraması (Port Scan) başlatılıyor...")
    for port in range(20, 41):
        pkt = IP(dst=TARGET_IP)/TCP(dport=port, flags="S")
        send(pkt, verbose=False)
    print("[+] Port taraması tamamlandı.\n")

def simulate_syn_flood():
    print(f"[*] {TARGET_IP} hedefine SYN Flood saldırısı başlatılıyor...")
    for _ in range(120):
        pkt = IP(dst=TARGET_IP)/TCP(dport=80, flags="S")
        send(pkt, verbose=False)
    print("[+] SYN Flood tamamlandı.\n")

if __name__ == "__main__":
    print("--- NeuralLock IDS Saldırı Simülatörü ---")
    simulate_port_scan()
    
    print("[*] 3 saniye bekleniyor...\n")
    time.sleep(3)
    
    simulate_syn_flood()
    print("--- Tüm test saldırıları gönderildi ---")