from kivy import Config
#Config.set('graphics', 'multisamples', '0')
#Config.set('graphics', 'fullscreen', 'auto')
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

# main.py
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.properties import StringProperty
from kivymd.toast import toast
from plyer import filechooser
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.icon_definitions import md_icons
from kivymd.uix.textfield import MDTextField
from kivy.utils import platform
import webbrowser as wb
from kivymd.uix.label import MDLabel
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.app import App
import errno
import requests
import socket
import math

from itertools import combinations_with_replacement

try:
    import data.invoice as inv
except Exception:
    pass

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def check_file_exists(filename, content, create_new):
    if create_new:
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write(content)
        else:
            with open(filename, "r+") as f:
                if f.read() == "":
                    f.write(content)
    else:
        if not os.path.exists(filename):
            raise Exception


def get_asset_path(file_name):
    return file_name

def get_downloads_path():
    return os.path.join(os.path.expanduser('~'), 'Desktop')

create_directory_if_not_exists("assets")
create_directory_if_not_exists("data")
SETTINGSFILE = get_asset_path("data/settings.txt")
QUOTATIONFILE = get_asset_path("data/quotation.txt")
LOGOFILE = get_asset_path("assets/icon.png")

check_file_exists(SETTINGSFILE, "[400, {'11':3, '12':2.5, '13':2.3, '14':2, '16':1.5, '18':1.2, '20':1, '22':0.8, '23':0.7, '24':0.6, '26':0.55, '28':0.5}, {'14':250, '16': 200, '18': 180, '20': 160, '22':150}, 2500, [45, 39, 36, 30], {'Medium Duty':1300, 'Heavy Duty':1500}]", True)
check_file_exists(QUOTATIONFILE, f"['QUOTATION', '1', 'https://danishbrothers.com.pk/wp-content/uploads/2024/01/Picsart-24-01-08-19-11-31-574-scaled.jpg', 'Your_Name Number', 'Walkin_Name Number', 'Karachi', 'Cash/Cheque', 'Thanks for your bussiness!', '> 70 % DOWNPAYMENT ON ORDER.~> 30 % AT THE TIME OF COMPLETION~> ABOVE PRICES ARE VALID FOR 07 DAYS ONLY~> ELECTRICITY/WATER REQUIRE FOR INSTALLATION SHALL BE PROVIDED BY COSTUMER~> ANY OTHER TERMS NOT LISTED WILL BE MUTUALLY DECIDED~We assure you of our best services and quality products in all the time. In meanwhile if you may require any additional information, clarification, kindly feel free to contact us. We will remain at your full disposal. Awaiting for your esteemed Reply', r'{str(get_downloads_path())}']", True)

class BackgroundFloatLayout(BoxLayout):
    BACKGROUNDPATH = StringProperty("")
    BACKGROUNDPATH = get_asset_path("assets/background.jpg")

class HomeScreen(Screen, BackgroundFloatLayout):
    LOGOPATH = StringProperty("")
    LOGOPATH = get_asset_path("assets/logo.png")
    def goto_main(self):
        self.manager.current = 'main'
    def goto_pallet(self):
        self.manager.current = 'pallet'
    def goto_wallshelving(self):
        self.manager.current = 'wallshelving'
    def goto_settings(self):
        self.manager.current = 'settings'
    def goto_quotation(self):
        self.manager.current = 'quotation'

