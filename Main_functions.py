#from syslab import SwitchBoard
#from syslab import GaiaWindTurbine
#from syslab import Photovoltaics
#from syslam import Dumpload

#node_1 ="pv715" #pv
#node_2 ="gaia1" #gaia (wt)
#node_3 ="mobload2" #mobileload2 (wb)

#SB= SwitchBoard("715-2") # flexhouse
#PV=Photovoltaics(node_1)
#GAIA=GaiaWindTurbine(node_2)
#MobILELOAD=Dumpload(node_3)


class Default:
    def __init__(self,unit_connection,unit_name):
        self.unit_connection = unit_connection
	self.unit_name = unit_name
        measurement = None
        set_point_A =None

    def Get_measurement(self):
        if self.unit_name="pv":
           measurement=self.connection.getACActivePower().value
        elif self.unit_name="windturbine":
           measurement=self.connection.GaiaWindTurbine().value
        elif self.unit_name="flexHOS":
           measurement=self.connection.getActivePower().value
        else:
            print("Invalid node name, please check the node")
        return measurement


    def Set_Point(self, power):
        if self.unit_name="pv":
           set_point_A=self.connection.setPacLimit(power)
        elif self.unit_name="mobileload":
           set_point_A=self.connection.setPowerSetpoint(float P)
        else:
            print("Invalid node name request, please check the node")
        return set_point_A

#class pv():

 #   def __init__(self):
 #       self.node_1 ="pv715" #pv
 #       self.PV=Photovoltaics(node_1)

 #   def PVPower(self):
 #       activepower = self.PV.getACActivePower().value #Gets the current active power production P
 #       return activepower

 #   def SET_PV_powerLimit(self, power): #Set a limit on the amount of energy output onto the grid
 #       powerLimit= self.PV.setPacLimit(power)
 #       return powerLimit

#class GAIAA():
 #   def __init__(self):
 #       self.node_2 ="gaia1" #gaia (wt)
 #       self.GAIA=GaiaWindTurbine(node_2)

#    def GAIAPower(self): # Current production of the turbine
#        powergaia = self.GAIA.GaiaWindTurbine().value
#        return powergaia 

#   def GAIA_WIND_SPEED(): # Get the wind speed as measured at the nacelle
#       wind_speed = self.GAIA.getWindspeed()
#      return wind_speed

#class LOAD():
#    def __init__(self):
#	self.node_3 ="mobload2" #mobileload2 (wb)
#	self.MObILELOAD=Dumpload(node_3)

#   def Set_Dumpload_Active_Power(self, float P): #Sets the dumpload to consume active power P
#       dumploadpower = self.MobILELOAD.setPowerSetpoint(float P)
#       return dumploadpower

#   def StartLoad(self): # Starts the load
#       startingload = self.MobILELOAD.startLoad()
#       return startingload

#  def StopLoad(self): # Stops the load
      #stoppingload = self.MobILELOAD.stopLoad()
      #return stoppingload


#class flexHOS():
#    def __init__(self):	
#	self.SB= SwitchBoard("715-2")

#   def flexhouse_Active_power(): #Get the active power P from instrument i
#       consumption = self.SB.getActivePower().value
#       return consumption

#  def flexhouse_reactive_power(): #Get the reactive power Q from instrument i
#      reactive_power = self.SB.getReactivePower
#      return reactive_power






 

 



