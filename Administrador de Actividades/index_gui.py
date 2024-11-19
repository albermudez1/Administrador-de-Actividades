# Importa el módulo tkinter para crear interfaces gráficas de usuario (GUI) en Python.
import tkinter as tk

# Importa el módulo messagebox de tkinter para mostrar cuadros de mensajes emergentes.
from tkinter import messagebox

# Importa el módulo simpledialog de tkinter para mostrar cuadros de diálogo simples que permiten ingresar texto de manera rápida .
from tkinter import simpledialog

# Importa el widget Checkbutton de tkinter. Este widget permite crear casillas de verificación
from tkinter import Checkbutton

# Importa funciones y clases definidas en el archivo 'index.py' que gestionan las tareas y subtareas.
from index import (
    Task,                          # La clase Task que representa una tarea individual.
    TaskManager,                   # La clase TaskManager que gestiona la lista de tareas y subtareas.
    add_task,                      # Función para agregar una nueva tarea.
    add_subtask,                   # Función para agregar una subtarea a una tarea específica.
    mark_task_complete,            # Función para marcar una tarea como completada.
    unmark_task_complete,          # Función para desmarcar una tarea como no completada.
    delete_task,                   # Función para eliminar una tarea.
    list_tasks,                    # Función para listar todas las tareas.
    list_subtasks,                 # Función para listar todas las subtareas.
    mark_subtask_complete,         # Función para marcar una subtarea como completada.
    unmark_subtask_complete,       # Función para desmarcar una subtarea como no completada.
    delete_subtask                 # Función para eliminar una subtarea.
)


