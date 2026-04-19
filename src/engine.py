from collections import defaultdict

class AnalysisEngine:
    def __init__(self):
        self.syn_tracker  = defaultdict(list)   
        self.port_tracker = defaultdict(set)    

    def analyze(self, feat):
        alerts = []
        src = feat["src_ip"]
        now = feat["timestamp"]

        self.port_tracker[src].add(feat["dst_port"])
        if len(self.port_tracker[src]) > 15:
            alerts.append({"type": "PORT_SCAN", "src": src, "severity": "HIGH"})

        if "S" in feat["flags"] and "A" not in feat["flags"]:
            self.syn_tracker[src].append(now)
            self.syn_tracker[src] = [t for t in self.syn_tracker[src] if now - t < 1]
            if len(self.syn_tracker[src]) > 100:
                alerts.append({"type": "SYN_FLOOD", "src": src, "severity": "CRITICAL"})

        return alerts