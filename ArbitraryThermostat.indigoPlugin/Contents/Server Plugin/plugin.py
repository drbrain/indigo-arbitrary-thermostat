import indigo

class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName,
                                   pluginVersion, pluginPrefs)

        self.debug = pluginPrefs.get('debug', False)

        self.devices = {}

    def deviceStartComm(self, device):
        if device.id not in self.devices:
            self.devices[device.id] = device

    def deviceStopComm(self, device):
        if device.id in self.diveces:
            self.devices.pop(device.id)
