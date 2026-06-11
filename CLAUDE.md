# Content Maker Agent

Веб-приложение для генерации постов в Telegram-каналы. Поддерживает несколько AI-провайдеров — работает как с облачными API (Claude, ChatGPT), так и локально (Ollama) без интернета и VPN.

## Каналы

| ID | Название | Тематика |
|---|---|---|
| `mice_japan` | MICE Japan | MICE-туризм в Японию: отели, гастрономия, культура, логистика групп |
| `match_point` | MATCH POINT | MICE в России и мире: тренды, новости рынка, обзоры площадок и отелей |
| `turdezhur` | ТурДежурный | AI-решения для отелей и турфирм; канал продаёт AI-продукты автора |

Автор всех каналов — Ольга Харлёнок. Голос единый, подача разная под аудиторию.

## Стек

- **Backend:** Python / Flask
- **AI-провайдеры:** Claude (Anthropic), OpenAI (GPT-4o-mini), GigaChat (Сбер), Ollama (локально)
- **Frontend:** Vanilla HTML/CSS/JS, тёмная тема
- **Промпты:** `prompts.py` — system prompt + ЦА + few-shot примеры из `examples.json`

## Структура файлов

```
app.py              — Flask-сервер: /generate, /set_provider, /health
prompts.py          — промпты, ЦА и характеры каналов; грузит примеры из examples.json
examples.json       — реальные посты каналов (few-shot), парсится из docx
.env                — API ключи и выбор провайдера (не в git)
templates/
  index.html        — весь фронтенд
Match Point/
  posts Match Point.docx   — исходные посты канала
MICE Japan/
  Posts Mice Japan.docx    — исходные посты канала
Turdezhur/          — папка под будущие посты канала (docx пока нет)
START.md            — инструкция по установке и запуску
requirements.txt    — flask, requests, anthropic, openai
```

## Запуск

```bash
pip install -r requirements.txt
python app.py
# Открыть: http://localhost:5000
```

Для Ollama дополнительно в отдельном терминале: `ollama serve`

## Переменные окружения (.env)

| Переменная | Значения | Описание |
|---|---|---|
| `AI_PROVIDER` | `claude` / `openai` / `gigachat` / `ollama` | Активный провайдер |
| `ANTHROPIC_API_KEY` | `sk-ant-...` | Ключ Claude |
| `OPENAI_API_KEY` | `sk-...` | Ключ OpenAI |
| `GIGACHAT_CLIENT_ID` | — | Client ID GigaChat |
| `GIGACHAT_CLIENT_SECRET` | — | Client Secret GigaChat |
| `OLLAMA_MODEL` | `llama3.2:3b` | Локальная модель |

Провайдер также переключается прямо в UI — кнопки Claude / ChatGPT / GigaChat / Local.

## Режимы генерации

| Режим | Описание |
|---|---|
| Пост | Полноценный пост в стиле канала |
| Короткий | До 80 слов |
| Идеи | 5 идей для постов по теме |
| Улучшить | Черновик / тезисы → готовый пост |

## Как добавить примеры постов

1. Положить `.docx` с постами в папку канала
2. Запустить парсер (скрипт встроен в историю сессии, вынести в `parse_posts.py`):
```python
# Логика в prompts.py: _load_examples() читает examples.json
# Перегенерировать: запустить скрипт парсинга docx → examples.json
```

## Следующие шаги

- Добавить кастомные промпты от автора (присланы будут отдельно)
- Добавить посты ТурДежурного в `Turdezhur/` → перегенерировать `examples.json`
- Добавить вкладку "Контент-план": загрузка текста/презентации → 20-30 идей постов
- Деплой на российский VPS (Timeweb/Selectel, 16 GB RAM)
- GigaChat: получить ключи на developers.sber.ru и протестировать

## Деплой на российский VPS

Те же шаги что и локально. Рекомендуемые хостинги: Timeweb, Selectel, Яндекс Облако.
Минимальные требования: 16 GB RAM, 30 GB диск, 4 CPU (для Ollama).
Для облачных провайдеров (Claude/OpenAI) — достаточно 2 GB RAM.
