# Importa el módulo csv, que se utiliza para trabajar con archivos CSV (Comma Separated Values).
import csv

# Importa el módulo os, que proporciona funciones para interactuar con el sistema operativo.
import os

# Define la clase Task que se utiliza para representar tareas que pueden estar completas o incompletas.
class Task:
    
    def __init__(self, title, task_id=None, completed=False):
        # Asigna el valor de task_id al atributo id del objeto (si no se pasa, será None).
        self.id = task_id
        
        # Asigna el valor de title al atributo title del objeto.
        self.title = title
        
        # Asigna el valor de completed al atributo completed del objeto.
        self.completed = completed

    # Método para marcar la tarea como completada.
    def mark_complete(self):
        self.completed = True

    # Método para desmarcar la tarea como completada.
    def unmark_complete(self):
        self.completed = False

    # Método especial __repr__ que se utiliza para representar un objeto de la clase Task en forma de cadena de texto.
    def __repr__(self):
        return f"Task({self.id}, '{self.title}', {self.completed})"

# Define la clase Subtask. Esta clase representa una sub-tarea, que está asociada a una tarea principal.
class Subtask:
    
    def __init__(self, title, task_id, subtask_id=None, completed=False):
        # Asigna el valor de subtask_id al atributo id del objeto (si no se pasa, será None).
        self.id = subtask_id
        
        # Asigna el valor de task_id al atributo task_id del objeto (es la tarea principal a la que pertenece esta sub-tarea).
        self.task_id = task_id
        
        # Asigna el valor de title al atributo title del objeto (es el título de la sub-tarea).
        self.title = title
        
        # Asigna el valor de completed al atributo completed del objeto (indica si la sub-tarea está completada o no).
        self.completed = completed

    # Método para marcar la sub-tarea como completada.
    def mark_complete(self):
        self.completed = True

    # Método para desmarcar la sub-tarea como completada.
    def unmark_complete(self):
        self.completed = False

    # Método especial __repr__ que se utiliza para representar el objeto de la clase Subtask en forma de cadena de texto.
    def __repr__(self):
        return f"Subtask({self.id}, '{self.title}', {self.completed})"

