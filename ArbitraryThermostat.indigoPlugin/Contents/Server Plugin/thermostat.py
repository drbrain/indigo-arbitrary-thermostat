import indigo

class Thermostat:
    def __init__(self, plugin, device):
        self.plugin = plugin
        self.device = device

        self.coolDevice        = None
        self.heatDevice        = None
        self.humidifierDevice  = None
        self.hygrometerDevice  = None
        self.thermometerDevice = None

        self.setDevices()
        self.setProperties()

    def setDevices(self):
        coolDeviceId        = self.device.ownerProps['coolDevice']
        heatDeviceId        = self.device.ownerProps['heatDevice']
        humidifierDeviceId  = self.device.ownerProps['humidifierDevice']
        hygrometerDeviceId  = self.device.ownerProps['hygrometerDevice']
        thermometerDeviceId = self.device.ownerProps['thermometerDevice']

        if coolDeviceId != "":
            self.coolDevice        = indigo.devices[int(coolDeviceId)]

        if heatDeviceId != "":
            self.heatDevice        = indigo.devices[int(heatDeviceId)]

        if humidifierDeviceId != "":
            self.humidifierDevice  = indigo.devices[int(humidifierDeviceId)]

        if hygrometerDeviceId != "":
            self.hygrometerDevice  = indigo.devices[int(hygrometerDeviceId)]

        if thermometerDeviceId != "":
            self.thermometerDevice = indigo.devices[int(thermometerDeviceId)]

    def setProperties(self):
        pluginProps = self.device.pluginProps

        pluginProps["NumTemperatureInputs"] = 1
        pluginProps["NumHumidityInputs"]    = 1

        self.device.replacePluginPropsOnServer(pluginProps)

    def update(self, oldDevice, newDevice):
        if self.coolDevice and oldDevice.id == self.coolDevice.id:
            self.plugin.debugLog("cooler %d updated to %f" % (
                oldDevice.id, newDevice.sensorValue))
        elif self.heatDevice and oldDevice.id == self.heatDevice.id:
            self.plugin.debugLog("heater %d updated to %f" % (
                oldDevice.id, newDevice.sensorValue))
        elif self.humidifierDevice and oldDevice.id == self.humidifierDevice.id:
            self.plugin.debugLog("humidifier %d updated to %f" % (
                oldDevice.id, newDevice.sensorValue))
        elif self.hygrometerDevice and oldDevice.id == self.hygrometerDevice.id:
            self.plugin.debugLog("hygrometer %d updated to %f" % (
                oldDevice.id, newDevice.sensorValue))

            self.device.updateStateOnServer("humidityInput1", newDevice.sensorValue)
        elif self.thermometerDevice and oldDevice.id == self.thermometerDevice.id:
            self.plugin.debugLog("thermometer %d updated to %f" % (
                oldDevice.id, newDevice.sensorValue))

            self.device.updateStateOnServer("temperatureInput1", newDevice.sensorValue)
