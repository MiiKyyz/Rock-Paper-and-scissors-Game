from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
import random
import sqlite3
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.menu import MDDropdownMenu
import datetime
from kivymd.icon_definitions import md_icons
from kivymd.uix.snackbar import Snackbar


class Panel(MDBoxLayout):
    pass

class CustomSnackbar(Snackbar):
    icon = StringProperty(None)


class Main_Page(Widget):

    icons = []
    time = 0
    balls_pos = []
    balls_color = []
    NUM_BALL_SNOW = 50



    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for i in md_icons:

            self.icons.append(i)

        self.balls()
        self.anim(None)
        Clock.schedule_interval(self.anim, 5)




        items = [
            {
                "text" : f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.box(x),

            } for i in self.label_menu
        ]


        self.menu = MDDropdownMenu(
            caller = self.ids.select,
            items = items,
            width_mult = 4,
        )

    def balls(self):
        for i in range(self.NUM_BALL_SNOW):
            X = random.randint(0,1500)
            Y =  random.randint(0,800)

            with self.ids.main.canvas.before:
                self.color = Color(3/255, 252/255, 94/255, 1)  # set the colour

                # Seting the size and position of canvas
                self.rect = RoundedRectangle(pos=(X, Y),
                                      size=(50,
                                            50), radius=[50])
                self.balls_pos.append(self.rect)
                self.balls_color.append(self.color)



    def anim(self,k):



        for i in self.balls_pos:
            X = random.randint(0, 1500)
            Y = random.randint(0, 800)
            balls_pos = Animation(pos=(X, Y), duration=5)
            balls_pos.start(i)




        for i in self.balls_color:
            R = random.randint(0, 255)
            G = random.randint(0, 255)
            B = random.randint(0, 255)
            balls_color = Animation(rgb=(R/255, G/255, B/255, 1), duration=5)
            balls_color.start(i)

    def remove_list(self):




        self.ids.Players_Name.text = ''
        self.ids.list_of_players.clear_widgets()

    def show_list(self):

        if self.ids.screen_manager.current_screen == self.ids.screen_manager.get_screen('stats'):
            print("you are here")
        else:


            connect = sqlite3.connect("Player_date.db")

            cursor = connect.cursor()

            cursor.execute("SELECT * FROM Player")

            record = cursor.fetchall()



            for i in record:


                self.new_list_panel = ThreeLineAvatarIconListItem(text=f"name: {i[0]}",
                                                             secondary_text=f"rounds won:{i[1]}, games won:{i[2]} ",
                                                             tertiary_text=f"Account Created on: {i[3]}")

                self.new_list_panel.add_widget(IconLeftWidget(icon=f"{self.icons[random.randint(0, len(self.icons))]}"))

                self.ids.list_of_players.add_widget(self.new_list_panel)



    def open_navigator(self):
        if self.ids.screen_manager.current_screen == self.ids.screen_manager.get_screen('game'):
            CustomSnackbar(text="Needs to log out first", snackbar_x="10dp",
                           snackbar_y="10dp",
                           size_hint_x=.9, bg_color=(46 / 255, 12 / 255, 171 / 255, 1), icon="information", duration=1

                           ).open()
        else:

            self.ids.navigator.set_state("open")


    def dialog_box(self):

        if self.ids.screen_manager.current_screen == self.ids.screen_manager.get_screen('game'):
            self.dialog = MDDialog(
                text=f"Log our from User {self.ids.Name_of_player.text}",
                buttons=[
                    MDRectangleFlatIconButton(
                        text="Log out",
                        icon="logout",
                        text_color=(5 / 255, 66 / 255, 33 / 255, 1),
                        on_release=self.logout
                    ),
                    MDRectangleFlatIconButton(
                        text="Cancel",
                        icon="account-cancel",
                        text_color=(5 / 255, 66 / 255, 33 / 255, 1),
                        on_release=self.Cancel
                    )
                ]
            )
            self.dialog.open()
    def logout(self,m):
        self.dialog.dismiss()
        self.screen_manager.current = 'login'
        self.ids.Name_of_player.text = "Name"
        self.ids.Players_Name.text = ''
        self.ids.score.text = '0'
        self.ids.opponent_score.text = '0'

        CustomSnackbar(text="Logged out", snackbar_x="10dp",
                       snackbar_y="10dp",
                       size_hint_x=.9, bg_color=(46 / 255, 12 / 255, 171 / 255, 1), icon="information", duration=1

                       ).open()

    def Cancel(self,m):
        self.dialog.dismiss()
    def box(self, texto):
        self.menu.dismiss()
        self.ids.select.text = f'{texto}'


    def start_to_play(self):

        if self.ids.Players_Name.text == "":

            CustomSnackbar(text="Type a Name", snackbar_x="10dp",
                           snackbar_y="10dp",
                           size_hint_x=.9, bg_color=(46/255, 12/255, 171/255, 1), icon="information", duration=1

                           ).open()




        else:

            CustomSnackbar(text="Logged in, Welcome Back!", snackbar_x="10dp",
                           snackbar_y="10dp",
                           size_hint_x=.9, bg_color=(46 / 255, 12 / 255, 171 / 255, 1), icon="information", duration=1

                           ).open()

            connect = sqlite3.connect("Player_date.db")

            cursor = connect.cursor()

            cursor.execute("SELECT * FROM Player")
            record = cursor.fetchall()
            new_record = []

            for i in record:
                new_record.append(i[0])

            #print(new_record)
            #if self.ids.Players_Name.text in new_record:
                #print("the user is registered")
                #print(record)

            else:


                cursor.execute("INSERT INTO Player VALUES (:name, :round, :game, :date)", {"name":self.ids.Players_Name.text, "round": 0, "game": 0, "date":datetime.datetime.now()})
                #print("new user registered")

                CustomSnackbar(text="Account Created, Welcome!", snackbar_x="10dp",
                               snackbar_y="10dp",
                               size_hint_x=.9, bg_color=(46 / 255, 12 / 255, 171 / 255, 1), icon="information",
                               duration=1

                               ).open()




            connect.commit()
            connect.close()

            self.ids.screen_manager.current = 'game'
            self.ids.Name_of_player.text = self.ids.Players_Name.text

    duration_animation = 0.8 #*18
    animation_state = 'non-process'
    label_text = ['Rock', 'Paper', 'Scissor', 'Shoot!']
    label_menu = ['Rock', 'Paper', 'Scissor']
    right_hand = ['right_rock.png','right_paper.png','right_scissor.png']
    left_hand = ['left_rock.png','left_paper.png','left_scissor.png']
    counter= 0
    player_score = 0
    opponent_score = 0



    def animation_done(self, k):



        self.animation_state = 'non-process'
        self.counter = 0

        left_hand_shot = random.randint(0,2)

        self.ids.left_hand.source= self.left_hand[left_hand_shot]



        if self.ids.select.text == "Rock":
            self.ids.right_hand.source = f'{self.right_hand[0]}'
        elif self.ids.select.text == "Paper":
            self.ids.right_hand.source = f'{self.right_hand[1]}'

        elif self.ids.select.text == "Scissor":
            self.ids.right_hand.source = f'{self.right_hand[2]}'



        animation_title = Animation(font_size=60, duration=self.duration_animation+3, opacity=1)
        animation_title += Animation(font_size=0, duration=self.duration_animation, opacity=0)



        if self.ids.right_hand.source == 'right_rock.png' and self.ids.left_hand.source == "left_scissor.png":

            self.ids.label2.text = "you win"
            animation_title.start(self.ids.label2)
            #print("you win")
            self.player_score +=1
            self.ids.score.text = f'{self.player_score}'

            connect = sqlite3.connect("Player_date.db")

            cursor = connect.cursor()
            #print("score", self.player_score)

            cursor.execute("SELECT Rounds FROM Player")

            record_1 = cursor.fetchall()
            new_score_1 = 0
            for i in record_1:

                new_score_1 = i[0]

            new_score_1 += 1
            cursor.execute(f"UPDATE Player SET Rounds={new_score_1} WHERE Name='{self.ids.Name_of_player.text}'")

            connect.commit()
            connect.close()

        elif self.ids.left_hand.source == 'left_rock.png' and self.ids.right_hand.source == "right_scissor.png":
            self.ids.label2.text = "you lost"
            animation_title.start(self.ids.label2)
            #print("you lost")

            self.opponent_score += 1
            self.ids.opponent_score.text = f'{self.opponent_score}'

        elif self.ids.left_hand.source == 'left_paper.png' and self.ids.right_hand.source == 'right_rock.png':
            self.ids.label2.text = 'you lost'
            animation_title.start(self.ids.label2)
            #print('you lost')

            self.opponent_score += 1
            self.ids.opponent_score.text = f'{self.opponent_score}'




        elif self.ids.left_hand.source == 'left_rock.png' and self.ids.right_hand.source == 'right_paper.png':
            self.ids.label2.text = "you win"
            animation_title.start(self.ids.label2)
            #print("you win")
            self.player_score += 1
            self.ids.score.text = f'{self.player_score}'

            connect = sqlite3.connect("Player_date.db")

            cursor = connect.cursor()


            cursor.execute("SELECT Rounds FROM Player")

            record_2 = cursor.fetchall()
            new_score_2 = 0
            for i in record_2:

                new_score_2 = i[0]

            new_score_2 += 1
            cursor.execute(f"UPDATE Player SET Rounds={new_score_2} WHERE Name='{self.ids.Name_of_player.text}'")



            connect.commit()
            connect.close()

        elif self.ids.left_hand.source == 'left_scissor.png' and self.ids.right_hand.source == 'right_paper.png':

            self.ids.label2.text = 'you lost'
            animation_title.start(self.ids.label2)
            #print('you lost')

            self.opponent_score += 1
            self.ids.opponent_score.text = f'{self.opponent_score}'





        elif self.ids.left_hand.source == 'left_paper.png' and self.ids.right_hand.source == 'right_scissor.png':


            self.ids.label2.text = "you win"
            animation_title.start(self.ids.label2)
            #print("you win")
            self.player_score += 1
            self.ids.score.text = f'{self.player_score}'

            connect = sqlite3.connect("Player_date.db")

            cursor = connect.cursor()
            #print("score", self.player_score)

            cursor.execute("SELECT Rounds FROM Player")

            record_3 = cursor.fetchall()
            new_score_3 = 0
            for i in record_3:

                new_score_3 = i[0]

            new_score_3 += 1
            cursor.execute(f"UPDATE Player SET Rounds={new_score_3} WHERE Name='{self.ids.Name_of_player.text}'")

            connect.commit()
            connect.close()


        elif self.ids.left_hand.source == 'left_rock.png' and self.ids.right_hand.source == 'right_rock.png':

            self.ids.label2.text = "TIE!"
            animation_title.start(self.ids.label2)


        elif self.ids.left_hand.source == 'left_paper.png' and self.ids.right_hand.source == 'right_paper.png':
            self.ids.label2.text = "TIE!"
            animation_title.start(self.ids.label2)


        elif self.ids.left_hand.source == 'left_scissor.png' and self.ids.right_hand.source == 'right_scissor.png':
            self.ids.label2.text = "TIE!"
            animation_title.start(self.ids.label2)


        if self.player_score == 3:

            self.ids.label2.text = "you win the game"
            animation_title.start(self.ids.label2)

            self.opponent_score = 0
            self.player_score = 0
            self.ids.score.text = f'0'
            self.ids.opponent_score.text = f'0'

            connect = sqlite3.connect("Player_date.db")

            cursor = connect.cursor()

            cursor.execute("SELECT Games FROM Player")

            record = cursor.fetchall()
            new_game_score = 0
            for i in record:
                new_game_score = i[0]

            new_game_score += 1
            cursor.execute(f"UPDATE Player SET Games={new_game_score} WHERE Name='{self.ids.Name_of_player.text}'")



            connect.commit()
            connect.close()

        elif self.opponent_score == 3:

            self.ids.label2.text = "you lost the game"
            animation_title.start(self.ids.label2)

            self.opponent_score = 0
            self.player_score = 0
            self.ids.score.text = f'0'
            self.ids.opponent_score.text = f'0'




    def change_label(self, k):

        self.ids.label.text = self.label_text[self.counter]
        self.counter += 1



    def shoot(self):
        if self.animation_state == "animation-in-progress":
            pass
        else:

            Clock.schedule_once(self.animation_done, 5.6)

            Clock.schedule_once(self.change_label, 0)
            Clock.schedule_once(self.change_label, 1.6)
            Clock.schedule_once(self.change_label, 3.2)
            Clock.schedule_once(self.change_label, 4.8)

            self.ids.right_hand.source = f'{self.right_hand[0]}'
            self.ids.left_hand.source = f'{self.left_hand[0]}'

            self.animation_state = "animation-in-progress"
            anim_left = Animation(pos_hint= {'center_y': 0.4, 'center_x': 0.09}, duration=self.duration_animation)
            anim_left += Animation( pos_hint= {'center_y': 0.5, 'center_x': 0.09}, duration=self.duration_animation)


            anim_left += Animation(pos_hint={'center_y': 0.4, 'center_x': 0.09}, duration=self.duration_animation)
            anim_left += Animation(pos_hint={'center_y': 0.5, 'center_x': 0.09}, duration=self.duration_animation)

            anim_left += Animation(pos_hint={'center_y': 0.4, 'center_x': 0.09}, duration=self.duration_animation)
            anim_left += Animation(pos_hint={'center_y': 0.5, 'center_x': 0.09}, duration=self.duration_animation)

            anim_left += Animation(pos_hint={'center_y': 0.4, 'center_x': 0.09}, duration=self.duration_animation)
            anim_left += Animation(pos_hint={'center_y': 0.5, 'center_x': 0.09}, duration=self.duration_animation)

            anim_left.start(self.ids.left_hand)

            anim_right = Animation(pos_hint= {'center_x': 0.91, 'center_y':0.4}, duration=self.duration_animation)
            anim_right += Animation(pos_hint={'center_x': 0.91, 'center_y': 0.5}, duration=self.duration_animation)

            anim_right += Animation(pos_hint={'center_x': 0.91, 'center_y': 0.4}, duration=self.duration_animation)
            anim_right += Animation(pos_hint={'center_x': 0.91, 'center_y': 0.5}, duration=self.duration_animation)

            anim_right += Animation(pos_hint={'center_x': 0.91, 'center_y': 0.4}, duration=self.duration_animation)
            anim_right += Animation(pos_hint={'center_x': 0.91, 'center_y': 0.5}, duration=self.duration_animation)

            anim_right += Animation(pos_hint={'center_x': 0.91, 'center_y': 0.4}, duration=self.duration_animation)
            anim_right += Animation(pos_hint={'center_x': 0.91, 'center_y': 0.5}, duration=self.duration_animation)

            anim_right.start(self.ids.right_hand)

            anim_label = Animation(font_size= 100,opacity=1 , duration=self.duration_animation)
            anim_label += Animation(font_size= 0,opacity=0, duration=self.duration_animation)

            anim_label += Animation(font_size=100,opacity=1, duration=self.duration_animation)
            anim_label += Animation(font_size=0,opacity=0, duration=self.duration_animation)

            anim_label += Animation(font_size=100,opacity=1, duration=self.duration_animation)
            anim_label += Animation(font_size=0,opacity=0, duration=self.duration_animation)

            anim_label += Animation(font_size=100,opacity=1, duration=self.duration_animation)
            anim_label += Animation(font_size=0,opacity=0, duration=self.duration_animation)

            anim_label.start(self.ids.label)




class game(MDApp):


    def build(self):

        return Main_Page()


    def on_start(self):

        connect_database = sqlite3.connect("Player_date.db")

        cursor = connect_database.cursor()

        cursor.execute(""" CREATE TABLE IF NOT EXISTS Player 
        (Name text, Rounds int, Games int, Registration int)""")

        connect_database.commit()
        connect_database.close()

if __name__ == '__main__':
    game().run()

