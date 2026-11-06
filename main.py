import customtkinter as ctk
from logic import TaskManager
from datetime import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Дедлайн-менеджер (Матрица Эйзенхауэра)")
        self.geometry("900x600")
        
        self.manager = TaskManager()

        # Панель добавления задачи
        self.frame_top = ctk.CTkFrame(self)
        self.frame_top.pack(pady=10, padx=10, fill="x")

        self.entry_title = ctk.CTkEntry(self.frame_top, placeholder_text="Название задачи", width=200)
        self.entry_title.pack(side="left", padx=5)

        self.entry_deadline = ctk.CTkEntry(self.frame_top, placeholder_text="Дедлайн (ГГГГ-ММ-ДД ЧЧ:ММ)", width=200)
        self.entry_deadline.pack(side="left", padx=5)

        self.check_important = ctk.CTkCheckBox(self.frame_top, text="Важно")
        self.check_important.pack(side="left", padx=5)

        self.btn_add = ctk.CTkButton(self.frame_top, text="Добавить", command=self.add_task)
        self.btn_add.pack(side="left", padx=5)

        self.label_msg = ctk.CTkLabel(self, text="", text_color="red")
        self.label_msg.pack()

        # Вкладки (4 квадранта)
        self.tabview = ctk.CTkTabview(self, width=850, height=450)
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.tabs = {
            "1. Срочно и Важно": self.tabview.add("1. Срочно и Важно"),
            "2. Важно и Не срочно": self.tabview.add("2. Важно и Не срочно"),
            "3. Срочно и Не важно": self.tabview.add("3. Срочно и Не важно"),
            "4. Не срочно и Не важно": self.tabview.add("4. Не срочно и Не важно")
        }

        self.update_ui()

    def add_task(self):
        title = self.entry_title.get()
        deadline = self.entry_deadline.get()
        is_important = bool(self.check_important.get())

        if not title:
            self.label_msg.configure(text="Введите название задачи!", text_color="red")
            return

        success, msg = self.manager.add_task(title, deadline, is_important)
        if success:
            self.label_msg.configure(text="Задача добавлена!", text_color="green")
            self.entry_title.delete(0, 'end')
            self.entry_deadline.delete(0, 'end')
            self.check_important.deselect()
            self.update_ui()
        else:
            self.label_msg.configure(text=msg, text_color="red")

    def update_ui(self):
        # Очищаем вкладки
        for tab in self.tabs.values():
            for widget in tab.winfo_children():
                widget.destroy()

        # Распределяем задачи
        for task in self.manager.tasks:
            quadrant_name = self.manager.get_quadrant(task)
            text = f"• {task['title']} (до {task['deadline'][:16]})"
            lbl = ctk.CTkLabel(self.tabs[quadrant_name], text=text, anchor="w", justify="left", font=("Arial", 14))
            lbl.pack(fill="x", pady=5, padx=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()