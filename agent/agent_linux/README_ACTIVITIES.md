# Руководство по добавлению новых активностей

## Обзор архитектуры

Система использует централизованный диспетчер `execute_activity_action()` с switch case для управления различными приложениями. Каждое приложение имеет свой собственный обработчик.

## Структура обработчика

Каждый обработчик должен:
1. Принимать параметр `action_data` (словарь с данными действия)
2. Выполнять необходимые операции
3. Логировать свои действия
4. Обрабатывать ошибки

## Пример добавления нового приложения

### Шаг 1: Создать функцию-обработчик

```python
def handle_your_app(action_data):
    """Обработчик для YourApp - описание приложения"""
    try:
        # Получаем данные из action_data
        app_name = action_data.get("name", "YourApp")
        role = action_data.get("role", "user")
        
        # Ваша логика здесь
        work_dir = get_work_dir()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"your_app_file_{timestamp}.ext"
        file_path = os.path.join(work_dir, filename)
        
        # Создание файла или другие операции
        with open(file_path, 'w') as f:
            f.write("Your app content")
        
        # Запуск приложения
        cmd = ["your_app_command", file_path]
        print(f"[LOG] Открываем {app_name} с файлом: {file_path}")
        
        process = subprocess.Popen(cmd)
        time.sleep(random.randrange(5, 15))
        
        # Корректное завершение
        try:
            process.terminate()
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            print(f"[LOG] {app_name} не закрылся корректно, принудительно завершаем")
            process.kill()
            process.wait()
        
        print(f"[LOG] {app_name} закрыт, файл сохранен: {file_path}")
        
    except Exception as e:
        print(f"[ERROR] Ошибка при работе с {app_name}: {e}")
```

### Шаг 2: Добавить в switch case

В функции `execute_activity_action()` добавьте новую ветку:

```python
elif "your_app" in activity_lower or "yourapp" in activity_lower:
    handle_your_app(action_data)
```

### Шаг 3: Добавить в конфигурацию

В `agent_config.json` добавьте новую активность:

```json
{
  "id": 4,
  "name": "YourApp",
  "url": null,
  "description": "Описание вашего приложения",
  "os": "linux"
}
```

## Доступные данные в action_data

- `name`: Имя активности
- `url`: URL (если применимо)
- `role`: Роль пользователя (dev/admin/user)

## Примеры существующих обработчиков

### Firefox
- Обрабатывает веб-поиск
- Использует разные поисковые запросы в зависимости от роли
- Поддерживает различные поисковые системы

### LibreOffice Calc
- Создает CSV файлы с случайными данными
- Открывает в LibreOffice Calc
- Сохраняет файлы в рабочей директории

### LibreOffice Writer
- Создает текстовые документы с Lorem ipsum
- Открывает в LibreOffice Writer
- Сохраняет файлы в рабочей директории

### GIMP
- Создает изображения (если установлен ImageMagick)
- Открывает в GIMP
- Сохраняет файлы в рабочей директории

### Текстовый редактор
- Автоматически выбирает доступный редактор (gedit/nano/vim)
- Создает текстовые файлы с русским содержимым
- Открывает в выбранном редакторе
- Сохраняет файлы в рабочей директории

## Лучшие практики

1. **Обработка ошибок**: Всегда используйте try-except блоки
2. **Логирование**: Используйте `print(f"[LOG] ...")` для информационных сообщений
3. **Очистка ресурсов**: Корректно завершайте процессы
4. **Файловая система**: Используйте `get_work_dir()` для создания файлов
5. **Временные задержки**: Используйте `random.randrange()` для естественного поведения
6. **Параметризация**: Используйте данные из `action_data` для настройки поведения

## Расширение функциональности

Для более сложных приложений можно:
- Добавить дополнительные параметры в `action_data`
- Создать конфигурационные файлы для каждого приложения
- Реализовать плагинную архитектуру
- Добавить поддержку различных операционных систем 