class SettingsScreen(Screen, BackgroundFloatLayout):
    # Kivy properties to store text from the file
    text_field1 = StringProperty("")
    text_field2 = StringProperty("")
    text_field3 = StringProperty("")
    text_field4 = StringProperty("")
    text_field5 = StringProperty("")
    text_field6 = StringProperty("")

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.load_settings_from_file()

    def show_info_popup(self):
        dialog = MDDialog(
                title="Settings - Info",
                text="Important! Make sure to only change numbers and not mixup or remove odd brackets or other any symbols as it may result in calculation errors.\n-\nIf incase settings have gotten messed up, just click on the reset button and you are good to go.",
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=lambda *args: dialog.dismiss()
                    )
                ],
            )
        dialog.open()

    def load_settings_from_file(self):
        # Read content from the text file and update properties
        try:
            with open(SETTINGSFILE, "r") as file:
                lines = eval(file.read())
                self.text_field1 = str(lines[0])
                self.text_field2 = str(lines[1])
                self.text_field3 = str(lines[2])
                self.text_field4 = str(lines[3])
                self.text_field5 = str(lines[4])
                self.text_field6 = str(lines[5])
        except Exception as e:
            dialog = MDDialog(
                title="Error",
                text=f"There was an error loading file. Error Details: {e}",
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=lambda *args: dialog.dismiss()
                    )
                ],
            )
            dialog.open()

    def save_settings_to_file(self):
        # Save content to the text file
        settings_metal_rates = str(self.ids.settings_metal_rates.text)
        settings_shelf_guage = str(self.ids.settings_shelf_guage.text)
        settings_angle_guage = str(self.ids.settings_angle_guage.text)
        settings_labour_rates = str(self.ids.settings_labour_cost.text)
        settings_standard_wallracksizes = str(self.ids.settings_standard_wallracksizes.text)
        settings_pallet_rates = str(self.ids.pallet_rates.text)
        file = open(SETTINGSFILE, "w")
        file.write(f"[{settings_metal_rates}, {settings_shelf_guage}, {settings_angle_guage}, {settings_labour_rates}, {settings_standard_wallracksizes}, {settings_pallet_rates}]")
        toast(
        text="Saved",
        duration=3,  # seconds
        )
        file.close()

    def reset_settings_from_file(self):
        file = open(SETTINGSFILE, "w")
        file.write("[400, {'11':3, '12':2.5, '13':2.3, '14':2, '16':1.5, '18':1.2, '20':1, '22':0.8, '23':0.7, '24':0.6, '26':0.55, '28':0.5}, {'14':250, '16': 200, '18': 180, '20': 160, '22':150}, 2500, [45, 39, 36, 30], {'Medium Duty':1300, 'Heavy Duty':1500}]")
        self.ids.settings_metal_rates.text = '400'
        self.ids.settings_shelf_guage.text = "{'11':3, '12':2.5, '13':2.3, '14':2, '16':1.5, '18':1.2, '20':1, '22':0.8, '23':0.7, '24':0.6, '26':0.55, '28':0.5}"
        self.ids.settings_angle_guage.text = "{'14':250, '16': 200, '18': 180, '20': 160, '22':150}"
        self.ids.settings_labour_cost.text = "2500"
        self.ids.settings_standard_wallracksizes.text = "[45, 39, 36, 30]"
        self.ids.pallet_rates.text = "{'Medium Duty':1300, 'Heavy Duty':1500}"
        toast(
        text="Settings Reseted",
        duration=3,  # seconds
        )
        file.close()

    def go_back(self):
        self.manager.current = 'home'
    def on_scroll_y(self, instance, value):
        self.scroll_position = value

