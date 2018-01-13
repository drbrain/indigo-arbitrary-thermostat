import indigo

class Thermostat:
    def __init__(self, plugin, thermostat):
        self.plugin     = plugin
        self.thermostat = thermostat

        self.coolDevice        = None
        self.heatDevice        = None
        self.humidifierDevice  = None
        self.hygrometerDevice  = None
        self.thermometerDevice = None

        self.setDevices()
        self.setProperties()

    def debugLog(self, message):
        self.plugin.debugLog(message)

    def setDevices(self):
        coolDeviceId        = self.thermostat.ownerProps['coolDevice']
        heatDeviceId        = self.thermostat.ownerProps['heatDevice']
        humidifierDeviceId  = self.thermostat.ownerProps['humidifierDevice']
        hygrometerDeviceId  = self.thermostat.ownerProps['hygrometerDevice']
        thermometerDeviceId = self.thermostat.ownerProps['thermometerDevice']

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
        pluginProps = self.thermostat.pluginProps

        pluginProps["NumTemperatureInputs"] = 1
        pluginProps["NumHumidityInputs"]    = 1

        self.thermostat.replacePluginPropsOnServer(pluginProps)

    def update(self, oldDevice, newDevice):
        if self.coolDevice and oldDevice.id == self.coolDevice.id:
            self.coolDevice = newDevice
            temperature  = float(self.thermometerDevice.sensorValue)
            coolSetpoint = self.thermostat.coolSetpoint

            if newDevice.onState and temperature <= coolSetpoint:
                indigo.device.turnOff(self.coolDevice.id)
            elif not newDevice.onState and temperature > coolSetpoint:
                indigo.device.turnOn(self.coolDevice.id)

        elif self.heatDevice and oldDevice.id == self.heatDevice.id:
            self.heatDevice = newDevice
            self.updateHeater()

        elif self.humidifierDevice and oldDevice.id == self.humidifierDevice.id:
            self.humidifierDevice = newDevice
            humidity = float(self.hygrometerDevice.sensorValue)

            # need humidity target to add humidifier control

        elif self.hygrometerDevice and oldDevice.id == self.hygrometerDevice.id:
            self.debugLog("hygrometer %d updated to %f" % (
                oldDevice.id, newDevice.sensorValue))

            self.hygrometerDevice = newDevice
            self.thermostat.updateStateOnServer("humidityInput1", newDevice.sensorValue)

        elif self.thermometerDevice and oldDevice.id == self.thermometerDevice.id:
            self.thermometerDevice = newDevice
            temperature = newDevice.sensorValue

            self.debugLog("thermometer %d updated to %f" % (
                oldDevice.id, temperature))

            self.thermostat.updateStateOnServer("temperatureInput1", temperature)

            self.updateHeater()
        elif self.thermostat == newDevice:
            self.updateHeater()

    def updateHeater(self):
        self.thermostat.refreshFromServer() # don't rely on subscriptions

        temperature  = float(self.thermometerDevice.sensorValue)
        heatSetpoint = self.thermostat.heatSetpoint

        if temperature >= heatSetpoint:
            indigo.device.turnOff(self.heatDevice.id)

            self.debugLog("heat off %s (%d) %f >= %f" % (
                self.heatDevice.name, self.heatDevice.id,
                temperature, heatSetpoint))
        elif temperature < heatSetpoint:
            indigo.device.turnOn(self.heatDevice.id)

            self.debugLog("heat on %s (%d) %f < %f" % (
                self.heatDevice.name, self.heatDevice.id,
                temperature, heatSetpoint))

