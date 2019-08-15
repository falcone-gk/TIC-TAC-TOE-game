"""
This script is intended to make a tic tac toe game with 2 playes and
a bot.
"""

import wx

class Programme(wx.Frame):
    """This class is the main class to start the game"""

    def __init__(self, parent, turn=1):
        """Set the basic features for the main window"""

        wx.Frame.__init__(self, parent=parent, title="Tic Tac Toe",
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.turn = turn
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        #Menu Options
        self.menu_bar = wx.MenuBar()
        self.options = wx.Menu()
        self.new_game = self.options.Append(-1, "New Game")
        self.evt = self.Bind(wx.EVT_MENU, self.set_new_game, self.new_game)
        self.menu_bar.Append(self.options, "Options")
        self.SetMenuBar(self.menu_bar)

        self.init_gui()

    def init_gui(self):
        """Initilize Game Grid"""
        self.gsz = wx.GridSizer(3, 3, 2, 2)
        self.list_turns = [[0 for i in range(3)] for j in range(3)]
        self.dict_bts = {}
        self.turn = 1

        self.stext = wx.StaticText(self, label="Player 1")

        #Create the buttons and are added in a dcitionary.
        for i in range(9):
            _y = i%3
            _x = i//3
            self.dict_bts[i] = TTTButton(self, pos=(_x, _y))
            self.gsz.Add(self.dict_bts[i])

        #Add widgets to box sizer.
        self.vbox.AddMany([(self.stext, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 5),
                           (self.gsz, 0, wx.ALL, 5)])
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.Layout()

    def next_move(self, val, i, j):
        """
        Update list of player's move.
        It changes the default value (0) to one of the self.turn values (1 or 2).
        It's replaced in a 2D-array (3x3) filled with zeros but it's done by the
        position of the button which is got by (i, j).

        It verifies if there is a winner and when all possible plays are done a draw
        is set
        """

        turns = [1, 2]
        self.list_turns[i][j] = val
        if self.view_winner():
            res = f"Player {self.turn} wins.".center(40, " ")
            ask = "Would you like to start a new game?".center(40, " ")
            msg = res + "\n" + ask
            dial = wx.MessageDialog(self, message=msg, caption="Result",
                                    style=wx.ICON_NONE | wx.YES_NO)
            res = dial.ShowModal()
            if res == 5103:
                self.set_new_game(self.evt)

        else:
            new_turn = list(filter(lambda x: x != val, turns))[0]
            self.turn = new_turn
            self.stext.SetLabel(f"Player {self.turn}")

            for line in self.list_turns:
                if 0 in line:
                    return None

            res = "It's a draw.".center(40, " ")
            ask = "Would you like to start a new game?".center(40, " ")
            msg = res + "\n" + ask
            dial = wx.MessageDialog(self, message=msg, caption="Result",
                                    style=wx.ICON_NONE | wx.YES_NO)
            res = dial.ShowModal()
            if res == 5103:
                self.set_new_game(self.evt)

    @staticmethod
    def is_unique(arr):
        """Evaluates  whether the array (arr) has only one value (1 or 2)."""
        unique_val = list(set(arr))
        if len(unique_val) == 1 and unique_val[0] != 0:
            return True
        return False

    def view_winner(self):
        """Verify if there is a winner"""
        dig_arr = []
        dig_inv = []

        for i in range(3):
            ver_arr = []
            hor_arr = list(set(self.list_turns[i]))
            dig_arr.append(self.list_turns[i][i])
            dig_inv.append(self.list_turns[-i-1][i])

            for j in range(3):
                ver_arr.append(self.list_turns[j][i])

            if self.is_unique(hor_arr) or self.is_unique(ver_arr):
                return True

        arr_list = [dig_arr, dig_inv]
        cond = list(map(self.is_unique, arr_list))
        if any(cond):
            return True

    def set_new_game(self, event):
        """Set a new game. Delete all the buttons and is intiliazed a new game."""
        while self.vbox.GetChildren():
            self.vbox.Hide(0)
            self.vbox.Remove(0)
        self.init_gui()
        return event

class TTTButton(wx.Button):
    """This class makes the button features"""

    def __init__(self, parent, pos):
        """Basic features of the button"""
        wx.Button.__init__(self, parent, size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.click_btn, self)
        self.pos = pos

    def click_btn(self, event):
        """Event when button is clicked.
        It sets button image (axe or circle)"""

        parent = self.GetParent()

        if self.GetBitmap() or parent.view_winner():
            return event

        if parent.turn == 1:
            bmp = wx.Bitmap("images/exs.png")
            self.SetBitmapLabel(bmp)
            parent.next_move(1, self.pos[0], self.pos[1])

        elif parent.turn == 2:
            bmp = wx.Bitmap("images/circle.png")
            self.SetBitmapLabel(bmp)
            parent.next_move(2, self.pos[0], self.pos[1])

def main():
    """Function to start the game"""

    my_app = wx.App()
    my_frame = Programme(None)
    my_frame.Show()
    my_app.MainLoop()

if __name__ == "__main__":
    main()
