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
    QInputDialog,
    QMessageBox,
    QSizePolicy,
    QScrollArea
)
from PySide6.QtCore import Qt, QSize
# import ./lib/client.py
from lib.client import KanbanClient


table_decode = {
    0: "To Do",
    1: "In Progress",
    2: "Done"
}
table_encode = {
    "To Do": 0,
    "In Progress": 1,
    "Done": 2
    }

server_address = os.getenv("SERVER_ADDRESS") or "http://localhost:8000" #ex; localhost:8000
# Create a client instance
client = KanbanClient(server_address)

# State of the application
k_all = client.get_all_tasks() # list of boards. boards = list of tasks






class KanbanBoard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kanban Board")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QHBoxLayout(central_widget)

        self.todo_column = KanbanColumn("To Do", self)
        self.in_progress_column = KanbanColumn("In Progress", self)
        self.done_column = KanbanColumn("Done", self)


        self.layout.addWidget(self.todo_column)
        self.layout.addWidget(self.in_progress_column)
        self.layout.addWidget(self.done_column)

        # Add example tasks
        #self.todo_column.add_task("Task 1")
        #self.todo_column.add_task("Task 2")
        #self.todo_column.add_task("Task 3")
        self.update_board()

    def update_board(self):
        # Get state of board from server
        k_all = client.get_all_tasks() # list of boards. boards = list of tasks
        # reset the board
        ## Could calculate the difference and only update the difference, but for simplicity, we will clear and re-add all tasks
        self.todo_column.task_list.clear()
        self.in_progress_column.task_list.clear()
        self.done_column.task_list.clear()
        
        for board_index in range(len(k_all)):
            board_name = table_decode[board_index]
            for task in k_all[board_index]:
                self.map_columns(board_name).task_list.add_task(task)

    def map_columns(self, table_name):
        if table_name == "To Do":
            return self.todo_column
        elif table_name == "In Progress":
            return self.in_progress_column
        else:
            return self.done_column


class KanbanColumn(QWidget):
    def __init__(self, title, board_instance, parent=None):
        super().__init__(parent)
        self.title = title
        self.board_instance = board_instance
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.task_list = ColumnListHandler(self.title, board_instance)
        self.layout.addWidget(self.task_list)

        self.create_button = QPushButton("Add")
        self.create_button.clicked.connect(self.create_task_prompt)
        self.layout.addWidget(self.create_button)

        # Add the task to the server
        #client.create_task(table_encode[self.title], task_name)
        # Update the board
        #self.board_instance.update_board()
    # Create a task
    def create_task_prompt(self):
        # Open a dialog to get the task name from the user
        task_name, ok = QInputDialog.getText(self, "Add Task", "Enter task name:")
        if ok and task_name.strip():  # Check if the user clicked OK and entered a valid name
            # Create the task in the server
            res = client.create_task(table_encode[self.title], task_name)
            if "error" in res:
                # Show an error message if the task creation failed
                QMessageBox.critical(self, "Error", res["error"])

            print(res)
            # Update the board
            self.board_instance.update_board()

class ColumnListHandler(QListWidget):
    # Shared attribute to store the source column name
    dragged_from = None

    def __init__(self, column_title, board_instance, parent=None):
        super().__init__(parent)
        self.column_title = column_title
        self.board_instance = board_instance

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QListWidget.DragDrop)
        self.setWordWrap(True)
        # prevent horizontal scrolling
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


    # visually represent the task
    def add_task(self, task_name):
        item = TaskWidget(task_name, self.column_title, self.board_instance, parent=self)
        self.addItem(item)
        self.setItemWidget(item, item.widget)

    def startDrag(self, supportedActions):
        print("Drag started")
        """Store the source column name before the drag starts."""
        ColumnListHandler.dragged_from = self.column_title
        super().startDrag(supportedActions)

    def dropEvent(self, event):
        print("Drag dropped")
        """Handle the drop event and print details."""
        super().dropEvent(event)
        if event.source():
            # Get the selected item
            item = event.source().currentItem()
            if item:
                print("B")
                task_name = item.task_name
                print("A")
                to_column = self.column_title
                self.move_task(task_name, to_column)
                print(f"Task '{task_name}' moved to '{to_column}'.")

    def move_task(self, task_name,to_column):
       # Send move instruction to the server
       # task_name, table_id of new column
       res = client.move_task(task_name, table_encode[to_column])
       print(res)
       self.board_instance.update_board()

class TaskWidget(QListWidgetItem):
    def __init__(self, task_name, column_title, board_instance, parent=None):
        super().__init__(parent)
        self.task_name = task_name
        self.column_title = column_title
        self.board_instance = board_instance
        #self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        #self.setWordWrap(True)
        self.widget = QWidget()

        label = QLabel(task_name)
        # Make the label word wrap instead of stretching the column
        label.setWordWrap(True)


        delete_button = QPushButton("X")
        delete_button.clicked.connect(self.delete_task)
        delete_button.setStyleSheet("background-color: red; border: 1px solid gray;")

        layout = QHBoxLayout()

        layout.addWidget(label)
        layout.addWidget(delete_button)

        layout.setStretchFactor(label, 4)
        layout.setStretchFactor(delete_button, 1)
        #layout.addStretch(0)
        #layout.setSizeConstraint(QVBoxLayout.SetMaximumSize)

        self.widget.setLayout(layout)
        self.setSizeHint(self.widget.sizeHint())
        
        #layout.setAlignment(Qt.AlignCenter)
        #layout.setContentsMargins(3, 3, 3, 3)
        #self.setMinimumHeight(50)
        
        #self.text = task_name
        #self.setText(self.text)
        

        #widget.setLayout(layout)
        
        # visually represent the task name

    def delete_task(self):
        # Remove the task from the server
        res = client.delete_task(self.task_name)
        print(res)
        # Update the board
        self.board_instance.update_board()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = KanbanBoard()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())