class QuotationScreen(Screen, BackgroundFloatLayout):
    # Kivy properties to store text from the file
    text_field1 = StringProperty("")
    text_field2 = StringProperty("")
    text_field3 = StringProperty("")
    text_field4 = StringProperty("")
    text_field5 = StringProperty("")
    text_field6 = StringProperty("")
    text_field7 = StringProperty("")
    text_field8 = StringProperty("")
    text_field9 = StringProperty("")
    text_field10 = StringProperty("")

    def __init__(self, **kwargs):
        super(QuotationScreen, self).__init__(**kwargs)
        self.load_settings_from_file()

    def show_info_popup(self):
        dialog = MDDialog(
                title="Quotation - Info",
                text="Important! Make sure to only change values like they are written by default and not mixup or remove any other symbols as it may result in pdf errors.\n-\nIf incase settings have gotten messed up, just click on the reset button and you are good to go.",
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=lambda *args: dialog.dismiss()
                    )
                ],
            )
        dialog.open()

    def load_settings_from_file(self):
        # Read content from the text file and update properties
        try:
            with open(QUOTATIONFILE, "r") as file:
                lines = eval(file.read())
                self.text_field1 = str(lines[0])
                self.text_field2 = str(lines[1])
                self.text_field3 = str(lines[2])
                self.text_field4 = str(lines[3])
                self.text_field5 = str(lines[4])
                self.text_field6 = str(lines[5])
                self.text_field7 = str(lines[6])
                self.text_field8 = str(lines[7])
                self.text_field9 = str(lines[8])
                self.text_field10 = str(lines[9])
        except Exception as e:
            dialog = MDDialog(
                title="Error",
                text=f"There was an error loading file. Error Details: {e}",
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=lambda *args: dialog.dismiss()
                    )
                ],
            )
            dialog.open()

    def change_path(self):
        selected_file = filechooser.choose_dir(title="Select Folder")
        if selected_file:
            self.ids.Download_Location_Android.text = selected_file[0]
        else:
            toast(
            text="Please choose a valid folder!",
            duration=3,  # seconds
            )
        

    def save_settings_to_file(self):
        # Save content to the text file
        quotation_header = str(self.ids.Quotaton_Header.text)
        quotation_number = str(self.ids.Quotation_Number.text)
        quotation_logo = str(self.ids.Quotation_Logo.text)
        quotation_owner = str(self.ids.Quotation_Owner.text)
        quotation_costumer = str(self.ids.Quotation_Costumer.text)
        quotation_shipping = str(self.ids.Quotation_Shipping.text)
        quotation_payment = str(self.ids.Quotation_Payment.text)
        quotation_notes = str(self.ids.Quotation_Notes.text)
        quotation_terms = str(self.ids.Quotation_Terms.text)
        download_location = str(self.ids.Download_Location_Android.text)
        file = open(QUOTATIONFILE, "w")
        file.write(f"['{quotation_header}', '{quotation_number}', '{quotation_logo}', '{quotation_owner.split()[0]} {quotation_owner.split()[1]}', '{quotation_costumer.split()[0]} {quotation_costumer.split()[1]}', '{quotation_shipping}', '{quotation_payment}', '{quotation_notes}', '{quotation_terms}', r'{download_location}']")
        toast(
        text="Saved",
        duration=3,  # seconds
        )
        file.close()

    def get_downloads_path(self):
        return os.path.join(os.path.expanduser('~'), 'Desktop')

    def reset_settings_from_file(self):
        file = open(QUOTATIONFILE, "w")
        file.write(f"['QUOTATION', '1', 'https://danishbrothers.com.pk/wp-content/uploads/2024/01/Picsart-24-01-08-19-11-31-574-scaled.jpg', 'Your_Name Number', 'Walkin_Name Number', 'Karachi', 'Cash/Cheque', 'Thanks for your bussiness!', '> 70 % DOWNPAYMENT ON ORDER.~> 30 % AT THE TIME OF COMPLETION~> ABOVE PRICES ARE VALID FOR 07 DAYS ONLY~> ELECTRICITY/WATER REQUIRE FOR INSTALLATION SHALL BE PROVIDED BY COSTUMER~> ANY OTHER TERMS NOT LISTED WILL BE MUTUALLY DECIDED~We assure you of our best services and quality products in all the time. In meanwhile if you may require any additional information, clarification, kindly feel free to contact us. We will remain at your full disposal. Awaiting for your esteemed Reply', r'{self.get_downloads_path()}']")
        self.ids.Quotaton_Header.text = "QUOTATION"
        self.ids.Quotation_Number.text = "1"
        self.ids.Quotation_Logo.text = 'https://danishbrothers.com.pk/wp-content/uploads/2024/01/Picsart-24-01-08-19-11-31-574-scaled.jpg'
        self.ids.Quotation_Owner.text = 'Your_Name Number'
        self.ids.Quotation_Costumer.text = "Walkin_Name Number"
        self.ids.Quotation_Shipping.text = "Karachi"
        self.ids.Quotation_Payment.text = "Cash/Cheque"
        self.ids.Quotation_Notes.text = 'Thanks for your bussiness!'
        self.ids.Quotation_Terms.text = '> 70 % DOWNPAYMENT ON ORDER.~> 30 % AT THE TIME OF COMPLETION~> ABOVE PRICES ARE VALID FOR 07 DAYS ONLY~> ELECTRICITY/WATER REQUIRE FOR INSTALLATION SHALL BE PROVIDED BY COSTUMER~> ANY OTHER TERMS NOT LISTED WILL BE MUTUALLY DECIDED~We assure you of our best services and quality products in all the time. In meanwhile if you may require any additional information, clarification, kindly feel free to contact us. We will remain at your full disposal. Awaiting for your esteemed Reply'
        self.ids.Download_Location_Android.text = self.get_downloads_path()
        toast(
        text="Quotation Reseted",
        duration=3,  # seconds
        )
        file.close()

    def go_back(self):
        self.manager.current = 'home'
    def on_scroll_y(self, instance, value):
        self.scroll_position = value

