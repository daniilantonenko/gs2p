import http.server
import os

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        allowed_directory = 'files'
        
        # Получите запрашиваемый путь
        requested_path = self.path.lstrip('/')
        
        # Проверьте, начинается ли запрашиваемый путь с разрешенной директории
        if not requested_path.startswith(allowed_directory):
            self.send_error(403, "403 Forbidden: Access is denied.")
            return

        # Путь к запрашиваемому файлу
        requested_file = self.path.lstrip('/')

        # Проверка существования файла
        if not os.path.exists(requested_file):
            print(f"Ошибка 404: Файл '{requested_file}' не найден.")
            self.send_error(404, "File not found")
            return

        # Проверка прав доступа к файлу
        if not os.access(requested_file, os.R_OK):
            print(f"Ошибка 403: Доступ к файлу '{requested_file}' запрещен.")
            self.send_error(403, "403 Forbidden: Access is denied.")
            return

        # Если файл существует и доступен, обрабатываем запрос
        try:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            self.send_error(500, "Внутренняя ошибка сервера.")