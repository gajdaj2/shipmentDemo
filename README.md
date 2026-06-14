# Lab 2 — Aktywny rekonesans z nmap (90 min)

## Cel
Zrozumieć działanie skanera portów, opanować praktyczne tryby skanowania, NSE i interpretację wyników.

## Plan
| Czas | Ćwiczenie |
|------|-----------|
| 0–25 min | Teoria (slajdy): TCP handshake, stany portów, tryby skanowania |
| 25–40 min | **Ex 2.1** — Pierwszy skan na `scanme.nmap.org` |
| 40–55 min | **Ex 2.2** — Skan localhost / docker network |
| 55–75 min | **Ex 2.3** — NSE scripts (vuln, http-enum, ssl-enum-ciphers) |
| 75–85 min | **Ex 2.4** — Porównanie nmap vs masscan vs rustscan |
| 85–90 min | Eksport do XML + searchsploit |

---

## ⚠️ Co wolno skanować

| Cel | Zgoda |
|-----|-------|
| `scanme.nmap.org` | ✅ Oficjalnie udostępniony przez projekt Nmap |
| `localhost`, `127.0.0.1` | ✅ Twoja maszyna |
| `172.17.0.0/24` (docker network w Codespace) | ✅ Twoje kontenery |
| Cokolwiek innego | ❌ **NIE skanuj** — narusza Codespace TOS i prawo |

---

## Ex 2.1 — Pierwszy skan

```bash
# Najbardziej podstawowy skan — Top 1000 TCP portów
nmap scanme.nmap.org

# Co zobaczysz:
# Nmap scan report for scanme.nmap.org (45.33.32.156)
# Host is up (0.15s latency).
# Not shown: 994 closed tcp ports (reset)
# PORT      STATE    SERVICE
# 22/tcp    open     ssh
# 80/tcp    open     http
# 9929/tcp  open     nping-echo
# 31337/tcp open     Elite
```

### Service & version detection
```bash
nmap -sV scanme.nmap.org
```
Zwróć uwagę na pole `VERSION` — to klucz do `searchsploit` w labie 4.

### Default scripts + version
```bash
nmap -sC -sV scanme.nmap.org
# -sC = --script=default — bezpieczne skrypty enumerujące
```

### Aggressive (najwięcej info, najbardziej "głośny")
```bash
nmap -A scanme.nmap.org
# -A = -sV + -sC + -O (OS detection) + traceroute
```

**Pytania:**
- Jaką wersję OpenSSH widzi nmap?
- Czy `-O` poprawnie zgaduje system operacyjny? Dlaczego mogło zawieść?
- Ile czasu zajął skan z `-A` vs domyślny?

---

## Ex 2.2 — Skan własnej infry (Juice Shop + DVWA)

Najpierw upewnij się, że cele działają:
```bash
docker compose ps
```

Znajdź IP kontenerów w sieci docker:
```bash
docker network inspect pentest-lab | grep -A 2 IPv4Address
```

Skan localhost (porty wystawione przez compose):
```bash
nmap -p 3000,8080,8081,8082,8090 -sV localhost
```

Skan całej sieci docker:
```bash
NETWORK=$(docker network inspect pentest-lab -f '{{(index .IPAM.Config 0).Subnet}}')
echo "Sieć: $NETWORK"
nmap -sn "$NETWORK"          # ping sweep — które hosty żyją
nmap -sV -p- "$NETWORK"      # wszystkie 65535 portów + wersje (uwaga — wolne!)
```

**Pytania:**
- Dlaczego `-sn` (ping sweep) może nie zadziałać na niektórych sieciach?
- Co znaczy stan `filtered`?
- Czemu skan **wszystkich** portów (`-p-`) trwa wielokrotnie dłużej?

---

## Ex 2.3 — NSE: skrypty NSE

NSE = Nmap Scripting Engine. Ponad 600 skryptów, podzielone na kategorie.

