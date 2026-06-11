# Content Maker — AI-копирайтер для Telegram-каналов

Локальный веб-инструмент для генерации постов и контент-планов для трёх Telegram-каналов. Работает с Claude, ChatGPT, GigaChat и локальной моделью Ollama (без VPN).

## Возможности

- **Генератор постов** — пишет посты в стиле каждого канала по теме или черновику
- **Контент-план** — загружаешь презентацию или текст, получаешь 50+ идей для постов
- **4 режима:** полный пост / короткий / 5 идей / улучшить черновик
- **4 AI-провайдера:** Claude, ChatGPT, GigaChat, Ollama — переключаются в интерфейсе
- **Авторские промпты** — написаны Ольгой Харлёнок под каждый канал

## Каналы

| Канал | Тематика |
|---|---|
| MICE Japan | MICE-туризм в Японию для корпоративных клиентов и агентств |
| MATCH POINT | MICE-индустрия: тренды, новости, площадки, направления |
| ТурДежурный | ИИ и автоматизация в туристическом бизнесе и других отраслях |

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка API-ключей

Создай файл `.env` в корне проекта:

```env
AI_PROVIDER=claude

ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GIGACHAT_CLIENT_ID=
GIGACHAT_CLIENT_SECRET=
OLLAMA_MODEL=llama3.2:3b
```

### 3. Запуск

```bash
python app.py
```

Открыть в браузере: [http://localhost:5000](http://localhost:5000)

## Где взять API-ключи

| Провайдер | Ссылка | VPN в России |
|---|---|---|
| Claude | [console.anthropic.com](https://console.anthropic.com/settings/keys) | Нужен |
| ChatGPT | [platform.openai.com](https://platform.openai.com/api-keys) | Нужен |
| GigaChat | [developers.sber.ru](https://developers.sber.ru/gigachat) | Не нужен |
| Ollama | Локально, ключи не нужны | Не нужен |

## Ollama (локальная модель, без интернета)

```bash
# Установить: https://ollama.com
ollama pull llama3.2:3b
ollama serve
```

Затем в `.env` поставить `AI_PROVIDER=ollama` или переключить в интерфейсе.

## Структура проекта

```
app.py              — Flask-сервер
prompts.py          — промпты каналов и контент-плана
examples.json       — реальные посты каналов (few-shot примеры)
templates/
  index.html        — интерфейс
Match Point/        — посты канала MATCH POINT (.docx)
MICE Japan/         — посты канала MICE Japan (.docx)
Turdezhur/          — посты канала ТурДежурный (.docx)
.env                — API ключи (не в git)
requirements.txt    — зависимости
```

## Контент-план

Во вкладке **Контент-план**:

1. Выбери канал (или все три сразу)
2. Загрузи файл (PPTX, PDF, DOCX) или вставь текст вручную
3. Опционально — вставь свой промпт в поле «Свои инструкции»
4. Нажми «Создать контент-план»

Получишь 50+ пронумерованных идей с описанием каждой.

## Требования

- Python 3.10+
- 2 GB RAM (для облачных провайдеров)
- 16 GB RAM (для Ollama с моделью llama3.2)
