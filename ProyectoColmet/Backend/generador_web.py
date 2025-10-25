import os
import http.server
import socketserver
import threading
from contextlib import suppress
import customtkinter as ctk
import webbrowser
import atexit

def generar_web():
    # Configuración del puerto
    PORT = 8000
    server = None
    server_thread = None

    # Función para crear la página web
    def create_web_page(title, body_text, theme):
        folder_name = "Pagina Colmet"
        os.makedirs(folder_name, exist_ok=True)

        # Archivo HTML
        with open(os.path.join(folder_name, "index.html"), "w") as f:
            f.write(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
                <link rel="stylesheet" href="style.css">
            </head>
            <body>
                <h1>{title}</h1>
                <p>{body_text}</p>
            </body>
            </html>
            """)

        # Archivo CSS
        with open(os.path.join(folder_name, "style.css"), "w") as f:
            if theme == "Claro":
                f.write("""
                body {
                    background-color: #fff;
                    color: #fff;
                    font-family: Arial, sans-serif;
                }

                h1 {
                    color: #66d9ef;
                }

                p {
                    color: #ccc;
                }

                a {
                    color: #66d9ef;
                    text-decoration: none;
                }

                a:hover {
                    color: #fff;
                    text-decoration: underline;
                }

                button {
                    background-color: #444;
                    color: #fff;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                }

                button:hover {
                    background-color: #555;
                }



                """)
            else:
                f.write("""
                body {
                    background-color: #333;
                    color: #333;
                    font-family: Arial, sans-serif;
                }

                h1 {
                    color: #3498db;
                }

                p {
                    color: #666;
                }

                a {
                    color: #3498db;
                    text-decoration: none;
                }

                a:hover {
                    color: #2ecc71;
                    text-decoration: underline;
                }

                button {
                    background-color: #4CAF50;
                    color: #fff;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                }

                button:hover {
                    background-color: #3e8e41;
                }
                """)

        # Iniciar servidor web
        start_web_server(folder_name)

    # Función para iniciar el servidor web
    def start_web_server(folder_name):
        global server, server_thread

        if server_thread and server_thread.is_alive():
            print("El servidor ya está corriendo.")
            return

        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=folder_name, **kwargs)

        server = socketserver.TCPServer(("localhost", PORT), CustomHandler)

        def run_server():
            with suppress(Exception):
                server.serve_forever()

        # Iniciar servidor en un hilo
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Registrar cierre del servidor al salir
        atexit.register(stop_web_server)

        # Abrir la página web automáticamente
        print(f"Servidor iniciado en http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}")

    # Función para detener el servidor
    def stop_web_server():
        global server
        if server:
            server.shutdown()
            server.server_close()
            print("Servidor detenido.")

    # Interfaz gráfica con CustomTkinter
    def main():
        app = ctk.CTk()
        app.title("Generador de páginas web")
        app.geometry("1024x720")

        def generate_web_page():
            title = title_entry.get()
            body_text = body_entry.get("1.0", "end").strip()
            theme = theme_var.get()
            create_web_page(title, body_text, theme)

        # Widgets
        ctk.CTkLabel(app, text="Título de la página:").pack(pady=10)
        title_entry = ctk.CTkEntry(app)
        title_entry.pack()

        ctk.CTkLabel(app, text="Texto del cuerpo:").pack(pady=10)
        body_entry = ctk.CTkTextbox(app, height=50)
        body_entry.pack()

        theme_var = ctk.StringVar(value="Claro")
        ctk.CTkLabel(app, text="Tema:").pack(pady=10)
        ctk.CTkRadioButton(app, text="Claro", variable=theme_var, value="Claro").pack()
        ctk.CTkRadioButton(app, text="Oscuro", variable=theme_var, value="Oscuro").pack()

        generate_button = ctk.CTkButton(app, text="Generar Página Web", command=generate_web_page)
        generate_button.pack(pady=20)

        app.protocol("WM_DELETE_WINDOW", lambda: (stop_web_server(), app.destroy()))
        app.mainloop()

    if __name__ == "__main__":
        main()
