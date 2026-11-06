import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            # Если файл поврежден, возвращаем пустой список (защита от сбоя)
            return []

    def save_tasks(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def add_task(self, title, deadline_str, is_important):
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return False, "Неверный формат даты (нужно ГГГГ-ММ-ДД ЧЧ:ММ)"

        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "deadline": deadline.isoformat(),
            "is_important": is_important
        }
        self.tasks.append(task)
        self.save_tasks()
        return True, "Задача добавлена"

    def get_quadrant(self, task):
        deadline = datetime.fromisoformat(task["deadline"])
        now = datetime.now()
        time_diff = (deadline - now).total_seconds() / 3600 # часы до дедлайна
        
        is_urgent = time_diff < 24 # Срочно, если меньше суток
        is_important = task["is_important"]

        if is_urgent and is_important:
            return "1. Срочно и Важно"
        elif not is_urgent and is_important:
            return "2. Важно и Не срочно"
        elif is_urgent and not is_important:
            return "3. Срочно и Не важно"
        else:
            return "4. Не срочно и Не важно"