# Definición de la clase TaskApp, que es la aplicación de gestión de tareas.
class TaskApp:

    def __init__(self, root):
        self.root = root  # Guarda el objeto 'root' (la ventana principal) como un atributo de la clase.
        self.root.title("Administrador de Actividades")  # Establece el título de la ventana principal.

        # Crea una instancia de TaskManager, que gestiona las tareas y subtareas.
        self.task_manager = TaskManager()

        # Crea un frame (un contenedor) dentro de la ventana principal donde se mostrarán las tareas.
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(pady=10)  # Empaqueta el frame y añade un margen de 10 píxeles en la dirección vertical (pady).

        # Crea un botón que, cuando se presiona, agrega una nueva tarea.
        self.add_button = tk.Button(self.root, text="Agregar Actividad", width=20, command=self.add_task)
        self.add_button.pack(pady=5)  # Empaqueta el botón en la ventana y añade un margen vertical de 5 píxeles (pady).

        # Llama al método 'refresh_task_list' para mostrar las tareas actuales en la interfaz gráfica.
        self.refresh_task_list()

    # Método que actualiza la lista de tareas en la interfaz gráfica.
    # Este método genera dinámicamente los Checkbuttons (casillas de verificación) y botones de borrar
    # para cada tarea en la lista de tareas, mostrando su estado (completada o pendiente) y permitiendo
    # agregar subtareas o borrar tareas.
    def refresh_task_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()  # Elimina cada widget de la interfaz (tareas y botones anteriores)

        task_row = 0  # Inicializamos un contador de filas para organizar las tareas y sus elementos en la interfaz.

        # Iteramos sobre todas las tareas obtenidas de la función 'list_tasks()'.
        # Esta función devuelve la lista de todas las tareas almacenadas en 'TaskManager'.
        for task in list_tasks():
            # Determina el estado de la tarea.
            task_status = "Completada" if task.completed else "Pendiente"
            
            # Creamos una variable de tipo BooleanVar que guardará el estado de la tarea (completada o pendiente).
            var = tk.BooleanVar(value=task.completed)

            # Creamos un Checkbutton para cada tarea. El texto del Checkbutton muestra el título de la tarea
            check = Checkbutton(self.task_frame, text=f"{task.title} - {task_status}",
                                variable=var, onvalue=True, offvalue=False, 
                                command=lambda t=task, v=var: self.toggle_task(t, v))

            # Usamos grid para colocar el Checkbutton en la interfaz gráfica. La tarea actual se coloca en la fila 
            # 'task_row' y en la primera columna. 'sticky="w"' alinea el texto a la izquierda, 'padx' y 'pady'
            # controlan los márgenes.
            check.grid(row=task_row, column=0, sticky="w", padx=10, pady=5)

            # Creamos un botón para eliminar la tarea.
            delete_button = tk.Button(self.task_frame, text="Borrar", width=10, 
                                    command=lambda t=task: self.delete_task(t))
            
            # Colocamos el botón de borrar en la interfaz en la misma fila de la tarea actual, en la segunda columna.
            delete_button.grid(row=task_row, column=1, padx=5, pady=5)

            # Creamos un botón para agregar una subtarea a la tarea actual.
            add_subtask_button = tk.Button(self.task_frame, text="Agregar Subactividad", width=20,
                                        command=lambda t=task: self.add_subtask(t))  # Pasamos la tarea actual al comando
            
            # Colocamos el botón para agregar subtareas en la misma fila de la tarea, en la tercera columna.
            add_subtask_button.grid(row=task_row, column=2, padx=5, pady=5)

            # Llamamos al método 'refresh_subtasks_for_task' para mostrar las subtareas asociadas con la tarea actual.
            # Este método generará los widgets correspondientes para cada subtarea y los colocará en la interfaz.
            # 'task_row' se pasa como argumento para que las subtareas se coloquen justo debajo de la tarea.
            subtask_row = self.refresh_subtasks_for_task(task, task_row)

            # Incrementamos el contador 'task_row' con el valor de 'subtask_row'.
            # Esto asegura que la siguiente tarea o conjunto de subtareas se coloque en una fila nueva
            # de la interfaz gráfica, debajo de las subtareas de la tarea anterior.
            task_row = subtask_row 

    # Método que actualiza la lista de subtareas debajo de una tarea principal.
    def refresh_subtasks_for_task(self, task, task_row):
        """Actualizar las subtareas debajo de la tarea principal, manteniendo la relación de jerarquía"""

        # Inicializamos la fila donde se mostrarán las subtareas. 
        # Esto asegura que las subtareas se muestren justo debajo de la tarea principal en la interfaz.
        subtask_row = task_row + 1 

        # Iteramos sobre todas las subtareas obtenidas mediante la función 'list_subtasks()'.
        for subtask in list_subtasks():
            # Comprobamos si la subtarea está asociada a la tarea actual (la tarea principal).
            if subtask.task_id == task.id:

                # Determinamos el estado de la subtarea.
                subtask_status = "Completada" if subtask.completed else "Pendiente"
                
                # Creamos una variable booleana para representar el estado de la subtarea en la interfaz.
                var = tk.BooleanVar(value=subtask.completed)

                # Creamos un Checkbutton para mostrar la subtarea en la interfaz gráfica.
                check_subtask = Checkbutton(self.task_frame, text=f"  {subtask.title} - {subtask_status}",
                                            variable=var, onvalue=True, offvalue=False,
                                            command=lambda s=subtask, v=var: self.toggle_subtask(s, v))

                # Colocamos el Checkbutton en la interfaz gráfica utilizando el método 'grid'.
                # Las subtareas se colocan en la fila 'subtask_row' y la primera columna.
                # El texto se alineará a la izquierda con 'sticky="w"', y 'padx' y 'pady' agregan márgenes.
                check_subtask.grid(row=subtask_row, column=0, sticky="w", padx=20, pady=5)

                # Creamos un botón para eliminar la subtarea.
                delete_subtask_button = tk.Button(self.task_frame, text="Borrar", width=10,
                                                command=lambda s=subtask: self.delete_subtask(s))
                
                # Colocamos el botón de eliminar subtarea en la interfaz gráfica utilizando 'grid'.
                # Se coloca en la misma fila de la subtarea, pero en la segunda columna.
                delete_subtask_button.grid(row=subtask_row, column=1, padx=5, pady=5)

                # Incrementamos 'subtask_row' para asegurar que la siguiente subtarea (si la hay) se muestre en la fila siguiente.
                subtask_row += 1

        # Al finalizar, devolvemos el valor actualizado de 'subtask_row'.
        return subtask_row

    # Método para marcar o desmarcar una tarea como completada o pendiente.
    def toggle_task(self, task, var):
        # Verificamos el estado de la variable 'var', que está vinculada al Checkbutton de la tarea.
        if var.get():
            mark_task_complete(task.id)  # Marcar como completada
        else:
            unmark_task_complete(task.id)  # Desmarcar tarea
        self.refresh_task_list()  # Actualizar la interfaz

    # Método para marcar o desmarcar una subtarea como completada o pendiente.
    def toggle_subtask(self, subtask, var):
        # Al igual que con las tareas, verificamos el estado de la variable 'var', que está vinculada al Checkbutton de la subtarea.
        if var.get():
            mark_subtask_complete(subtask.id)  # Marcar como completada
        else:
            unmark_subtask_complete(subtask.id)  # Desmarcar subtarea
        self.refresh_task_list()  # Actualizar la interfaz

    # Método para eliminar una tarea.
    def delete_task(self, task):
        # Llamamos a la función 'delete_task' pasando el ID de la tarea que se desea eliminar.
        # Esta función se encarga de eliminar la tarea tanto de la lista de tareas como del archivo CSV.
        delete_task(task.id)
        self.refresh_task_list()  # Actualizar la interfaz

    # Método para eliminar una subtarea.
    def delete_subtask(self, subtask):
        # Llamamos a la función 'delete_subtask' pasando el ID de la subtarea que se desea eliminar.
        # Esta función se encarga de eliminar la subtarea tanto de la lista de subtareas como del archivo CSV.
        delete_subtask(subtask.id)
        self.refresh_task_list()  # Actualizar la interfaz

    # Método para agregar una nueva tarea.
    def add_task(self):
        # Abrimos un cuadro de diálogo para que el usuario ingrese el nombre de la nueva tarea.
        # La función 'simpledialog.askstring' muestra una ventana emergente donde el usuario puede escribir texto.
        task_title = simpledialog.askstring("Nueva Actividad", "Ingresa el nombre de la Actividad:")
        if task_title:
            # Llamamos a la función 'add_task', pasando el título de la tarea ingresada por el usuario.
            # Esta función agrega la tarea a la lista y la guarda en el archivo CSV.
            add_task(task_title)
            self.refresh_task_list()  # Actualizar la interfaz

    # Método para agregar una subtarea a una tarea existente.
    def add_subtask(self, task):
        # Abrimos un cuadro de diálogo para que el usuario ingrese el nombre de la nueva subtarea.
        subtask_title = simpledialog.askstring("Nueva Subactividad", "Ingresa el nombre de la Subactividad:")
        if subtask_title:
            # Llamamos a la función 'add_subtask', pasando el ID de la tarea a la que se agregará la subtarea
            # y el título de la nueva subtarea ingresada por el usuario.
            # Esta función agrega la subtarea a la lista y la guarda en el archivo CSV.
            add_subtask(task.id, subtask_title)
            self.refresh_task_list()  # Actualizar la interfaz

# Crear la ventana principal
if __name__ == "__main__": 
    root = tk.Tk()  # Crea una nueva instancia de la ventana principal de la aplicación
    app = TaskApp(root)  # Crea la instancia de la clase 'TaskApp', que inicializa la interfaz gráfica
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica, que espera y responde a los eventos del usuario