class MainScreen(Screen, BackgroundFloatLayout):
    def goto_home(self):
        self.manager.current = 'home'
    def on_scroll_y(self, instance, value):
        self.scroll_position = value

    def show_calculated_popup(self, popupd=True):
        global shelf_length_value
        global shelf_width_value
        global shelf_number_value
        global shelf_gauge_value
        global angle_guage_value
        global per_shelf
        global angle_height_value
        global per_angle
        global labour_rates
        global rack_quantity
        try:
            settingsFile = open(SETTINGSFILE, 'r+')
            settings_content = eval(settingsFile.read())
            guagelistshelf = settings_content[1]
            guagelistAngle = settings_content[2]
            metal_rates = settings_content[0]
            labour_rates = settings_content[3]
            shelf_length_value = float(self.ids.Shelf_Length.text)
            shelf_width_value = float(self.ids.Shelf_Width.text)
            shelf_gauge_value = str(self.ids.Shelf_Guage.text)
            shelf_number_value = float(self.ids.Shelf_Number.text)
            angle_height_value = float(self.ids.Angle_Height.text)
            angle_guage_value = str(self.ids.Angle_Guage.text)
            rack_quantity = int(self.ids.rack_quantity.text)
            per_shelf = (((((shelf_length_value+3)*(shelf_width_value+3))/144)*0.729)*guagelistshelf[shelf_gauge_value])*int(metal_rates)
            total_shelfs = (per_shelf*shelf_number_value)
            per_angle = guagelistAngle[angle_guage_value]*angle_height_value
            total_angles = (per_angle*4)
            total_rack = (total_shelfs+total_angles+int(labour_rates))
            settingsFile.close()
            perifmorerack = "" if rack_quantity == 1 else f"\nCost of {rack_quantity} Racks: Rs.{round(total_rack)*rack_quantity}"
            perifmoreshelf = "" if rack_quantity == 1 else f"\n-------------------------------\nCost Total Shelfs for {rack_quantity} Racks: Rs.{round(total_shelfs*rack_quantity)}"
            perifmoreangle = "" if rack_quantity == 1 else f"\nCost Total Angles for {rack_quantity} Racks: Rs.{round(total_angles*rack_quantity)}"
            prc = f"Cost Per Shelf: Rs.{round(per_shelf)}\nCost Per Angle: Rs.{round(per_angle)}\nCost Total Shelfs for 1 Rack: Rs.{round(total_shelfs)}\nCost Total Angles for 1 Rack: Rs.{round(total_angles)}{perifmoreshelf}{perifmoreangle}\n-------------------------------\nCost of 1 Rack: Rs.{round(total_rack)}{perifmorerack}"
            dialog = MDDialog(
                title="Successfully Calculated",
                text=prc,
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=lambda *args: dialog.dismiss()
                    )
                ],
            )
        except Exception as e:
            dialog = MDDialog(
                title="Error",
                text=f"There was an error while calculating results. Error Details: {e}",
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=lambda *args: dialog.dismiss()
                    )
                ],
            )
        finally:
            if popupd:
                dialog.open()

    def show_savepdf_popup(self):
        # content = MDTextField(
        #     multiline=False,
        #     hint_text="Enter Costumer Name",
        #     size_hint=(None, None),
        #     width=200,
        # )
        
        file = open(QUOTATIONFILE, "r")
        lines = eval(file.read())
        text_field1 = str(lines[0])
        dialog = MDDialog(
            title="Foresupport PDF Downloader",
            text=f"Do you want to download {text_field1.capitalize()} for this rack?",
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    theme_text_color= 'Custom',
                    text_color= (1, 1, 1, 1),
                    md_bg_color= (0, 0, 0, 1),
                    on_release=lambda *args: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="OK",
                    theme_text_color= 'Custom',
                    text_color= (1, 1, 1, 1),
                    md_bg_color= (0, 0, 0, 1),
                    on_release=lambda *args: self.process_input(dialog)
                ),
            ],
        )
        dialog.open()
        file.close()

    def process_input(self, dialog):
        self.show_calculated_popup(popupd=False)
        file = open(QUOTATIONFILE, "r")
        lines = eval(file.read())
        text_field1 = str(lines[0])
        text_field2 = str(lines[1])
        text_field3 = str(lines[2])
        text_field4 = (((str(lines[3]).split())[0]).replace("_", " ") if "_" in (str(lines[3]).split())[0] else (str(lines[3]).split())[0])+"\n"+(str(lines[3]).split())[1]
        text_field5 = (((str(lines[4]).split())[0]).replace("_", " ") if "_" in (str(lines[4]).split())[0] else (str(lines[4]).split())[0])+"\n"+(str(lines[4]).split())[1]
        text_field6 = str(lines[5])
        text_field7 = str(lines[6])
        text_field8 = str(lines[7])
        text_field9 = str(lines[8])
        text_field10 = str(lines[9])
        text_field9_edited = text_field9.replace("~", "\n")
        file.close()
        invoice = inv.InvoiceGenerator(
        # logo="https://danishbrothers.com.pk/wp-content/uploads/2023/12/Picsart_23-12-09_12-53-31-929.png",
        header=text_field1,
        number=text_field2,
        logo=text_field3,
        sender=text_field4,
        to=text_field5,
        ship_to=text_field6,
        payments_terms=text_field7,
        notes=f"> Rates are subject to {rack_quantity} Racks.\n{text_field8}",
        terms=text_field9_edited
        )

        invoice.add_item(
            name=f"Shelf ({shelf_gauge_value} guage)\n{shelf_width_value}\"x{shelf_length_value}\"",
            quantity=int(shelf_number_value)*rack_quantity,
            unit_cost=int(per_shelf),
        )
        invoice.add_item(
            name=f"Angle ({angle_guage_value} guage)\n{angle_height_value}\'",
            quantity=4*rack_quantity,
            unit_cost=int(per_angle),
        )
        invoice.add_item(
            name=f"Labour, Nut, Bolts, Corners, etc",
            quantity=1*rack_quantity,
            unit_cost=int(labour_rates),
        )

        invoice.toggle_subtotal(shipping=False, tax=False)

        try:
            invoice.download(f"{text_field10}\{text_field1.capitalize()}{text_field2}.pdf")
            file = open(QUOTATIONFILE, "w")
            file.write(f"['{text_field1}', '{str(int(text_field2)+1)}', '{text_field3}', '{(str(lines[3]).split())[0]} {(str(lines[3]).split())[1]}', '{(str(lines[4]).split())[0]} {(str(lines[4]).split())[1]}', '{text_field6}', '{text_field7}', '{text_field8}', '{text_field9}', r'{text_field10}']")
            dialog.dismiss()
            toast(
            text=f"{text_field1.capitalize()}{text_field2}.pdf Downloaded!",
            duration=3,  # seconds
            )
        except Exception:
            dialog.dismiss()
            toast(
            text=f"Error While Dowloading {text_field1.capitalize()}{text_field2}.pdf!",
            duration=3,  # seconds
            )
        finally:
            file.close()
            
