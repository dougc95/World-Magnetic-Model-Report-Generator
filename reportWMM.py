import wx
import wx.adv
import datetime #para delta
import WMMv2
import pandas as pd
from xlsgen import WMM
import os 




def ft2km(pies):
	return pies * 0.3048780487804878 /1000


class WMMGui(wx.Frame):
    def __init__(self,parent,title,x,y):
        wx.Frame.__init__(self,parent=parent,title=title,size=(x,y))
        #Panel
        panel = wx.Panel(self)
        #Botones
        buttonGen = wx.Button(panel,-1,label = u"Generar",pos = (435,200))
        buttonGen.SetSize(75,50)
        #Label
        label1 = wx.StaticText(panel,-1,"Latitude", pos= (20,55))
        label2 = wx.StaticText(panel,-1,"Longitud", pos= (20,130))
        label3 = wx.StaticText(panel,-1,"Elevacion", pos= (20,210))
        label4 = wx.StaticText(panel,-1,"Fecha Inicial", pos= (300,10))
        label5 = wx.StaticText(panel,-1,"Fecha Final", pos= (585,10))
        label6 = wx.StaticText(panel,-1,"Delta", pos= (250,210))
        label7 = wx.StaticText(panel,-1,"Archivo", pos= (535,210))        
        #Get Text
        self.txtLat = wx.TextCtrl(panel,pos = (80,55))
        self.txtLon = wx.TextCtrl(panel,pos = (80,130))
        self.txtAlt = wx.TextCtrl(panel,pos = (80,210))
        self.txtDelta = wx.TextCtrl(panel,pos = (290,210),size = (50,25))
        self.txtFile = wx.TextCtrl(panel,pos=(585,210))
        #Calendar
        self.calendarioIni = wx.adv.CalendarCtrl(panel,pos = (220,40))
        self.calendarioFin = wx.adv.CalendarCtrl(panel,pos = (500,40))
        #Radio Buttons
        self.rbotN=wx.RadioButton(panel, label = "North", pos= (50,10),style=wx.RB_GROUP)
        self.rbotS=wx.RadioButton(panel, label = "South", pos= (50,30))
        self.rbotLat=wx.RadioButton(panel, label = "West", pos= (50,90),style=wx.RB_GROUP)
        self.rbotLon=wx.RadioButton(panel, label = "East", pos= (50,110))
        self.rbotKm=wx.RadioButton(panel, label = "KM", pos= (50,165),style=wx.RB_GROUP)
        self.rbotFt=wx.RadioButton(panel, label = "Feet", pos= (50,185))
        #Window
        self.Center(True)
        self.Show()
        #Event
        self.Bind(wx.EVT_BUTTON, self.onClickGen, buttonGen)


    def onClickGen(self, event):
        if(self.rbotN.GetValue()):
            self.lat = float(self.txtLat.GetValue())
        else:
            self.lat = -float(self.txtLat.GetValue())
            pass

        if(self.rbotLat.GetValue()):
            self.lon = -float(self.txtLon.GetValue())
        else:
            self.lon = float(self.txtLon.GetValue())
            pass

        if(self.rbotKm.GetValue()):
            self.alt = float(self.txtAlt.GetValue())
        else:
            self.alt = ft2km(float(self.txtAlt.GetValue()))
            pass

        self.writerBook(self.generateDates())
        pass

    def generateDates(self):
        start = str(self.calendarioIni.PyGetDate())[0:10]
        end = str(self.calendarioFin.PyGetDate())[0:10]
        #Parse str into date
        aux1 = start.split("-")
        aux2 = end.split("-")
        start = datetime.date(int(aux1[0]), int(aux1[1]), int(aux1[2]))
        end = datetime.date(int(aux2[0]), int(aux2[1]), int(aux2[2]))
        #start iteration
        print(self.txtDelta.GetValue())
        step = int(self.txtDelta.GetValue())
        delta = datetime.timedelta(days = step )
        cup = list()
        while start <= end:
            print(start)
            cup.append(str(start))
            start = start + delta
        pass
        print(cup)
        return cup


    def writerBook(self, dates):
        #1st section
        vectorTotalField = []
        vectorHorizontal = []
        vectorNorth = []
        vectorEast = []
        vectorVertical = []
        vectorDeclination = []
        vectorInclination = []
        #2nd section
        deltaVectorTotalField = []
        deltaVectorHorizontal = []
        deltaVectorNorth = []
        deltaVectorEast = []
        deltaVectorVertical = []
        deltaVectorDeclination = []
        deltaVectorInclination = []
        #Check Values
        print("Lat:"+str(self.lat))
        print("Lon:"+str(self.lon))
        print("Alt:"+str(self.alt))
        for x in dates:
            vaso = WMM(self.lat,self.lon,self.alt,x)
            x = vaso.decimalYear(x)
            vecIntensity=WMMv2.getIntensity(self.lat,self.lon,x,self.alt)
            vecHorizontalIntensity=WMMv2.getHorizontalIntensity(self.lat,self.lon,x,self.alt)
            vecNorthIntensity=WMMv2.getNorthIntensity(self.lat,self.lon,x,self.alt)
            vecEastIntensity=WMMv2.getEastIntensity(self.lat,self.lon,x,self.alt)
            vecVerticalIntensity=WMMv2.getVerticalIntensity(self.lat,self.lon,x,self.alt)
            vecDeclination=WMMv2.getDeclination(self.lat,self.lon,x,self.alt)
            vecDipAngle=WMMv2.getDipAngle(self.lat,self.lon,x,self.alt)
            #Get values from next year
            vecIntensity2=WMMv2.getIntensity(self.lat,self.lon,x+1,self.alt)
            vecHorizontalIntensity2=WMMv2.getHorizontalIntensity(self.lat,self.lon,x+1,self.alt)
            vecNorthIntensity2=WMMv2.getNorthIntensity(self.lat,self.lon,x+1,self.alt)
            vecEastIntensity2=WMMv2.getEastIntensity(self.lat,self.lon,x+1,self.alt)
            vecVerticalIntensity2=WMMv2.getVerticalIntensity(self.lat,self.lon,x+1,self.alt)
            vecDeclination2=WMMv2.getDeclination(self.lat,self.lon,x+1,self.alt)
            vecDipAngle2=WMMv2.getDipAngle(self.lat,self.lon,x+1,self.alt)
            #Add values of 1st yr to buff
            vectorTotalField.append(vecIntensity)
            vectorHorizontal.append(vecHorizontalIntensity) 
            vectorNorth.append(vecNorthIntensity) 
            vectorEast.append(vecEastIntensity)
            vectorVertical.append(vecVerticalIntensity)
            vectorDeclination.append(vecDeclination)
            vectorInclination.append(vecDipAngle)
            #Variacion anual yr2-yr1
            deltaIntensity=vecIntensity2-vecIntensity
            deltaHorizontalIntensity=vecHorizontalIntensity2-vecHorizontalIntensity
            deltaNorthIntensity=vecNorthIntensity2-vecNorthIntensity
            deltaEastIntensity=vecEastIntensity2-vecEastIntensity
            deltaVerticalIntensity=vecVerticalIntensity2-vecVerticalIntensity
            deltaDeclination=vecDeclination2-vecDeclination
            deltaDipAngle=vecDipAngle2-vecDipAngle
            #Add values of yr2-yr1 to buff
            deltaVectorTotalField.append(deltaIntensity)
            deltaVectorHorizontal.append(deltaHorizontalIntensity)
            deltaVectorNorth.append(deltaNorthIntensity)
            deltaVectorEast.append(deltaEastIntensity)
            deltaVectorVertical.append(deltaVerticalIntensity)
            deltaVectorDeclination.append(deltaDeclination)
            deltaVectorInclination.append(deltaDipAngle)

            pass
        #Data frame section 1
        df1 = pd.DataFrame({'Date': dates})
        df2 = pd.DataFrame({'Total Field': vectorTotalField})
        df3 = pd.DataFrame({'Horizontal': vectorHorizontal})
        df4 = pd.DataFrame({'North': vectorNorth})
        df5 = pd.DataFrame({'East': vectorEast})
        df6 = pd.DataFrame({'Vertical': vectorVertical})
        df7 = pd.DataFrame({'Declination': vectorDeclination})
        df8 = pd.DataFrame({'Inclination': vectorInclination})
        #Data frame section 2
        dfd1 =pd.DataFrame({'\u0394 Total Field': deltaVectorTotalField})
        dfd2 =pd.DataFrame({'\u0394 Horizontal': deltaVectorHorizontal})
        dfd3 = pd.DataFrame({'\u0394 North': deltaVectorNorth})
        dfd4 = pd.DataFrame({'\u0394 East': deltaVectorEast})
        dfd5 = pd.DataFrame({'\u0394 Vertical': deltaVectorVertical})
        dfd6 = pd.DataFrame({'\u0394 Declination': deltaVectorDeclination})
        dfd7 = pd.DataFrame({'\u0394 Inclination': deltaVectorInclination})

        
        auxFile = os.getcwd()+'\\'+str(self.txtFile.GetValue())+'.xlsx'
        writer = pd.ExcelWriter(auxFile, engine='xlsxwriter')
        
        df1.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=0,index=False)
        df2.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=1,index=False)
        df3.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=2,index=False)
        df4.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=3,index=False)
        df5.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=4,index=False)
        df6.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=5,index=False)
        df7.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=6,index=False)
        df8.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=7,index=False)

        dfd1.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=9,index=False)
        dfd2.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=10,index=False)
        dfd3.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=11,index=False)
        dfd4.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=12,index=False)
        dfd5.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=13,index=False)
        dfd6.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=14,index=False)
        dfd7.to_excel(writer, sheet_name='Sheet1', startrow=0,startcol=15,index=False)


        writer.save()
    

        


app = wx.App()
frame = WMMGui(None,"Reports",800,300)
app.MainLoop()