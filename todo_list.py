class TodoList():
    __tasks:list[str] = []
    __completed_task_count:int = 0

    def add_task(self, task:str):
        self.__tasks.append(task)

    def remove_task_by_index(self, index:int) -> bool:
        if 0 <= index < len(self.__tasks):
            self.__tasks.pop(index)
            return True
        else:
            return False
        
    def insert_task(self, index:int, task:str) -> bool:
        if 0 <= index <= len(self.__tasks):
            self.__tasks.insert(index, task)
            return True
        elif len(self.__tasks) < index:
            self.__tasks.append(task)
            return True
        else:
            return False
        
    def clear_tasks(self):
        self.__tasks.clear()

    def complete_task(self):
        if len(self.__tasks) > 0:
            self.__completed_task_count += 1
            self.__tasks.pop(0)
        else:
            raise IndexError("No tasks to complete.")
        
    def get_current_task(self) -> str:
        if len(self.__tasks) > 0:
            return self.__tasks[0]
        else:
            raise IndexError("No tasks available.")
        
    def get_all_tasks(self) -> list[str]:
        return self.__tasks
    
    def get_ordered_list_string(self) -> str:
        ordered_list = ""
        for i, task in enumerate(self.__tasks):
            ordered_list += f"{i+1}. {task}\n"
        return ordered_list