import indigo
from thermostat import *

class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName,
                                   pluginVersion, pluginPrefs)

        self.debug = pluginPrefs.get('debug', False)

        self.thermostats = {}

        indigo.devices.subscribeToChanges()

    def actionControlThermostat(self, action, device):
        value  = action.actionValue
        mode   = action.actionMode
        action = action.thermostatAction

        self.debugLog("%s (%d) action %s value %r mode %r" % (
            device.name, device.id, action, value, mode))

        thermostat   = self.thermostats[device.id]
        setpointCool = device.coolSetpoint
        setpointHeat = device.heatSetpoint

        if indigo.kThermostatAction.DecreaseCoolSetpoint == action:
            device.updateStateOnServer("setpointCool", setpointCool - value)

        elif indigo.kThermostatAction.DecreaseHeatSetpoint == action:
            device.updateStateOnServer("setpointHeat", setpointHeat - value)
            thermostat.updateHeater()

        elif indigo.kThermostatAction.IncreaseCoolSetpoint == action:
            device.updateStateOnServer("setpointCool", setpointCool + value)

        elif indigo.kThermostatAction.IncreaseHeatSetpoint == action:
            device.updateStateOnServer("setpointHeat", setpointHeat + value)
            thermostat.updateHeater()

        elif indigo.kThermostatAction.SetCoolSetpoint == action:
            device.updateStateOnServer("setpointCool", value)

        elif indigo.kThermostatAction.SetHeatSetpoint == action:
            device.updateStateOnServer("setpointHeat", value)
            thermostat.updateHeater()

        elif indigo.kThermostatAction.SetHvacMode == action:
            device.updateStateOnServer("hvacOperationMode", mode)
            thermostat.updateHeater()

        self.debugLog("%s (%d) mode %s cool %.1f heat %.1f" % (
            device.name, device.id,
            device.hvacMode,
            device.coolSetpoint, device.heatSetpoint))

    def deviceStartComm(self, device):
        if device.id not in self.thermostats:
            self.thermostats[device.id] = Thermostat(self, device)

    def deviceStopComm(self, device):
        if device.id in self.thermostats:
            self.thermostats.pop(device.id)

