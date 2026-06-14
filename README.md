# 📦 Shipment API

REST API do zarządzania przesyłkami, zbudowane w **FastAPI** z walidacją danych przez **Pydantic**.

## 🚀 Tech Stack

| Technologia | Wersja |
|---|---|
| Python | ≥ 3.13 |
| FastAPI | ≥ 0.136 |
| Pydantic | v2 |
| Scalar (docs UI) | ≥ 1.8 |
| uv (package manager) | latest |

## 📋 Funkcjonalności

- ✅ Pobieranie wszystkich przesyłek
- ✅ Pobieranie przesyłki po ID
- ✅ Pobieranie konkretnego pola przesyłki
- ✅ Dodawanie nowej przesyłki
- ✅ Aktualizacja przesyłki (PUT)
- ✅ Częściowa aktualizacja pola (PATCH)
- ✅ Aktualizacja statusu przesyłki
- ✅ Usuwanie przesyłki
- ✅ Walidacja danych wejściowych (Pydantic + Field)
- ✅ Interaktywna dokumentacja API (Scalar UI)

## 📌 Endpointy

| Metoda | Endpoint | Opis |
|---|---|---|
| `GET` | `/shipments` | Pobierz wszystkie przesyłki |
| `GET` | `/shipment` | Pobierz przesyłkę (ostatnią lub po `?id=`) |
| `GET` | `/shipment/{field}?id=` | Pobierz konkretne pole przesyłki |
| `POST` | `/shipment` | Dodaj nową przesyłkę |
| `PUT` | `/shipment/{id}` | Zaktualizuj całą przesyłkę |
| `PATCH` | `/shipment/{id}` | Zaktualizuj status przesyłki |
| `PATCH` | `/shipment/{field}?id=` | Zaktualizuj konkretne pole |
| `GET` | `/scalar` | Dokumentacja API (Scalar UI) |

## 🗂️ Model danych

```json
{
  "weight": 12.5,
  "content": "Electronics",
  "status": "In transit"
}
```

**Statusy przesyłki:**
- `In transit`
- `Delivered`
- `Pending`
- `Cancelled`

## ⚙️ Instalacja i uruchomienie

```bash
# Klonowanie repo
git clone https://github.com/gajdaj2/shipmentDemo.git
cd shipmentDemo

# Instalacja zależności (uv)
uv sync

# Uruchomienie serwera
uv run fastapi dev main.py
```

Serwer będzie dostępny pod adresem: `http://localhost:8000`  
Dokumentacja Scalar: `http://localhost:8000/scalar`

## 🏗️ Struktura projektu

```
├── main.py                      # Główna aplikacja FastAPI
├── models/
│   └── shipment_model.py        # Model Pydantic (ShipmentModel)
├── db.py                        # In-memory baza danych
├── check_shipment_field.py      # Walidacja pola przesyłki
├── check_shipment_requirements.py # Walidacja wymaganych pól
└── pyproject.toml               # Konfiguracja projektu
```
