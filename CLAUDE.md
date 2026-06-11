# Content Maker Agent

Веб-приложение для генерации постов в Telegram-каналы. Поддерживает несколько AI-провайдеров — работает как с облачными API (Claude, ChatGPT), так и локально (Ollama) без интернета и VPN.

## Каналы

| ID | Название | Тематика |
|---|---|---|
| `mice_japan` | MICE Japan | MICE-туризм в Японию: отели, гастрономия, культура, логистика групп |
| `match_point` | MATCH POINT | MICE в России и мире: тренды, новости рынка, обзоры площадок и отелей |
| `turdezhur` | ТурДежурный | ИИ в бизнесе и автоматизация для туризма и других отраслей |

Автор всех каналов — Ольга Харлёнок. Промпты написаны самим автором и интегрированы в `prompts.py`.

## Стек

- **Backend:** Python / Flask
- **AI-провайдеры:** Claude (Anthropic), OpenAI (GPT-4o-mini), GigaChat (Сбер), Ollama (локально)
- **Frontend:** Vanilla HTML/CSS/JS, тёмная тема
- **Промпты:** `prompts.py` — авторские system prompts + few-shot примеры из `examples.json`

## Структура файлов

```
app.py              — Flask-сервер: /generate, /content_plan, /set_provider, /health
prompts.py          — авторские промпты каналов + CONTENT_PLAN_SYSTEM + CONTENT_PLAN_CHANNEL_CONTEXT
examples.json       — реальные посты каналов (few-shot), парсится из docx
.env                — API ключи и выбор провайдера (не в git)
templates/
  index.html        — весь фронтенд (2 вкладки: Генератор + Контент-план)
Match Point/
  posts Match Point.docx   — исходные посты канала
MICE Japan/
  Posts Mice Japan.docx    — исходные посты канала
Turdezhur/
  Posts.docx               — исходные посты канала
START.md            — инструкция по установке и запуску
requirements.txt    — flask, requests, anthropic, openai, python-pptx, pypdf2
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

Провайдер переключается прямо в UI — кнопки Claude / ChatGPT / GigaChat / Local.

## Режимы генерации (вкладка Генератор)

| Режим | Описание |
|---|---|
| Пост | Полноценный пост в стиле канала |
| Короткий | До 80 слов |
| Идеи | 5 идей для постов по теме |
| Улучшить | Черновик / тезисы → готовый пост |

## Контент-план (вкладка Контент-план)

Загрузка материала → 50+ идей для постов.

- **Форматы файлов:** PPTX, PDF, DOCX
- **Или:** текст вручную в поле
- **Канал:** один из трёх или все сразу (тогда у каждой идеи указан канал)
- **Свои инструкции:** необязательное поле — если заполнено, заменяет стандартный промпт

Endpoint: `POST /content_plan` (multipart/form-data: file, text, channel, system_prompt)

## Промпты

Все промпты написаны Ольгой Харлёнок и хранятся в `prompts.py`:
- `CHANNELS[id]["system_prompt"]` — авторский промпт каждого канала
- `CONTENT_PLAN_SYSTEM` — промпт для генерации контент-плана (50+ идей)
- `CONTENT_PLAN_CHANNEL_CONTEXT` — контекст канала для контент-плана

Few-shot примеры: `examples.json` (MICE Japan: 15 постов, MATCH POINT: 13, ТурДежурный: 8).
Примеры обрезаются до 900 символов, 1 пример на канал.

## Как добавить примеры постов

1. Положить `.docx` с постами в папку канала
2. Запустить в терминале:
```python
python -c "
import zipfile, json, os
from xml.etree import ElementTree as ET

def parse_docx(path):
    ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml')
    root = ET.fromstring(xml)
    paragraphs = []
    for p in root.iter(ns + 'p'):
        text = ''.join(r.text or '' for r in p.iter(ns + 't')).strip()
        paragraphs.append(text)
    posts, current = [], []
    for para in paragraphs:
        if para: current.append(para)
        else:
            if current: posts.append('\n'.join(current)); current = []
    if current: posts.append('\n'.join(current))
    return posts

with open('examples.json', 'r', encoding='utf-8') as f:
    examples = json.load(f)
examples['turdezhur'] = parse_docx('Turdezhur/Posts.docx')
with open('examples.json', 'w', encoding='utf-8') as f:
    json.dump(examples, f, ensure_ascii=False, indent=2)
"
```

## Следующие шаги

- GigaChat: получить ключи на developers.sber.ru и протестировать
- Деплой на российский VPS (Timeweb/Selectel)
- Отдельный проект: парсер новостей по темам и конкурентам

## Деплой на российский VPS

Те же шаги что и локально. Рекомендуемые хостинги: Timeweb, Selectel, Яндекс Облако.
Для облачных провайдеров (Claude/OpenAI) — достаточно 2 GB RAM.
Для Ollama — минимум 16 GB RAM, 30 GB диск, 4 CPU.
