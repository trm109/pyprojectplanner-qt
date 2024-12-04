import requests

class KanbanClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_all_tasks(self):
        response = requests.get(f"{self.base_url}/all")
        return response.json()

    def create_task(self, table_id, task_name):
        response = requests.post(f"{self.base_url}/task/create", json={"table_id": table_id, "task_name": task_name})
        return response.json()
    
    def edit_task(self, old_task_name, new_task_name):
        response = requests.put(f"{self.base_url}/task/edit", json={"old_task_name": old_task_name, "new_task_name": new_task_name})
        return response.json()
    
    def delete_task(self, task_name):
        response = requests.delete(f"{self.base_url}/task/delete", json={"task_name": task_name})
        return response.json()

    def move_task(self, task_name, table_id):
        response = requests.put(f"{self.base_url}/task/move", json={"task_name": task_name, "table_to": table_id})
        return response.json()
