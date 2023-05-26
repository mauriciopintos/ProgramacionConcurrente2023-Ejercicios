import socket
import threading
import tkinter as tk
from tkinter import messagebox

# Variables globales
DEFAULT_PORT = 5500
MAX_CONNS = 5
BUFSIZ = 1024
ADDR = ''
USERNAME = ''
connected = False

class ChatWindow(tk.Toplevel):
    """Ventana principal de la aplicación"""
    def __init__(self, title, subtitle):
        super().__init__()
        self.title(title)
        self.geometry("600x400")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: close_window(self))

        # Menú de la ventana
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Nueva conversación", command=self.new_chat)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=lambda: close_window(self))
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.config(menu=self.menu_bar)

        # Barra de herramientas
        self.toolbar = tk.Frame(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.btn_new_chat = tk.Button(self.toolbar, text="Nueva conversación", command=self.new_chat)
        self.btn_new_chat.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_close_chat = tk.Button(self.toolbar, text="Cerrar conversación", command=self.close_chat, state=tk.DISABLED)
        self.btn_close_chat.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_exit = tk.Button(self.toolbar, text="Salir", command=lambda: close_window(self))
        self.btn_exit.pack(side=tk.RIGHT, padx=5, pady=5)

        # Título y subtítulo
        self.lbl_title = tk.Label(self, text=title, font=("Arial", 16))
        self.lbl_title.pack()

        self.lbl_subtitle = tk.Label(self, text=subtitle, font=("Arial", 12))
        self.lbl_subtitle.pack(pady=5)
        
        # Seleccionar chats
        self.chat_selector = tk.Frame(self)
        self.chat_selector.pack(side=tk.LEFT, fill=tk.Y)

        self.lbl_selector_title = tk.Label(self.chat_selector, text="Conversaciones", font=("Arial", 12))
        self.lbl_selector_title.pack(pady=5)

        self.chat_listbox = tk.Listbox(self.chat_selector, selectmode=tk.SINGLE)
        self.chat_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.chat_listbox.bind("<<ListboxSelect>>", self.on_select_chat)
        
        # Variables de usuario y conexión
        self.username = getpass.getuser()
        self.current_chat = None
        self.connections = {}

        # Frame principal
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True, fill="both")

        # Frame de selección de chats
        self.chat_select_frame = tk.Frame(self.frame)
        self.chat_select_frame.pack(side="left", fill="y")

        self.lbl_chat_select = tk.Label(self.chat_select_frame, text="Seleccione el chat:", font=("Arial", 12))
        self.lbl_chat_select.pack(pady=5)

        self.chat_select_box = tk.Listbox(self.chat_select_frame, width=30, height=15)
        self.chat_select_box.pack(padx=10, pady=5)

        self.btn_new_chat = tk.Button(self.chat_select_frame, text="Nuevo chat", command=self.new_chat)
        self.btn_new_chat.pack(side="bottom", pady=10)

        # Frame de chat
        self.chat_frame = tk.Frame(self.frame)
        self.chat_frame.pack(side="left", fill="both", expand=True)

        self.chat_box = tk.Text(self.chat_frame, width=50, height=25, state="disabled")
        self.chat_box.pack(padx=10, pady=5, expand=True, fill="both")

        self.scrollbar = tk.Scrollbar(self.chat_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.chat_box.yview)

        # Frame de control
        self.control_frame = tk.Frame(self.frame)
        self.control_frame.pack(side="left", fill="y")
        
        # Botones de control
        self.btn_open_chat = ttk.Button(self.chat_list_frame, text="Abrir Chat", command=self.open_chat)
        self.btn_open_chat.pack(side=tk.LEFT, padx=10)

        self.btn_new_chat = ttk.Button(self.chat_list_frame, text="Nuevo Chat", command=self.new_chat)
        self.btn_new_chat.pack(side=tk.LEFT, padx=10)

        self.btn_exit = ttk.Button(self.chat_list_frame, text="Salir", command=lambda: close_window(self))
        self.btn_exit.pack(side=tk.RIGHT, padx=10)

        # Frame del chat actual
        self.current_chat_frame = ttk.Frame(self)
        self.current_chat_frame.pack(pady=20)

        self.lbl_current_chat = tk.Label(self.current_chat_frame, text="Seleccione un chat para empezar a conversar", font=("Arial", 12))
        self.lbl_current_chat.pack(pady=10)

        # Botones del chat actual
        self.btn_send = ttk.Button(self.current_chat_frame, text="Enviar", command=self.send_message)
        self.btn_send.pack(side=tk.RIGHT, padx=10)

        self.btn_close_chat = ttk.Button(self.current_chat_frame, text="Cerrar Chat", command=self.close_chat)
        self.btn_close_chat.pack(side=tk.RIGHT, padx=10)

        # Scrollbar y caja de mensajes
        self.chat_scrollbar = tk.Scrollbar(self.current_chat_frame)
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_box = tk.Text(self.current_chat_frame, state=tk.DISABLED)
        self.chat_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.chat_box.config(yscrollcommand=self.chat_scrollbar.set)
        self.chat_scrollbar.config(command=self.chat_box.yview)

        # Ventana de notificaciones
        self.notify_window = tk.Toplevel()
        self.notify_window.title("Notificaciones")
        self.notify_window.geometry("300x200")
        self.notify_window.withdraw()

        self.lbl_notify_title = tk.Label(self.notify_window, text="Nuevos mensajes", font=("Arial", 12))
        self.lbl_notify_title.pack(pady=5)

        self.lbl_notify_msg = tk.Label(self.notify_window, text="")
        self.lbl_notify_msg.pack()

        # Área de selección de chats
        self.lbl_select_chat = tk.Label(self, text="Seleccione una conversación:", font=("Arial", 12))
        self.lbl_select_chat.pack(padx=10, pady=5, anchor="w")

        self.cb_select_chat = ttk.Combobox(self, values=[], width=25)
        self.cb_select_chat.bind("<<ComboboxSelected>>", self.cb_select_chat_onselect)
        self.cb_select_chat.pack(padx=10, pady=5, anchor="w")

        # Área de chat activo
        self.lbl_chat_title = tk.Label(self, text="Chat", font=("Arial", 12))
        self.lbl_chat_title.pack(padx=10, pady=5, anchor="w")

        self.txt_chat = tk.scrolledtext.ScrolledText(self, height=10, state="disabled")
        self.txt_chat.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.lbl_msg = tk.Label(self, text="Mensaje:")
        self.lbl_msg.pack(padx=10, pady=5, anchor="w")

        self.ent_msg = tk.Entry(self, width=50)
        self.ent_msg.pack(padx=10, pady=5, anchor="w")

        # Botones de control
        self.btn_new_chat = tk.Button(self, text="Nueva conversación", command=self.new_chat)
        self.btn_new_chat.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_send_msg = tk.Button(self, text="Enviar", command=self.send_message)
        self.btn_send_msg.pack(side=tk.RIGHT, padx=10, pady=5)

        self.btn_close_chat = tk.Button(self, text="Cerrar conversación", command=self.close_chat)
        self.btn_close_chat.pack(side=tk.RIGHT, padx=10, pady=5)

        self.btn_exit = tk.Button(self, text="Salir", command=self.destroy)
        self.btn_exit.pack(side=tk.RIGHT, padx=10, pady=5)

        # Inicializar variables de estado
        self.server_ip = ""
        self.server_port = 0
        self.username = ""
        self.client_socket = None
        self.current_chat = None
        self.msg_queue = queue.Queue()

    def connect_to_server(self):
        """Conectar a un servidor"""
        # Ventana para ingresar IP o hostname del servidor
        connect_window = tk.Toplevel()
        connect_window.title("Conectar a servidor")
        connect_window.geometry("300x100")
        connect_window.resizable(False, False)

        lbl_ip = tk.Label(connect_window, text="IP o hostname:")
        lbl_ip.pack(padx=10, pady=10)

        entry_ip = tk.Entry(connect_window)
        entry_ip.pack(padx=10, pady=5)

        btn_connect = tk.Button(connect_window, text="Conectar", command=lambda: self._connect_to_server(entry_ip.get(), connect_window))
        btn_connect.pack(padx=10, pady=5)

    def _connect_to_server(self, server_addr, connect_window):
        """Conectar a un servidor (parte interna)"""
        # Validar dirección del servidor
        try:
            socket.inet_aton(server_addr)
            is_valid = True
        except socket.error:
            is_valid = False

        if not is_valid:
            try:
                socket.gethostbyname(server_addr)
                is_valid = True
            except socket.gaierror:
                is_valid = False

        if not is_valid:
            messagebox.showerror("Error", "Dirección del servidor no válida.")
            return

        # Conectar a servidor
        try:
            self.client = Client(server_addr, self.username)
            self.client.connect()
            self.btn_send.config(state="normal")
            self.btn_new_chat.config(state="normal")
            self.btn_connect.config(state="disabled")
            connect_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

    def send_message(self):
        """Enviar un mensaje"""
        msg = self.entry_msg.get()
        chat = self.chats[self.current_chat_idx]

        try:
            chat.client.send_message(msg)
            chat.add_message(self.username, msg)
            self.entry_msg.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el mensaje: {e}")

    def new_chat(self):
        """Crear una nueva conversación"""
        # Ventana para ingresar el destinatario
        new_chat_window = tk.Toplevel()
        new_chat_window.title("Nueva conversación")
        new_chat_window.geometry("300x100")
        new_chat_window.resizable(False, False)

        lbl_dest = tk.Label(new_chat_window, text="Destinatario:")
        lbl_dest.pack(padx=10, pady=10)

        entry_dest = tk.Entry(new_chat_window)
        entry_dest.pack(padx=10, pady=5)

        btn_create = tk.Button(new_chat_window, text="Crear", command=lambda: self._new_chat(entry_dest.get(), new_chat_window))
        btn_create.pack(padx=10, pady=5)

    def _new_chat(self, dest_username, new_chat_window):
        """Crear una nueva conversación (parte interna)"""
        # Validar nombre de usuario del destinatario
        if not dest_username:
            messagebox.showerror("Error", "Debe ingresar un nombre de usuario.")
            return

        # Verificar si la conversación ya existe
        for i, chat in enumerate(self.chats):
            if chat.username == dest_username:
                messagebox.showwarning("Advertencia", "La conversación ya existe.")
                self._change_current_chat(i)
                new_chat_window.destroy()
                return

        # Crear nueva convers