### Kategorie
```bash
nmap --script-help "default" | head -30
# Inne kategorie: safe, auth, vuln, exploit, intrusive, malware, discovery, dos
```

### Skanowanie HTTP — enumeracja katalogów
```bash
nmap -p 3000 --script http-enum localhost
```

### Skan podatności (vuln)
```bash
nmap -p 3000 --script vuln localhost
# Trochę false positives, ale warto przejrzeć
```

### SSL/TLS ciphers
```bash
# Zewnętrzny target z HTTPS
nmap -p 443 --script ssl-enum-ciphers scanme.nmap.org
```

### Konkretny skrypt na konkretne CVE
```bash
nmap -p 3000 --script http-shellshock localhost
nmap -p 3000 --script http-sql-injection localhost
```

**Pytania:**
- Który skrypt zwrócił najbardziej użyteczny output?
- Czy widzisz różnicę między `safe` a `intrusive`?
- Jak skierowałbyś NSE wyłącznie na 1 konkretną podatność?

---

## Ex 2.4 — Alternatywy: masscan, rustscan

```bash
# Instalacja masscan
sudo apt-get install -y masscan

# masscan — bardzo szybki, ale tylko port discovery (bez wersji)
sudo masscan -p1-65535 127.0.0.1 --rate=1000
```

```bash
# rustscan — wrapper który robi szybki port discovery i pipuje do nmap
docker run -it --rm --net=host rustscan/rustscan:latest -a 127.0.0.1 -- -sV -sC
```

**Pytanie do dyskusji:** kiedy używamy masscan/rustscan, a kiedy "czystego" nmap?

---

## Ex 2.5 — Eksport i integracja z exploit-db

```bash
# Eksport do XML
nmap -sV -sC -oX scan.xml scanme.nmap.org

# Eksport do wszystkich formatów (XML, normal, grep)
nmap -sV -sC -oA scanme scanme.nmap.org
ls -la scanme.*

# searchsploit potrafi parsować nmap XML i sugerować exploity
searchsploit --nmap scan.xml
```

**Pytanie:** dlaczego sugestie searchsploit traktować z dużą ostrożnością? Co znaczy "kandydat do dalszej weryfikacji"?

---

## Deliverable Labu 2

Stwórz `nmap-report.md` z trzema sekcjami:

1. **Zewnętrzny cel** (scanme.nmap.org): porty + wersje + 1 obserwacja z NSE
2. **Wewnętrzny cel** (jeden z kontenerów docker): porty + wersje + co działa na danym porcie
3. **Hipotezy ataku** — co byś próbował na podstawie wykrytych wersji?

To input do Labu 3 i 4.

---

## Cheatsheet — najczęstsze flagi

| Flag | Działanie |
|------|-----------|
| `-sS` | SYN stealth scan (default jeśli root) |
| `-sT` | Full TCP connect (jeśli brak root) |
| `-sU` | UDP scan (wolny, dużo "open\|filtered") |
| `-sV` | Service version detection |
| `-sC` | Default scripts (`--script=default`) |
| `-A` | Aggressive (-sV -sC -O --traceroute) |
| `-O` | OS detection |
| `-Pn` | Skip ping (target blokuje ICMP) |
| `-p-` | Wszystkie 65535 portów |
| `-p 80,443,8000-9000` | Konkretne porty/zakresy |
| `-T0..T5` | Timing: T0 paranoid (audyt), T3 default, T4/T5 agresywne |
| `--top-ports 100` | Top 100 najczęstszych portów |
| `--open` | Pokaż tylko otwarte porty |
| `--reason` | Pokaż, czemu nmap uznał port za open/closed |
| `-oA <basename>` | Output w 3 formatach (XML/normal/grep) |
| `-vv` | Verbose (zobaczysz progress) |

---

## Materiały dodatkowe

- Nmap Reference: https://nmap.org/book/man.html
- NSE script database: https://nmap.org/nsedoc/
- "Nmap Network Scanning" — Gordon Lyon (autor nmap) — bezpłatny rozdział online
