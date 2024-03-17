import pyshark
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from constants import wireshark_file_path

height = 500
width = 500
class PacketAnalysisApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')

        # Display packet analysis results
        self.display_results(root)

        # Adding close button
        close_button = Button(text='Close', size_hint=(0.2, 0.1), pos_hint={'right': 1, 'top': 1})
        close_button.bind(on_press=self.confirm_close)
        root.add_widget(close_button)

        return root
    
    def confirm_close(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Are you sure you want to close the application?'))

        # Create "Yes" button to close the app
        yes_button = Button(text='Yes', size_hint=(1, None), height=40)
        yes_button.bind(on_press=self.close_app)
        content.add_widget(yes_button)

        # Create "No" button to cancel
        no_button = Button(text='No', size_hint=(1, None), height=40)
        content.add_widget(no_button)

        # Create Popup
        popup = Popup(title='Confirmation', content=content, size_hint=(None, None), size=(300, 200))
        popup.open()

        # Bind "No" button to dismiss the popup
        no_button.bind(on_press=popup.dismiss)

    def close_app(self, instance):
        App.get_running_app().stop()

    def display_results(self, layout):
        # Display total unique links
        total_links_label = Label(text=f"Total Unique Links: {self.count_total_websites()}", size_hint=(1, None))
        layout.add_widget(total_links_label)

        # Display total packets
        total_packets_label = Label(text=f"Total Packets: {self.count_packets()}", size_hint=(1, None))
        layout.add_widget(total_packets_label)

        # Display source IP address
        source_ip_label = Label(text=f"Source IP Address: {self.get_source_ip()}", size_hint=(1, None))
        layout.add_widget(source_ip_label)

        # Display protocol information
        protocol_label = Label(text="Protocol Information (First 5 Packets):", size_hint=(1, None))
        layout.add_widget(protocol_label)
        self.display_protocol(layout)

    def count_packets(self):
        cap = pyshark.FileCapture(wireshark_file_path)
        total_packets = sum(1 for _ in cap)
        return total_packets

    def count_total_websites(self):
        cap = pyshark.FileCapture(wireshark_file_path)
        visited_websites = set()

        for packet in cap:
            if "IP" in packet:
                if hasattr(packet, "dns") and packet.dns.qry_name:
                    dns_query = packet.dns.qry_name.lower()
                    visited_websites.add(dns_query)
                elif hasattr(packet, "http") and packet.http.host:
                    http_host = packet.http.host.lower()
                    visited_websites.add(http_host)

        return len(visited_websites)

    def display_protocol(self, layout, max_rows=5):
        try:
            with pyshark.FileCapture(wireshark_file_path) as cap:
                for row_num, pkt in enumerate(cap):
                    try:
                        layer_names = [lay.layer_name for lay in pkt.layers]
                        protocol_info_label = Label(text=f"Packet {row_num + 1}: {', '.join(layer_names)}", size_hint=(1, None))
                        layout.add_widget(protocol_info_label)
                    except AttributeError as ex:
                        print(ex)

                    if row_num >= max_rows - 1:
                        break
        except pyshark.FileCaptureException as e:
            print(f"Error opening file: {e}")

    def get_source_ip(self):
        pcap_file = wireshark_file_path
        # Open the pcap file
        cap = pyshark.FileCapture(pcap_file)

        # Iterate over each packet in the pcap file
        for packet in cap:
            # Check if the packet has an IP layer
            if 'IP' in packet:
                # Extract and return the source IP address
                return packet.ip.src

        # If no IP address is found, return None
        return None

if __name__ == "__main__":
    PacketAnalysisApp().run()
