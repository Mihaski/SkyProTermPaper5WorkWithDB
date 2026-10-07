from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Абстрактный класс для работы с API-сервисами."""

    @abstractmethod
    def get_data(self, *args, **kwargs):
        """Получает данные из API-сервиса."""
        pass
