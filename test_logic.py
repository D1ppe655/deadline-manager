import pytest
from logic import TaskManager
from datetime import datetime, timedelta

@pytest.fixture
def manager(tmp_path, monkeypatch):
    # Подменяем файл данных на временный
    monkeypatch.setattr("logic.DATA_FILE", str(tmp_path / "tasks.json"))
    return TaskManager()

def test_quadrant_1_urgent_important(manager):
    # Дедлайн через 2 часа, Важно
    deadline = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
    manager.add_task("Task 1", deadline, True)
    assert manager.get_quadrant(manager.tasks[0]) == "1. Срочно и Важно"

def test_quadrant_2_not_urgent_important(manager):
    # Дедлайн через 3 дня, Важно
    deadline = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M")
    manager.add_task("Task 2", deadline, True)
    assert manager.get_quadrant(manager.tasks[0]) == "2. Важно и Не срочно"

def test_quadrant_3_urgent_not_important(manager):
    # Дедлайн через 2 часа, Не важно
    deadline = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
    manager.add_task("Task 3", deadline, False)
    assert manager.get_quadrant(manager.tasks[0]) == "3. Срочно и Не важно"

def test_quadrant_4_not_urgent_not_important(manager):
    # Дедлайн через 3 дня, Не важно
    deadline = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M")
    manager.add_task("Task 4", deadline, False)
    assert manager.get_quadrant(manager.tasks[0]) == "4. Не срочно и Не важно"