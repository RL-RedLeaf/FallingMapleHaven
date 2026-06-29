class PluginRegistry {
  constructor() {
    this.plugins = new Map()
  }

  register(pluginConfig) {
    this.plugins.set(pluginConfig.type, pluginConfig)
  }

  getPlugin(type) {
    return this.plugins.get(type)
  }

  getActivePlugins() {
    return Array.from(this.plugins.values())
  }

  getRoutes() {
    const routes = []
    for (const plugin of this.plugins.values()) {
      if (plugin.route) {
        routes.push(plugin.route)
      }
    }
    return routes
  }

  getAdminRoutes() {
    const routes = []
    for (const plugin of this.plugins.values()) {
      if (plugin.adminRoute) {
        routes.push({
          ...plugin.adminRoute,
          meta: { requiresAuth: true, requiresAdmin: true },
        })
      }
    }
    return routes
  }

  getAdminSidebarItems() {
    const items = []
    for (const plugin of this.plugins.values()) {
      if (plugin.adminSidebar && plugin.adminRoute) {
        items.push({
          path: '/admin/' + plugin.adminRoute.path,
          name: plugin.adminSidebar.name,
          icon: plugin.adminSidebar.icon,
        })
      }
    }
    return items
  }
}

export const pluginRegistry = new PluginRegistry()
