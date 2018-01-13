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
        self.debugLog("action %s value %r device %d" % (
            action.thermostatAction,
            action.actionValue,
            device.id))

        thermostat   = self.thermostats[device.id]
        setpointCool = device.coolSetpoint
        setpointHeat = device.heatSetpoint

        if indigo.kThermostatAction.DecreaseCoolSetpoint == action.thermostatAction:
            setpointCool -= action.actionValue
        elif indigo.kThermostatAction.DecreaseHeatSetpoint == action.thermostatAction:
            setpointHeat -= action.actionValue
            thermostat.updateHeater()

        elif indigo.kThermostatAction.IncreaseCoolSetpoint == action.thermostatAction:
            setpointCool += action.actionValue
        elif indigo.kThermostatAction.IncreaseHeatSetpoint == action.thermostatAction:
            setpointHeat += action.actionValue
            thermostat.updateHeater()

        elif indigo.kThermostatAction.SetCoolSetpoint == action.thermostatAction:
            setpointCool = action.actionValue
        elif indigo.kThermostatAction.SetHeatSetpoint == action.thermostatAction:
            setpointHeat = action.actionValue
            thermostat.updateHeater()

        device.updateStateOnServer("setpointCool", setpointCool)
        device.updateStateOnServer("setpointHeat", setpointHeat)

    def deviceStartComm(self, device):
        if device.id not in self.thermostats:
            self.thermostats[device.id] = Thermostat(self, device)

    def deviceStopComm(self, device):
        if device.id in self.thermostats:
            self.thermostats.pop(device.id)

    def deviceUpdated(self, oldDevice, newDevice):
        for _, thermostat in self.thermostats.iteritems():
            thermostat.update(oldDevice, newDevice)