class PalletScreen(Screen, BackgroundFloatLayout):
    def __init__(self, **kwargs):
        super(PalletScreen, self).__init__(**kwargs)
        self.add_shelf = True
    def goto_home(self):
        self.manager.current = 'home'
    def on_scroll_y(self, instance, value):
        self.scroll_position = value
        
    def toggle_button_state(self, button, text):
        if text == "Shelf - ON":
            button.text = "Shelf - OFF"
            button.md_bg_color = (1, 1, 1, 0)  # White color (RGB)
            button.text_color = (0, 0, 0, 1)  # Black text color (RGB)
            button.line_color = (0, 0, 0, 1)  # Black outline color (RGB)
            self.ids.Guage_Pallet_Shelf.readonly = True
            self.ids.Guage_Pallet_Shelf.text = "Not Required"
            self.add_shelf = False
        else:
            button.text = "Shelf - ON"
            button.md_bg_color = (0, 0, 0, 1)  # Black color (RGB)
            button.text_color = (1, 1, 1, 1)  # White text color (RGB)
            button.line_color = (0, 0, 0, 1)  # Black outline color (RGB)
            self.ids.Guage_Pallet_Shelf.readonly = False
            self.ids.Guage_Pallet_Shelf.text = ""
            self.add_shelf = True

    def highlight_button(self, button, option, text):
        # Reset button colors, text colors, and outline colors
        self.ids.medium_duty_btn.md_bg_color = [1, 1, 1, 0]
        self.ids.medium_duty_btn.text_color = [0, 0, 0, 1]
        self.ids.medium_duty_btn.line_color = [0, 0, 0, 1]

        self.ids.heavy_duty_btn.md_bg_color = [1, 1, 1, 0]
        self.ids.heavy_duty_btn.text_color = [0, 0, 0, 1]
        self.ids.heavy_duty_btn.line_color = [0, 0, 0, 1]

        # Set the pressed button to black background, white text, and black outline
        if option == 'medium_duty':
            button.md_bg_color = [0, 0, 0, 1]  # Black color
            button.text_color = [1, 1, 1, 1]  # White color
            button.line_color = [0, 0, 0, 1]  # Black color
        elif option == 'heavy_duty':
            button.md_bg_color = [0, 0, 0, 1]  # Black color
            button.text_color = [1, 1, 1, 1]  # White color
            button.line_color = [0, 0, 0, 1]  # Black color
        self.ids.pallet_type.text = text

    def show_calculated_popup(self, popupd=True):
        global SideFrameHeight
        global BeamLength
        global perSideFrame
        global shelfqtytotal
        global sideframeqty
        global beampairqty
        global pairBeam
        global per_shelf
        global rack_addons
        global RackDepth
        try:
            settingsFile = open(SETTINGSFILE, 'r+')
            settings_content = eval(settingsFile.read())
            guagelistshelf = settings_content[1]
            metal_rates = settings_content[0]
            palletrates = settings_content[5]
            labour_rates = 200
            pallettype = self.ids.pallet_type.text
            SideFrameHeight = float(self.ids.Sideframe_Height.text)
            BeamLength = float(self.ids.Beam_Length.text)
            NoOfLevels = int(self.ids.Number_of_Levels.text)
            RackDepth = int(self.ids.Pallet_Depth.text)
            rack_addons = int(self.ids.rack_addons.text)
            pallet_shelf_gauge_value = self.ids.Guage_Pallet_Shelf.text if self.add_shelf else 0
            per_shelf = (((((((RackDepth*12))*(12+3))/144)*0.729)*guagelistshelf[pallet_shelf_gauge_value])*int(metal_rates))+labour_rates if self.add_shelf else 0
            perSideFrame = SideFrameHeight*int(palletrates[pallettype])
            pairBeam = BeamLength*int(palletrates[pallettype])
            sideframeqty = 2+rack_addons
            beampairqty = NoOfLevels*(rack_addons+1)
            shelfqtyperlevel = math.floor(BeamLength) if self.add_shelf else 0
            shelfqtyperrack = shelfqtyperlevel*NoOfLevels if self.add_shelf else 0
            shelfqtytotal = shelfqtyperrack*(rack_addons+1) if self.add_shelf else 0
            StarterRackCost = (perSideFrame*2)+(pairBeam*NoOfLevels)+(shelfqtyperrack*per_shelf)
            AddonRackCost = StarterRackCost-perSideFrame
            TotalRackCost = StarterRackCost+(AddonRackCost*rack_addons)
            settingsFile.close()
            prc = f"Starter Rack: Rs.{round(StarterRackCost)}\nAddon Rack ({rack_addons}): Rs.{round(AddonRackCost)}\n" if rack_addons>0 else ""
            shelf_add_or_not = f"\nShelfs ({shelfqtytotal}): Rs.{round(shelfqtytotal*per_shelf)}" if self.add_shelf else ""
            dialog = MDDialog(
                title="Successfully Calculated",
                text=f"Sideframe ({sideframeqty}): Rs.{round(perSideFrame*sideframeqty)}\nBeam Pair ({beampairqty}): Rs.{round(pairBeam*beampairqty)}{shelf_add_or_not}\n-------------------------------\n{prc}Total Rack Cost: Rs.{round(TotalRackCost)}",
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=lambda *args: dialog.dismiss()
                    )
                ],
            )
        except Exception as e:
            dialog = MDDialog(
                title="Error",
                text=f"There was an error while calculating results. Error Details: {e}",
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=lambda *args: dialog.dismiss()
                    )
                ],
            )
        finally:
            if popupd:
                dialog.open()

    def show_savepdf_popup(self):
        # content = MDTextField(
        #     multiline=False,
        #     hint_text="Enter Costumer Name",
        #     size_hint=(None, None),
        #     width=200,
        # )
        
        file = open(QUOTATIONFILE, "r")
        lines = eval(file.read())
        text_field1 = str(lines[0])
        dialog = MDDialog(
            title="Pallet PDF Downloader",
            text=f"Do you want to download {text_field1.capitalize()} for this rack?",
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    theme_text_color= 'Custom',
                    text_color= (1, 1, 1, 1),
                    md_bg_color= (0, 0, 0, 1),
                    on_release=lambda *args: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="OK",
                    theme_text_color= 'Custom',
                    text_color= (1, 1, 1, 1),
                    md_bg_color= (0, 0, 0, 1),
                    on_release=lambda *args: self.process_input(dialog)
                ),
            ],
        )
        dialog.open()
        file.close()

    def process_input(self, dialog):
        self.show_calculated_popup(popupd=False)
        file = open(QUOTATIONFILE, "r")
        lines = eval(file.read())
        text_field1 = str(lines[0])
        text_field2 = str(lines[1])
        text_field3 = str(lines[2])
        text_field4 = (((str(lines[3]).split())[0]).replace("_", " ") if "_" in (str(lines[3]).split())[0] else (str(lines[3]).split())[0])+"\n"+(str(lines[3]).split())[1]
        text_field5 = (((str(lines[4]).split())[0]).replace("_", " ") if "_" in (str(lines[4]).split())[0] else (str(lines[4]).split())[0])+"\n"+(str(lines[4]).split())[1]
        text_field6 = str(lines[5])
        text_field7 = str(lines[6])
        text_field8 = str(lines[7])
        text_field9 = str(lines[8])
        text_field10 = str(lines[9])
        text_field9_edited = text_field9.replace("~", "\n")
        file.close()
        invoice = inv.InvoiceGenerator(
        # logo="https://danishbrothers.com.pk/wp-content/uploads/2023/12/Picsart_23-12-09_12-53-31-929.png",
        header=text_field1,
        number=text_field2,
        logo=text_field3,
        sender=text_field4,
        to=text_field5,
        ship_to=text_field6,
        payments_terms=text_field7,
        notes=f"> Rates are subject to 1 Starter & {rack_addons} Addons.\n{text_field8}",
        terms=text_field9_edited
        )

        invoice.add_item(
            name=f"Side Frame\n{SideFrameHeight}\'",
            quantity=sideframeqty,
            unit_cost=perSideFrame,
        )
        invoice.add_item(
            name=f"Beam Pair\n{BeamLength}\'",
            quantity=beampairqty,
            unit_cost=pairBeam,
        )
        if self.add_shelf:
            invoice.add_item(
                name=f"Shelf\n{(RackDepth*12)-3}\"",
                quantity=shelfqtytotal,
                unit_cost=per_shelf,
            )

        invoice.toggle_subtotal(shipping=False, tax=False)

        try:
            invoice.download(f"{text_field10}\{text_field1.capitalize()}{text_field2}.pdf")
            file = open(QUOTATIONFILE, "w")
            file.write(f"['{text_field1}', '{str(int(text_field2)+1)}', '{text_field3}', '{(str(lines[3]).split())[0]} {(str(lines[3]).split())[1]}', '{(str(lines[4]).split())[0]} {(str(lines[4]).split())[1]}', '{text_field6}', '{text_field7}', '{text_field8}', '{text_field9}', r'{text_field10}']")
            dialog.dismiss()
            toast(
            text=f"{text_field1.capitalize()}{text_field2}.pdf Downloaded!",
            duration=3,  # seconds
            )
        except Exception:
            dialog.dismiss()
            toast(
            text=f"Error While Dowloading {text_field1.capitalize()}{text_field2}.pdf!",
            duration=3,  # seconds
            )
        finally:
            file.close()
    