# Define la clase TaskManager. Esta clase es responsable de gestionar las tareas y sub-tareas.
class TaskManager:

    def __init__(self, task_file='tasks.csv', subtask_file='subtasks.csv'):
        # Asigna el nombre del archivo CSV para tareas al atributo task_file del objeto.
        self.task_file = task_file
        
        # Asigna el nombre del archivo CSV para sub-tareas al atributo subtask_file del objeto.
        self.subtask_file = subtask_file
        
        # Inicializa la lista de tareas como una lista vacía.
        self.tasks = []
        
        # Inicializa la lista de sub-tareas como una lista vacía.
        self.subtasks = []
        
        # Llama al método load_tasks_from_csv() para cargar las tareas desde el archivo CSV.
        self.load_tasks_from_csv()
        
        # Llama al método load_subtasks_from_csv() para cargar las sub-tareas desde el archivo CSV.
        self.load_subtasks_from_csv()

    # Define el método add_task que agrega una nueva tarea al sistema.
    def add_task(self, title):
        # Calcula el id de la nueva tarea.
        task_id = len(self.tasks) + 1 if not self.tasks else self.tasks[-1].id + 1
        
        # Crea un nuevo objeto de tipo Task con el título recibido y el id calculado.
        task = Task(title, task_id)
        
        # Agrega la nueva tarea a la lista de tareas (self.tasks).
        self.tasks.append(task)
        
        # Llama al método save_tasks_to_csv() para guardar las tareas actuales en el archivo CSV.
        self.save_tasks_to_csv()

    # Define el método add_subtask que agrega una nueva sub-tarea a una tarea principal específica.
    def add_subtask(self, task_id, title):
        # Calcula el id de la nueva sub-tarea.
        subtask_id = len(self.subtasks) + 1 if not self.subtasks else self.subtasks[-1].id + 1
        
        # Crea un nuevo objeto de la clase Subtask utilizando el título recibido (title),
        # el id de la tarea principal (task_id), y el subtask_id calculado.
        subtask = Subtask(title, task_id, subtask_id)
        
        # Agrega la nueva sub-tarea a la lista de sub-tareas (self.subtasks).
        self.subtasks.append(subtask)
        
        # Llama al método save_subtasks_to_csv() para guardar las sub-tareas actuales en el archivo CSV.
        self.save_subtasks_to_csv()

    # Define el método mark_task_complete que marca una tarea como completada.
    def mark_task_complete(self, task_id):
        # Llama al método get_task() para obtener la tarea correspondiente al task_id proporcionado.
        task = self.get_task(task_id)
        
        # Verifica si la tarea existe.
        if task:
            # Si la tarea fue encontrada, se llama al método mark_complete() de la tarea para marcarla como completada.
            task.mark_complete()
            
            # Después de marcar la tarea como completada, se guarda el estado actualizado de las tareas en el archivo CSV.
            self.save_tasks_to_csv()

    # Define el método unmark_task_complete que desmarca una tarea como incompleta.
    def unmark_task_complete(self, task_id):
        # Llama al método get_task() para obtener la tarea correspondiente al task_id proporcionado.
        task = self.get_task(task_id)
        
        # Verifica si la tarea existe.
        if task:
            # Si la tarea fue encontrada, se llama al método unmark_complete() de la tarea para desmarcarla como completada.
            task.unmark_complete()
            
            # Después de desmarcar la tarea como incompleta, se guarda el estado actualizado de las tareas en el archivo CSV.
            self.save_tasks_to_csv()

    # Define el método mark_subtask_complete que marca una sub-tarea como completada.
    def mark_subtask_complete(self, subtask_id):
        # Llama al método get_subtask() para obtener la sub-tarea correspondiente al subtask_id proporcionado.
        subtask = self.get_subtask(subtask_id)
        
        # Verifica si la sub-tarea existe.
        if subtask:
            # Si la sub-tarea fue encontrada, se llama al método mark_complete() de la sub-tarea para marcarla como completada.
            subtask.mark_complete()
            
            # Después de marcar la sub-tarea como completada, se guarda el estado actualizado de las sub-tareas en el archivo CSV.
            self.save_subtasks_to_csv()

    # Define el método unmark_subtask_complete que desmarca una sub-tarea como incompleta.
    def unmark_subtask_complete(self, subtask_id):
        # Llama al método get_subtask() para obtener la sub-tarea correspondiente al subtask_id proporcionado.
        subtask = self.get_subtask(subtask_id)
        
        # Verifica si la sub-tarea existe (si subtask no es None).
        if subtask:
            # Si la sub-tarea fue encontrada, se llama al método unmark_complete() de la sub-tarea para desmarcarla como completada.
            subtask.unmark_complete()
            
            # Después de desmarcar la sub-tarea como incompleta, se guarda el estado actualizado de las sub-tareas en el archivo CSV.
            self.save_subtasks_to_csv()

    # Define el método delete_task que elimina una tarea y todas las subtareas asociadas a ella.
    def delete_task(self, task_id):
        # Llama al método get_task() para obtener la tarea correspondiente al task_id proporcionado.
        task = self.get_task(task_id)
        
        # Verifica si la tarea existe.
        if task:
            # Si la tarea fue encontrada, se elimina de la lista de tareas (self.tasks).
            self.tasks.remove(task)

            # Elimina todas las subtareas que están asociadas a esta tarea eliminada.
            self.subtasks = [subtask for subtask in self.subtasks if subtask.task_id != task_id]

            # Después de eliminar la tarea y sus subtareas, se guarda el estado actualizado de las tareas en el archivo CSV.
            self.save_tasks_to_csv()

            # También guarda el estado actualizado de las subtareas en el archivo CSV.
            self.save_subtasks_to_csv()

    # Define el método delete_subtask que elimina una sub-tarea.
    def delete_subtask(self, subtask_id):
        # Llama al método get_subtask() para obtener la sub-tarea correspondiente al subtask_id proporcionado.
        subtask = self.get_subtask(subtask_id)
        
        # Verifica si la sub-tarea existe.
        if subtask:
            # Si la sub-tarea fue encontrada, se elimina de la lista de sub-tareas (self.subtasks).
            self.subtasks.remove(subtask)
            
            # Después de eliminar la sub-tarea, se guarda el estado actualizado de las sub-tareas en el archivo CSV.
            self.save_subtasks_to_csv()

    # Define el método get_task que busca una tarea por su identificador (task_id).
    def get_task(self, task_id):
        # Utiliza una expresión generadora para buscar la tarea que tenga el id igual al task_id.
        return next((task for task in self.tasks if task.id == task_id), None)

    # Define el método get_subtask que busca una sub-tarea por su identificador (subtask_id).

    def get_subtask(self, subtask_id):
        # Utiliza una expresión generadora para buscar la sub-tarea que tenga el id igual al subtask_id.
        return next((subtask for subtask in self.subtasks if subtask.id == subtask_id), None)

    # Define el método load_tasks_from_csv que carga las tareas desde el archivo CSV.
    def load_tasks_from_csv(self):
        # Verifica si el archivo de tareas (self.task_file) no existe en el sistema.
        # Si el archivo no existe, lo crea y escribe la cabecera (header) en él.
        if not os.path.exists(self.task_file):
            # Abre el archivo en modo escritura (modo 'w').
            with open(self.task_file, mode='w') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "title", "completed"])  # Escribe la cabecera del archivo CSV

        # Abre el archivo en modo lectura (modo 'r') para leer los datos existentes.
        with open(self.task_file, mode='r') as file:
            reader = csv.reader(file)
            # Convierte el objeto 'reader' a una lista de filas (rows).
            # Cada fila en 'rows' es una lista que representa una línea en el archivo CSV.
            rows = list(reader)

            # Inicializa una lista vacía para almacenar las tareas cargadas desde el archivo CSV.
            self.tasks = []
            
            # Itera sobre todas las filas del archivo CSV, comenzando desde la segunda fila (rows[1:]),
            # para ignorar la cabecera (que está en la primera fila).
            for row in rows[1:]:
                # Verifica si la fila tiene exactamente 3 columnas: id, title, completed.
                if len(row) == 3:
                    try:
                        # Desempaqueta la fila en 3 variables: task_id, title, completed.
                        task_id, title, completed = row
                        
                        # Convierte el task_id a entero.
                        task_id = int(task_id)
                        
                        # Convierte el valor de completed a un valor booleano.
                        completed = completed == 'True'
                        
                        # Crea un objeto Task con el título, id y estado de completado, y lo agrega a la lista de tareas.
                        self.tasks.append(Task(title, task_id, completed))
                    except ValueError:
                        # Si ocurre un error al convertir task_id o completed, se ignora esa fila y se continúa con la siguiente.
                        continue

    # Define el método load_subtasks_from_csv que carga las sub-tareas desde el archivo CSV.
    def load_subtasks_from_csv(self):  
        # Verifica si el archivo de subtareas (self.subtask_file) no existe en el sistema.
        # Si el archivo no existe, lo crea y escribe la cabecera (header) en él.
        if not os.path.exists(self.subtask_file):
            # Abre el archivo en modo escritura (modo 'w').
            with open(self.subtask_file, mode='w') as file:
                writer = csv.writer(file)
                writer.writerow(["id", "task_id", "title", "completed"])  # Escribe la cabecera del archivo CSV

        # Abre el archivo en modo lectura (modo 'r') para leer los datos existentes.
        with open(self.subtask_file, mode='r') as file:
            reader = csv.reader(file)
            # Convierte el objeto 'reader' a una lista de filas (rows).
            # Cada fila en 'rows' es una lista que representa una línea en el archivo CSV.
            rows = list(reader)

            # Inicializa una lista vacía para almacenar las subtareas cargadas desde el archivo CSV.
            self.subtasks = []
            
            # Itera sobre todas las filas del archivo CSV, comenzando desde la segunda fila (rows[1:]),
            # para ignorar la cabecera (que está en la primera fila).
            for row in rows[1:]:
                # Verifica si la fila tiene exactamente 4 columnas: id, task_id, title, completed.
                if len(row) == 4:
                    try:
                        # Desempaqueta la fila en 4 variables: subtask_id, task_id, title, completed.
                        subtask_id, task_id, title, completed = row
                        
                        # Convierte el subtask_id y task_id a enteros.
                        subtask_id = int(subtask_id)
                        task_id = int(task_id)
                        
                        # Convierte el valor de completed a un valor booleano.
                        completed = completed == 'True'
                        
                        # Crea un objeto Subtask con el título, task_id, subtask_id y estado de completado, y lo agrega a la lista de subtareas.
                        self.subtasks.append(Subtask(title, task_id, subtask_id, completed))
                    except ValueError:
                        # Si ocurre un error al convertir subtask_id, task_id o completed se ignora esa fila y se continúa con la siguiente.
                        continue

    # Define el método save_tasks_to_csv que guarda las tareas en el archivo CSV.
    def save_tasks_to_csv(self):
        # Abre el archivo de tareas (self.task_file) en modo escritura ('w').
        with open(self.task_file, mode='w', newline='') as file:
            # Crea un objeto escritor CSV que se utilizará para escribir en el archivo.
            writer = csv.writer(file)
            # Escribe la cabecera en el archivo CSV, indicando los nombres de las columnas.
            writer.writerow(["id", "title", "completed"])  # Cabecera

            # Itera sobre todas las tareas en la lista self.tasks.
            for task in self.tasks:
                # Escribe una fila en el archivo CSV para cada tarea.
                writer.writerow([task.id, task.title, task.completed])

    # Define el método save_subtasks_to_csv que guarda las subtareas en el archivo CSV.
    def save_subtasks_to_csv(self):
        """Guardar las subtareas en el archivo CSV"""
        
        # Abre el archivo de subtareas (self.subtask_file) en modo escritura ('w').
        with open(self.subtask_file, mode='w', newline='') as file:
            # Crea un objeto escritor CSV que se utilizará para escribir en el archivo.
            writer = csv.writer(file)
            # Escribe la cabecera en el archivo CSV, indicando los nombres de las columnas.
            writer.writerow(["id", "task_id", "title", "completed"])  # Cabecera

            # Itera sobre todas las subtareas en la lista self.subtasks.
            for subtask in self.subtasks:
                # Escribe una fila en el archivo CSV para cada sub-tarea.
                writer.writerow([subtask.id, subtask.task_id, subtask.title, subtask.completed])

