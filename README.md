# Adaptive Access Control PDP

FastAPI-сервис (PDP) для адаптивного управления доступом. Принимает 4 признака поведения пользователя, вычисляет уровень риска `R` и возвращает фазу: `GREEN`, `GRAY`, `BLACK`.

## Требования

- Python 3.8+
- pip

## Установка

```bash
pip install fastapi uvicorn pydantic pandas requests
```

## Запуск API

```bash
python main.py
```

Сервер: `http://127.0.0.1:8001`

## API

### POST `/v1/authz`

**Запрос:**

```json
{"t": 1, "d": 0, "a": 1, "c": 5}
```

**Ответ:**

```json
{"riskScore": 3.245, "phase": "GRAY"}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `t` | int | Нерабочее время (0/1) |
| `d` | int | Нештатное устройство (0/1) |
| `a` | int | Нетипичное действие (0/1) |
| `c` | int | Кол-во системных команд |

**Фазы:**

- `R ≤ 2` → `GREEN`
- `2 < R ≤ 6` → `GRAY`
- `R > 6` → `BLACK`

## Валидация на CERT r4.2

Положите `all_features.csv` в корень проекта.

```bash
python validate_cert.py
```

Результат: `data/predictions_cert.csv` (колонки: `user`, `predicted_R`, `predicted_phase`).

## Структура

```
├── main.py              # FastAPI-приложение (PDP)
├── validate_cert.py     # Валидация на CERT r4.2
├── all_features.csv     # Признаки из CERT r4.2
├── data/
│   └── predictions_cert.csv
└── README.md
```

## Быстрая проверка

```bash
curl -X POST http://127.0.0.1:8001/v1/authz \
  -H "Content-Type: application/json" \
  -d '{"t":1,"d":0,"a":1,"c":5}'
```