class WallShelvingScreen(Screen, BackgroundFloatLayout):
    def goto_home(self):
        self.manager.current = 'home'
    def on_scroll_y(self, instance, value):
        self.scroll_position = value
    def show_info_popup(self):
        dialog = MDDialog(
                title="Wall Shelving - Info",
                text="Larger sizes take longer to calculate then smaller sizes unless you have a fast computer.\n-\nRecommended: Make sure to enter sizes under the range of 5000\" for seamless and fast calculation.",
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=lambda *args: dialog.dismiss()
                    )
                ],
            )
        dialog.open()
    def tuple_to_dict(self, input_tuple):
        result_dict = {}
        for item in input_tuple:
            result_dict[item] = result_dict.get(item, 0) + 1
        result_dict = ', '.join([f'{key}={value}' for key, value in result_dict.items()])
        return result_dict
    def show_calculated_popup(self):
        Wall_size_value = int(self.ids.Wall_Size.text)
        file = open(SETTINGSFILE, "r")
        lines = eval(file.read())
        Rack_sizes = lines[4]
        Rack_sizes.sort(reverse=True)
        target_number = Wall_size_value


        if target_number >= Rack_sizes[len(Rack_sizes)-1]:
            best_combination = None
            best_difference = float('inf')

            for length in range(1, len(Rack_sizes) + (target_number//45)+1):
                # Generate all combinations of numbers with the current length
                combinations = combinations_with_replacement(Rack_sizes, length)

                for combo in combinations:
                    # print(combo)
                    current_sum = sum(combo)
                    difference = target_number - current_sum

                    if difference >= 0 and difference < best_difference:
                        best_combination = combo
                        best_difference = difference

                    if current_sum == target_number:
                        break

            number_of_racks = f"Rack Quantity : {len(best_combination)}\nPole Quantity : {len(best_combination)+1}\n-------------------------------\nSpace Used: {sum(best_combination)}\"/{target_number}\"\n-\nRack Sizes: {self.tuple_to_dict(best_combination)}\n-\nRack Sizes : {best_combination}"

        else:
            number_of_racks = f"Size of wall is too small. Minimum size requirement is {Rack_sizes[len(Rack_sizes)-1]}"
        dialog = MDDialog(
                title="Successfully Calculated",
                text=number_of_racks,
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=lambda *args: dialog.dismiss()
                    )
                ],
            )
        dialog.open()