# Exporta las funciones para interactuar con las tareas.
task_manager = TaskManager()

# Define la función add_task que agrega una tarea.
def add_task(title):
    task_manager.add_task(title)

# Define la función add_subtask que agrega una subtarea a una tarea específica.
def add_subtask(task_id, title):
    task_manager.add_subtask(task_id, title) 

# Define la función mark_task_complete que marca una tarea como completada.
def mark_task_complete(task_id):
    task_manager.mark_task_complete(task_id) 

# Define la función unmark_task_complete que desmarca una tarea como no completada.
def unmark_task_complete(task_id):
    task_manager.unmark_task_complete(task_id) 

# Define la función mark_subtask_complete que marca una subtarea como completada.
def mark_subtask_complete(subtask_id):
    task_manager.mark_subtask_complete(subtask_id)

# Define la función unmark_subtask_complete que desmarca una subtarea como no completada.
def unmark_subtask_complete(subtask_id):
    task_manager.unmark_subtask_complete(subtask_id)

# Define la función delete_task que elimina una tarea.
def delete_task(task_id):
    task_manager.delete_task(task_id)

# Define la función delete_subtask que elimina una subtarea.
def delete_subtask(subtask_id):
    task_manager.delete_subtask(subtask_id)

# Define la función list_tasks que devuelve la lista de tareas almacenadas en el objeto 'task_manager'.
def list_tasks():
    return task_manager.tasks 

# Define la función list_subtasks que devuelve la lista de subtareas almacenadas en el objeto 'task_manager'.
def list_subtasks():
    return task_manager.subtasks 
