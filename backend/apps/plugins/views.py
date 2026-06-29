from rest_framework.views import APIView
from rest_framework.response import Response
from apps.plugins.registry import PluginRegistry


class ActivePluginsView(APIView):
    def get(self, request):
        plugins = PluginRegistry.get_active_plugins()
        data = [
            {
                "type": p.plugin_type,
                "name": p.display_name,
                "icon": p.icon,
                "description": p.description,
            }
            for p in plugins.values()
        ]
        return Response({"code": 0, "message": "success", "data": data})