class LoadingScreen(Screen, BackgroundFloatLayout):
    def goto_home(self):
        self.manager.current = 'home'
    def url_opener_mail(self, *args):
        wb.open_new_tab("mailto:playwithaayan25@gmail.com")
    def url_opener_ir(self, *args):
        wb.open_new_tab("https://aayan-yasin25.itch.io/rack-calculator/devlog/669543/rack-calculator-issue-resolver")
    
        
    
class ErrorScreen(Screen, BackgroundFloatLayout):
    def __init__(self,**kwargs):
        super(ErrorScreen, self).__init__(**kwargs)
    def url_opener_mail(self, *args):
        wb.open_new_tab("mailto:playwithaayan25@gmail.com")
    def url_opener_ir(self, *args):
        wb.open_new_tab("https://aayan-yasin25.itch.io/rack-calculator/devlog/669543/rack-calculator-issue-resolver")
    def on_enter(self, *args):
        main_layout = Builder.load_string("""
ErrorScreen:
    BoxLayout:
        orientation: 'vertical'
                                            
        BoxLayout:
            orientation: 'vertical'
            padding: dp(100)

            AsyncImage:
                source: 'https://danishbrothers.com.pk/wp-content/uploads/2024/01/Picsart_24-01-19_23-14-28-957-min.png'
                size_hint_y: None
                height: '200dp'

            MDLabel:
                text: '[Critical Error]'
                font_size: 24

            BoxLayout:
                orientation: 'vertical'

                MDLabel:
                    text: "1) Some files are not found which can cause application to crash or behave abnormally.."
                    font_size: 16

                MDLabel:
                    text: "2) Error Report: """+self.error+""""
                    font_size: 16

                MDLabel:
                    text: "3) Try Retrieving Files or Uninstall Rack Calculator and run Setup.exe again."
                    font_size: 16

                MDLabel:
                    text: "4) If error persists, please contact at playwithaayan25@gmail.com or Visit Help Center."
                    font_size: 16


            BoxLayout:
                spacing: 10
                                        
                MDRaisedButton:
                    text: "Mail Us"
                    pos_hint: {'center_x': 0.5}
                    theme_text_color: 'Custom'
                    text_color: 0,0,0, 1
                    line_color: 0,0,0, 1
                    md_bg_color: 1, 1, 1, 1
                    on_release: root.url_opener_mail()
                                        
                MDRaisedButton:
                    text: "Help Center"
                    pos_hint: {'center_x': 0.5}
                    theme_text_color: 'Custom'
                    text_color: 0,0,0, 1
                    line_color: 0,0,0, 1
                    md_bg_color: 1, 1, 1, 1
                    on_release: root.url_opener_ir()
                                        
                MDRaisedButton:
                    text: "Retrieve Files"
                    pos_hint: {'center_x': 0.5}
                    theme_text_color: 'Custom'
                    text_color: 0,0,0, 1
                    line_color: 0,0,0, 1
                    md_bg_color: 1, 1, 1, 1
                    on_release: app.stop()

                # MDRaisedButton:
                #     text: "Close"
                #     pos_hint: {'center_x': 0.5}
                #     theme_text_color: 'Custom'
                #     text_color: 0,0,0, 1
                #     line_color: 0,0,0, 1
                #     md_bg_color: 1, 1, 1, 1
                #     on_release: app.stop()

        BoxLayout:
            orientation: 'horizontal'
            padding: dp(16)
            size_hint_y: None
            height: '40dp'

            MDLabel:
                text: "© 2024 Aayan Yasin"
                halign: 'left'
                font_style: 'Caption'
        """)

        self.add_widget(main_layout)

    def is_internet_available(self):
        """
        Check if the internet connection is available.

        Returns:
        - bool: True if internet is available, False otherwise.
        """
        try:
            # Try to connect to Google's DNS server (8.8.8.8) with a timeout of 1 second
            socket.create_connection(("8.8.8.8", 53), timeout=1)
            return True
        except OSError:
            return False

    def download_file(self, url, folder_path, file_name):
        """
        Download a file from a given URL and save it to the specified folder.

        Parameters:
        - url (str): The URL of the file to be downloaded.
        - folder_path (str): The path of the folder where the file will be saved.
        - file_name (str): The name to be given to the downloaded file.
        """
        try:
            # Check for internet connection
            if not self.is_internet_available():
                print()
                dialog = MDDialog(
                    title="Successfully Calculated",
                    text="No internet connection. File download aborted.",
                    buttons=[
                        MDFlatButton(
                            text="Close", on_release=lambda *args: dialog.dismiss()
                        )
                    ],
                )
                dialog.open()
                return

            # Create the folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Concatenate the folder path and file name
            file_path = os.path.join(folder_path, file_name)

            # Make a request to the URL and download the file
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses

            # Save the content to the file
            with open(file_path, 'wb') as file:
                file.write(response.content)

            print(f"File '{file_name}' downloaded successfully to '{folder_path}'.")
        except Exception as e:
            print()
            dialog = MDDialog(
                    title="Successfully Calculated",
                    text=f"Error downloading file: Reason - {e}",
                    buttons=[
                        MDFlatButton(
                            text="Close", on_release=lambda *args: dialog.dismiss()
                        )
                    ],
                )
            dialog.open()


class MyApp(MDApp):
    def build(self):
        
        sm = ScreenManager()

        try:
            # Attempt to Check files
            self.check_files_exists("assets/icon.png", "assets/background.jpg", "assets/logo.png", "data/design.kv", "data/invoice.py")
            # Attempt to load the KV file
            Builder.load_file('data/design.kv')
            sm.add_widget(LoadingScreen(name='loading_screen'))
            sm.add_widget(MainScreen(name='main'))
            sm.add_widget(HomeScreen(name='home'))
            sm.add_widget(SettingsScreen(name='settings'))
            sm.add_widget(PalletScreen(name='pallet'))
            sm.add_widget(WallShelvingScreen(name='wallshelving'))
            sm.add_widget(QuotationScreen(name='quotation'))
        except Exception as e:
            # Handle file not found exception
            ec = ErrorScreen(name='error')
            ec.error = str(e)
            sm.add_widget(ec)

        return sm

    def check_files_exists(self, *args):
        file_not_found = []
        for i in args:
            if not os.path.exists(i):
                file_not_found.append(i)
        if len(file_not_found) > 0:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ", ".join(file_not_found))

if __name__ == '__main__':
    MyApp().run()
