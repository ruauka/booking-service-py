# файл изменяет переменную окружения на TEST при запуске тестов через pytest.
import os

os.environ["MODE"] = "TEST"
