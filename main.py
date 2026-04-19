import threading
import time
from src.capture import sniff_packets, packet_queue
from src.engine import AnalysisEngine
from src.gui import IDSGui

class IDSController:
    def __init__(self):
        self.engine = AnalysisEngine()
        self.gui = IDSGui(start_callback=self.start_sniffing)
        self.is_sniffing = False

    def start_sniffing(self):
        if not self.is_sniffing:
            self.is_sniffing = True
            self.gui.log_alert("Sistem Başlatıldı. Ağ trafiği dinleniyor...")
            sniff_thread = threading.Thread(target=sniff_packets, daemon=True)
            sniff_thread.start()
            
            analyze_thread = threading.Thread(target=self.process_traffic, daemon=True)
            analyze_thread.start()

    def process_traffic(self):
        """Kuyruktaki paketleri alır, arayüze yazar ve tehdit analizi yapar."""
        while True:
            if not packet_queue.empty():
                packet_data = packet_queue.get()
                
                self.gui.update_table(packet_data)
                
                alerts = self.engine.analyze(packet_data)
                
                # 3. Eğer tehdit varsa arayüzdeki kırmızı ekrana bas
                for alert in alerts:
                    msg = f"[{alert['severity']}] {alert['type']} Tespit Edildi! Kaynak IP: {alert['src']}"
                    self.gui.log_alert(msg)
            else:
                time.sleep(0.01) 

    def run(self):
        self.gui.mainloop()

if __name__ == "__main__":
    app = IDSController()
    app.run()