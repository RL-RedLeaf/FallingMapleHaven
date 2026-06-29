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
}

export const pluginRegistry = new PluginRegistry()
