import sys
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from wiresharkpractise import get_local_ip_address
from constants import wireshark_file_path


WINDOW_SIZE = 500
LABEL_HEIGHT = 40

class SysInfoWindow(App):
    def build(self):
        root = FloatLayout()

        # Adding background image
        bg_image = Image(source='background.png', allow_stretch=True, keep_ratio=False, size=(WINDOW_SIZE, WINDOW_SIZE))
        root.add_widget(bg_image)

        # Create layout for information display
        infoLayout = BoxLayout(orientation='vertical', size_hint=(None, None), width=WINDOW_SIZE, height=WINDOW_SIZE)
        infoLayout.pos_hint = {'top': 1.0}  # Position the layout at the top of the screen
        infoLayout.padding = [20, 20]  # Add padding to the layout

        # Define labels for displaying the info
        self.infoLabels = {
            "Computer name": Label(text="Computer name: ...", color=(1, 1, 1, 1)),
            "IP Address": Label(text="IP Address: ...", color=(1, 1, 1, 1)),
            "Protocol": Label(text="Protocol: ...", color=(1, 1, 1, 1)),
            "Websites Visited": Label(text="Websites Visited: ...", color=(1, 1, 1, 1)),
            "SFTP": Label(text="SFTP: ...", color=(1, 1, 1, 1)),
        }

        # Update label style and add to layout
        for label in self.infoLabels.values():
            label.size_hint_y = None
            label.height = LABEL_HEIGHT
            infoLayout.add_widget(label)

        # Add infoLayout to the root
        root.add_widget(infoLayout)

        # This is where you would connect to the backend to update the labels
        self.updateInfo()

        return root


    def updateInfo(self):
        """Update the information labels with data from the backend."""
        self.infoLabels["Computer name"].text = f"Computer name: {self.getComputerName()}"
        self.infoLabels["IP Address"].text = f"IP Address: {self.getIPAddress()}"
        self.infoLabels["Websites Visited"].text = f"Websites Visited: {self.websites()}"
        # ... update other labels similarly ...

    def getComputerName(self):
        
        return "comp_name"

    def getIPAddress(self):
       ip = get_local_ip_address()
       return ip 
       
    
    def websites(self):
        return "website"

if __name__ == "__main__":
    SysInfoWindow().run()
