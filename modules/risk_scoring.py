import sys, time, threading, shutil, re, textwrap
from colorama import Fore, Style
from tabulate import tabulate

_USE_ANSI = True
def set_ansi_enabled(enabled: bool):
    global _USE_ANSI
    _USE_ANSI = bool(enabled)

def C(x): return x if _USE_ANSI else ""
def S(x): return x if _USE_ANSI else ""

class LiveRiskScorer:
    WEIGHTS = {"critical": 40, "high": 30, "medium": 15, "low": 5}

    def __init__(self):
        self.score = 0
        self.factors = []
        self._stop_evt = threading.Event()
        self._pulse_thread = None
        self._pulse_started = False

    # ---- internals ----
    def _level(self, s=None):
        s = self.score if s is None else s
        if s <= 30: return "LOW", C(Fore.GREEN)
        if s <= 70: return "MEDIUM", C(Fore.YELLOW)
        return "HIGH", C(Fore.RED)

    def _pulse_worker(self, fixed_score):
        if not _USE_ANSI:
            return
        bar_len = max(10, shutil.get_terminal_size().columns // 4)
        filled = int(bar_len * fixed_score // 100)
        while not self._stop_evt.is_set():
            sys.stdout.write("\r" + f"[{C(Fore.RED)}{'█'*filled}{S(Style.RESET_ALL)}{'░'*(bar_len - filled)}] {fixed_score}%  {C(Fore.RED)}HIGH RISK!{S(Style.RESET_ALL)}")
            sys.stdout.flush(); time.sleep(0.3)
            sys.stdout.write("\r" + f"[{C(Fore.LIGHTWHITE_EX)}{'█'*filled}{S(Style.RESET_ALL)}{'░'*(bar_len - filled)}] {fixed_score}%  {C(Fore.RED)}HIGH RISK!{S(Style.RESET_ALL)}")
            sys.stdout.flush(); time.sleep(0.3)
        sys.stdout.write("\r" + " " * (bar_len + 30) + "\r"); sys.stdout.flush()

    def _maybe_pulse(self):
        lvl, _ = self._level()
        if lvl == "HIGH" and not self._pulse_started:
            self._pulse_started = True
            self._pulse_thread = threading.Thread(target=self._pulse_worker, args=(self.score,), daemon=True)
            self._pulse_thread.start()

    # ---- API ----
    def add_finding(self, factor: str, severity: str):
        sev = (severity or "low").lower().strip()
        self.score = min(100, self.score + self.WEIGHTS.get(sev, 0))
        self.factors.append(factor)
        self._maybe_pulse()

    def add_many(self, findings):
        for f in findings or []:
            self.add_finding(f.get("factor", "Unspecified finding"), f.get("severity", "low"))

    def finalize(self):
        if self._pulse_started:
            self._stop_evt.set()
            time.sleep(0.1)
        return {"risk_score": self.score, "factors": list(self.factors)}

    def _colored_factors(self):
        sev_map = {
            "critical": C(Fore.RED), "high": C(Fore.RED),
            "vulnerable": C(Fore.RED), "vulnerability": C(Fore.RED),
            "exposed": C(Fore.RED), "breach": C(Fore.RED), "compromise": C(Fore.RED),
            "open port": C(Fore.YELLOW), "ssl expired": C(Fore.YELLOW),
            "weak": C(Fore.YELLOW), "suspicious": C(Fore.YELLOW),
            "low": C(Fore.GREEN), "secure": C(Fore.GREEN)
        }
        colored = []
        for f in self.factors:
            low = f.lower(); color = ""
            for k, c in sev_map.items():
                if re.search(rf"\b{re.escape(k)}\b", low):
                    color = c; break
            colored.append(f"{color}{f}{S(Style.RESET_ALL) if color else ''}")
        return colored

    def _progress_bar(self):
        width = shutil.get_terminal_size().columns
        bar_len = max(10, width // 4)
        filled = int(bar_len * self.score // 100)
        lvl, color = self._level()
        if _USE_ANSI:
            bar = f"{color}{'█'*filled}{S(Style.RESET_ALL)}{'░'*(bar_len - filled)}"
        else:
            bar = f"{'#'*filled}{'.'*(bar_len - filled)}"
        return f"[{bar}] {self.score}%", lvl, color

    def render_table(self):
        progress, lvl_text, lvl_color = self._progress_bar()
        wrap_w = max(30, shutil.get_terminal_size().columns // 3)
        wrapped = textwrap.fill(", ".join(self._colored_factors()), width=wrap_w)
        return tabulate(
            [[progress, f"{lvl_color}{lvl_text}{S(Style.RESET_ALL)}", wrapped]],
            headers=["Risk Score", "Risk Level", "Key Risk Factors"],
            tablefmt="fancy_grid"
        )
