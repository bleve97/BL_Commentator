import wx

import wx
import includes
import commclasses as CC
import scoreboard as SB



#class PlayerInfoPanel(wx.Panel):
class PlayerWidget():

    def __init__(self, parent, title, player):
        super().__init__(parent)

        PlayerSizer = wx.FlexGridSizer(1,4,1,10)


        numFont = wx.Font(wx.FontInfo(40).Bold())
        PNumber = wx.StaticText(self, wx.ID_ANY,  str(player.GameNumber), style=wx.ALIGN_CENTER_HORIZONTAL)
        PNumber.SetBackgroundColour(wx.Colour(255, 255, 255))
        PNumber.SetForegroundColour(wx.Colour(47, 47, 79))
        PNumber.SetFont(numFont)
        PlayerSizer.Add(PNumber, 4, wx.ALIGN_CENTER | wx.ALL | wx.FIXED_MINSIZE, 1)

        namesSizer = wx.FlexGridSizer(2, 1, 0, 0)
        PlayerSizer.Add(namesSizer, 1, wx.EXPAND, 0)

        Sirname = wx.StaticText(self, wx.ID_ANY, player.SirName, style=wx.ALIGN_CENTER_HORIZONTAL)
        Sirname.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        namesSizer.Add(Sirname, 1, wx.ALL, 4)

        firstNamePronounceSizer = wx.GridBagSizer(0, 0)
        namesSizer.Add(firstNamePronounceSizer, 1, wx.EXPAND, 0)

        FirstName = wx.StaticText(self, wx.ID_ANY, player.FirstName, style=wx.ALIGN_LEFT)
        FirstName.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        firstNamePronounceSizer.Add(FirstName, (0, 0), (1, 1), wx.ALIGN_CENTER | wx.ALL, 5)

        Pronounced = wx.StaticText(self, wx.ID_ANY, player.PronunciationGuide, style=wx.ALIGN_RIGHT)
        Pronounced.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_BOLD, 0, ""))
        firstNamePronounceSizer.Add(Pronounced, (0, 1), (1, 1), wx.ALIGN_CENTER | wx.ALL, 5)

        grid_sizer_1 = wx.FlexGridSizer(3, 1, 0, 2)
        PlayerSizer.Add(grid_sizer_1, 1, wx.ALL | wx.EXPAND, 5)

        Goals = wx.StaticText(self, wx.ID_ANY, str(player.GameGoals))
        Goals.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        grid_sizer_1.Add(Goals, 0, 0, 0)

        Assists = wx.StaticText(self, wx.ID_ANY, str(player.GameAssists))
        Assists.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, ""))
        grid_sizer_1.Add(Assists, 0, 0, 0)

        PIM = wx.StaticText(self, wx.ID_ANY, str(player.GamePIM))
        PIM.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_BOLD, 0, ""))
        grid_sizer_1.Add(PIM, 0, 0, 0)

        firstNamePronounceSizer.AddGrowableCol(0)
        # firstNamePronounceSizer.AddGrowableCol(1)

        namesSizer.AddGrowableRow(0)
        namesSizer.AddGrowableCol(0)

        self.SetSizer(PlayerSizer)

        self.Layout()







class TeamPanel(wx.Panel):

    def __init__(self, parent, teamName, team):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticBox(self, -1, teamName)
        main_sizer.Add(title, 0, wx.TOP|wx.LEFT, 10)
        for player in team:
            print("player in team panel :". player.FirstName)
            #PPanel = PlayerInfoPanel(self, player=player, title="bloot")
            PWidget = PlayerWidget(self, title=teamName, player=player)
            #main_sizer.Add(PPanel, 0)
            main_sizer.Add((PWidget, 0))

        self.SetSizer(main_sizer)
#class PlayerInfoPanel():
#    def __init__(self):
#        print("hi")
    # hi


class TeamFrame(wx.Frame):

    def __init__(self, title, parent=None):
        wx.Frame.__init__(self,parent=parent, title=title)
        testPlayer = CC.Player(PlayerID = 1234, GameNumber = 69, FirstName = "Ernie", SirName = "Vanker", PronunciationGuide="WANKer")
        testPlayer2 = CC.GetPlayerByXciteID(19113)
        #panel=PlayerInfoPanel(self,player=testPlayer, title="bar")
        # panel=TeamPanel(self, teamName="hometeam name", team=[testPlayer, testPlayer2])
        #panel2=PlayerInfoPanel(self,player=testPlayer2, title="bloot")
        #panel=TeamPanel(self, )
        self.Show()

    def SetTeam(self, team):
        # create playerwidgets for each player in the team, to insert into the sizer for the team panel
        for num in team:
            player = team[num]
            print("SetTeam : ", player.FirstName, player.PronunciationGuide)

