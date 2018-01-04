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
        if device.id in self.devices:
            self.devices.pop(device.id)

    def actionControlThermostat(self, action, device):
        self.debugLog("action %s value %r device %d" % (
            action.thermostatAction,
            action.actionValue,
            device.id))

        setpointCool = device.coolSetpoint
        setpointHeat = device.heatSetpoint

        if indigo.kThermostatAction.DecreaseCoolSetpoint == action.thermostatAction:
            setpointCool -= action.actionValue
        elif indigo.kThermostatAction.DecreaseHeatSetpoint == action.thermostatAction:
            setpointHeat -= action.actionValue
        elif indigo.kThermostatAction.IncreaseCoolSetpoint == action.thermostatAction:
            setpointCool += action.actionValue
        elif indigo.kThermostatAction.IncreaseHeatSetpoint == action.thermostatAction:
            setpointHeat += action.actionValue
        elif indigo.kThermostatAction.SetCoolSetpoint == action.thermostatAction:
            setpointCool = action.actionValue
        elif indigo.kThermostatAction.SetHeatSetpoint == action.thermostatAction:
            setpointHeat = action.actionValue

        device.updateStateOnServer("setpointCool", setpointCool)
        device.updateStateOnServer("setpointHeat", setpointHeat)
