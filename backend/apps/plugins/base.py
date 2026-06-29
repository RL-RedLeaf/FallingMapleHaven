from abc import ABC, abstractmethod


class BasePlugin(ABC):
    plugin_type: str = ""
    display_name: str = ""
    description: str = ""
    icon: str = ""

    @abstractmethod
    def get_profile_data(self, user_id: int) -> dict:
        pass

    def get_routes(self) -> list:
        return []

    def get_admin_config(self) -> dict:
        return {}
