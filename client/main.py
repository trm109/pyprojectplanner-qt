import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt


tablemap = {
    0: "To Do",
    1: "In Progress",
    2: "Done"
}
server_address = os.getenv("SERVER_ADDRESS") or "localhost:8000" #ex; localhost:8000


class KanbanColumn(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.task_list = CustomListWidget(self.title)
        self.layout.addWidget(self.task_list)

    def add_task(self, task_name):
        item = QListWidgetItem(task_name)
        self.task_list.addItem(item)


class CustomListWidget(QListWidget):
    # Shared attribute to store the source column name
    dragged_from = None

    def __init__(self, column_title, parent=None):
        super().__init__(parent)
        self.column_title = column_title

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QListWidget.DragDrop)

    def startDrag(self, supportedActions):
        """Store the source column name before the drag starts."""
        CustomListWidget.dragged_from = self.column_title
        super().startDrag(supportedActions)

    def dropEvent(self, event):
        """Handle the drop event and print details."""
        super().dropEvent(event)
        if event.source():
            # Get the selected item
            item = event.source().currentItem()
            if item:
                task_name = item.text()
                from_column = CustomListWidget.dragged_from
                to_column = self.column_title
                res = requests.put()
                print(f"Task '{task_name}' moved from '{from_column}' to '{to_column}'.")


class KanbanBoard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.setWindowTitle("Kanban Board")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QHBoxLayout(central_widget)

        # backend server addres
        self.backend_server_address = backendServerAddress()

        self.todo_column = KanbanColumn("To Do")
        self.in_progress_column = KanbanColumn("In Progress")
        self.done_column = KanbanColumn("Done")


        self.layout.addWidget(self.todo_column)
        self.layout.addWidget(self.in_progress_column)
        self.layout.addWidget(self.done_column)

        # Add example tasks
        self.todo_column.add_task("Task 1")
        self.todo_column.add_task("Task 2")
        self.todo_column.add_task("Task 3")
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = KanbanBoard()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
