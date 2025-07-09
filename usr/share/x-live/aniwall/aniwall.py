#!/usr/bin/python3

import os
import sys
import subprocess
import time
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QFileDialog, QWidget, QTextEdit, QLabel, QVBoxLayout, QProgressBar   
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QProcess, QTimer, QSize, QCoreApplication
from threading import Thread

class AnimatedWallpaperApp:
    def __init__(self):

        self.app = QApplication([])
        self.tray_icon = QSystemTrayIcon(QIcon("/usr/share/x-live/aniwall/icon.png"), self.app)
        self.infowidget = QWidget()
        self.infowidget.move(240,320)
        #self.infowidget.setFixedSize(0,0)
        self.layout=QVBoxLayout()
        self.text= QLabel("Video wird umgewandelt")
        #self.infowidget.setFixedSize(620,98)
        #self.text.setFixedSize(300,48)
        self.layout.addWidget(self.text)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.layout.addWidget(self.progress)
        self.infowidget.setLayout(self.layout)
        #self.infowidget.show()
        self.infowidget.hide()
        # Verzeichnisse für Frames und ursprünglicher Hintergrund
        self.frame_dir = os.path.expanduser("~/.aniwall/frames")
        if not os.path.exists(self.frame_dir):
            os.makedirs(self.frame_dir)
        self.original_wallpaper = self.get_current_wallpaper()

        # Menüeinträge
        menu = QMenu()
        self.select_video_action = QAction("Video importieren")
        self.select_video_action.triggered.connect(self.select_video)
        menu.addAction(self.select_video_action)

        self.start_action = QAction("Animation starten")
        self.start_action.triggered.connect(self.start_animation)
        #self.start_action.setEnabled(False)  # Deaktiviert beim Start
        menu.addAction(self.start_action)

        self.stop_action = QAction("Animation stoppen")
        self.stop_action.triggered.connect(self.stop_animation)
        self.stop_action.setEnabled(False)
        menu.addAction(self.stop_action)

        self.control_action = QAction("Control Center")
        #self.control_action.triggered.connect(self.stop_animation)
        self.control_action.setEnabled(True)
        #menu.addAction(self.control_action)

        # Untermenü für Frame-Überspringen
        self.frame_skip_menu = QMenu("Frame-Überspringen")
        self.frame_skip = 1  # Standardwert auf 1 setzen, um null zu vermeiden

        self.text_skip1="\tJeden "
        self.text_skip2="ten Frame"

        # Jedes Frame-Überspringen einzeln hinzufügen
        self.skip_1_action = QAction(f"->{self.text_skip1}1{self.text_skip2}", self.app)
        self.skip_1_action.triggered.connect(lambda: self.set_frame_skip(1))
        self.frame_skip_menu.addAction(self.skip_1_action)

        self.skip_2_action = QAction(f"{self.text_skip1}2{self.text_skip2}", self.app)
        self.skip_2_action.triggered.connect(lambda: self.set_frame_skip(2))
        self.frame_skip_menu.addAction(self.skip_2_action)

        self.skip_3_action = QAction(f"{self.text_skip1}3{self.text_skip2}", self.app)
        self.skip_3_action.triggered.connect(lambda: self.set_frame_skip(3))
        self.frame_skip_menu.addAction(self.skip_3_action)

        self.skip_4_action = QAction(f"{self.text_skip1}4{self.text_skip2}", self.app)
        self.skip_4_action.triggered.connect(lambda: self.set_frame_skip(4))
        self.frame_skip_menu.addAction(self.skip_4_action)

        self.skip_5_action = QAction(f"{self.text_skip1}5{self.text_skip2}", self.app)
        self.skip_5_action.triggered.connect(lambda: self.set_frame_skip(5))
        self.frame_skip_menu.addAction(self.skip_5_action)

        self.skip_10_action = QAction(f"{self.text_skip1}10{self.text_skip2}", self.app)
        self.skip_10_action.triggered.connect(lambda: self.set_frame_skip(10))
        self.frame_skip_menu.addAction(self.skip_10_action)

        menu.addMenu(self.frame_skip_menu)


        # Untermenü für Frame-speed
        self.frame_speed_menu = QMenu("Frame-Geschwindigkeit")
        self.frame_speed = 1  # Standardwert auf 1 setzen, um null zu vermeiden

        self.text_speed = "\tGeschwindigkeit / "
        # Jedes Frame-Überspringen einzeln hinzufügen
        self.speed_1_action = QAction(f"->{self.text_speed}1", self.app)
        self.speed_1_action.triggered.connect(lambda: self.set_frame_speed(1))
        self.frame_speed_menu.addAction(self.speed_1_action)

        self.speed_2_action = QAction(f"{self.text_speed}2", self.app)
        self.speed_2_action.triggered.connect(lambda: self.set_frame_speed(2))
        self.frame_speed_menu.addAction(self.speed_2_action)

        self.speed_3_action = QAction(f"{self.text_speed}3", self.app)
        self.speed_3_action.triggered.connect(lambda: self.set_frame_speed(3))
        self.frame_speed_menu.addAction(self.speed_3_action)

        self.speed_4_action = QAction(f"{self.text_speed}4", self.app)
        self.speed_4_action.triggered.connect(lambda: self.set_frame_speed(4))
        self.frame_speed_menu.addAction(self.speed_4_action)

        self.speed_5_action = QAction(f"{self.text_speed}5", self.app)
        self.speed_5_action.triggered.connect(lambda: self.set_frame_speed(5))
        self.frame_speed_menu.addAction(self.speed_5_action)

        self.speed_10_action = QAction(f"{self.text_speed}10", self.app)
        self.speed_10_action.triggered.connect(lambda: self.set_frame_speed(10))
        self.frame_speed_menu.addAction(self.speed_10_action)

        menu.addMenu(self.frame_speed_menu)

        self.exit_action = QAction("Beenden")
        #self.exit_action.triggered.connect(self.exit_app)
        self.exit_action.triggered.connect(self.quit_application)
        menu.addAction(self.exit_action)
        self.tray_icon.activated.connect(self.toogle_run_animation)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

        # Variablen für Animation
        self.animation_running = False
        self.animation_thread = None
        self.sleep_time = 0.1  # Standard Schlafzeit
        
        
        # Hinzufügen eines Quit-Signals zur App
        #self.app.aboutToQuit.connect(self.quit_application)
        #self.app.aboutToQuit.connect(self.prevent_close)
        QCoreApplication.instance().aboutToQuit.connect(self.quit_application)
        self.start_animation()


    def get_primary_monitor(self):
        xrandr_output = subprocess.getoutput("xrandr --query")
        for line in xrandr_output.splitlines():
            if " connected primary" in line:
                return f"monitor{line.split()[0]}"
        return None

    def get_active_workspace(self):
        wmctrl_output = subprocess.getoutput("wmctrl -d")
        for line in wmctrl_output.splitlines():
            if "*" in line:  # Aktiver Workspace hat ein "*"
                workspace_id = line.split()[0]
                return f"workspace{workspace_id}"
        return None

    def get_current_wallpaper(self):
        monitor = self.get_primary_monitor()
        workspace = self.get_active_workspace()
        if monitor and workspace:
            return subprocess.getoutput(f"xfconf-query -c xfce4-desktop -p /backdrop/screen0/{monitor}/{workspace}/last-image")
        return None

    def select_video(self):
        QTimer.singleShot(0, self.select_video_start)

    def select_video_start(self):
        self.stop_animation()
        video_path, _ = QFileDialog.getOpenFileName(None, "Wähle ein Video", "", "Videodatein (*.mp4 *.mkv *.avi *.mov *.webm *.flv *.mpeg *.mpg *.wmv);;All Files (*)")
        
        if video_path:
            # Leeren des Frame-Ordners vor dem Extrahieren
            for frame_file in os.listdir(self.frame_dir):
                os.remove(os.path.join(self.frame_dir, frame_file))

            self.start_frame_extraction(video_path)

    def start_frame_extraction(self, video_path):
        self.infowidget.show()
        self.zeit=""
        self.titledauer=""
        self.titleseconds=0
        self.zeitseconds=0
        self.fortschrittprozent=0

        self.extract_frames_ffmpeg(video_path)
 

    def extract_frames_ffmpeg(self, video_path):
        frame_pattern = os.path.join(self.frame_dir, "frame_%04d.jpg")
        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyRead.connect(self.read_output)
        self.process.finished.connect(self.extract_frames_finished)
        self.process.start("ffmpeg", ["-i", video_path, "-vf", "fps=10", frame_pattern])
        #self.process.waitForFinished()
        
        
    def extract_frames_finished(self):
        print("Frame-Erstellung abgeschlossen")
        # Benachrichtigung anzeigen
        self.start_action.setEnabled(True)  # Aktivieren, wenn Frames erfolgreich extrahiert wurden
        self.tray_icon.showMessage("Erstellung abgeschlossen", "Die Frames wurden erfolgreich erstellt.", QSystemTrayIcon.Information, 15000)
        
        #print("Video ausgewählt", "Das Video wurde erfolgreich in Frames umgewandelt.")
        self.start_animation()
        time.sleep(2)
        self.infowidget.hide()

    def read_output(self):
        if self.process:
            output = self.process.readAll().data().decode()
            output = output.replace('\r\n', '\n').replace('\r', '\n')
            #print(output)
            self.check_output(output)
            self.text.setText("Video wird umgewandelt !!")# + " \n"+self.zeit+" von "+self.titledauer+" !!")

    def check_output(self,output):
        completeText = output.splitlines()
        for Text in completeText:
            #print("1-",Text.strip())
            if "time=" in Text.strip().lower():
                dauer = Text.strip().lower().split("time=")[1].split(" ")[0]
                hours = dauer.split(":")[0]
                minutes = dauer.split(":")[1]
                seconds = dauer.split(":")[2].split(".")[0]
                self.zeit=hours+ " Stunden " + minutes + " Minuten " + seconds + " Sekunden"
                self.zeitseconds = int(hours)*3600+int(minutes)*60+int(seconds)
            if Text.strip().lower().startswith("duration") and self.titledauer=="":
                dauer = Text.strip().lower().split(" ")[1]
                hours = dauer.split(":")[0]
                minutes = dauer.split(":")[1]
                seconds = dauer.split(":")[2].split(".")[0]
                #self.titledauer = Text.strip().lower().split(" ")[1]
                self.titledauer = hours+ " Stunden " + minutes + " Minuten " + seconds + " Sekunden"
                self.titleseconds = int(hours)*3600+int(minutes)*60+int(seconds)
                print(self.titleseconds)
            if self.titleseconds>0:    
                self.fortschrittprozent=int(self.zeitseconds/self.titleseconds*100)
            self.progress.setValue(self.fortschrittprozent)
            
    def set_frame_skip(self, skip):
        self.frame_skip = skip
        print("Frame-Überspringen", f"Jeden {skip}ten Frame wird angezeigt.")
        #print(self.frame_skip)
        self.set_arrows()

    def set_frame_speed(self, speed):
        self.sleep_time = int(speed)/10  # Anpassung der Schlafzeit basierend auf dem Frame-Überspringen
        print("Frame-Geschwindigkeit", f"Auf Geschwindigkeit / {speed} gesetzt.")
        #print(self.frame_skip)
        self.set_arrows()

    def set_arrows(self):
        print(self.sleep_time)
        self.speed_1_action.setText(f"{self.text_speed}1")
        self.speed_2_action.setText(f"{self.text_speed}2")
        self.speed_3_action.setText(f"{self.text_speed}3")
        self.speed_4_action.setText(f"{self.text_speed}4")
        self.speed_5_action.setText(f"{self.text_speed}5")
        self.speed_10_action.setText(f"{self.text_speed}10")
        
        if self.sleep_time == 0.1: self.speed_1_action.setText(f"->{self.text_speed}1")
        if self.sleep_time == 0.2: self.speed_2_action.setText(f"->{self.text_speed}2")
        if self.sleep_time == 0.3: self.speed_3_action.setText(f"->{self.text_speed}3")
        if self.sleep_time == 0.4: self.speed_4_action.setText(f"->{self.text_speed}4")
        if self.sleep_time == 0.5: self.speed_5_action.setText(f"->{self.text_speed}5")
        if self.sleep_time == 1: self.speed_10_action.setText(f"->{self.text_speed}10")
        
        self.skip_1_action.setText(f"{self.text_skip1}1{self.text_skip2}")
        self.skip_2_action.setText(f"{self.text_skip1}2{self.text_skip2}")
        self.skip_3_action.setText(f"{self.text_skip1}3{self.text_skip2}")
        self.skip_4_action.setText(f"{self.text_skip1}4{self.text_skip2}")
        self.skip_5_action.setText(f"{self.text_skip1}5{self.text_skip2}")
        self.skip_10_action.setText(f"{self.text_skip1}10{self.text_skip2}")
        
        
        self.frame_skip=int(self.frame_skip)
        if self.frame_skip == 1:self.skip_1_action.setText(f"->{self.text_skip1}1{self.text_skip2}")
        if self.frame_skip == 2:self.skip_2_action.setText(f"->{self.text_skip1}2{self.text_skip2}")
        if self.frame_skip == 3:self.skip_3_action.setText(f"->{self.text_skip1}3{self.text_skip2}")
        if self.frame_skip == 4:self.skip_4_action.setText(f"->{self.text_skip1}4{self.text_skip2}")
        if self.frame_skip == 5:self.skip_5_action.setText(f"->{self.text_skip1}5{self.text_skip2}")
        if self.frame_skip == 10:self.skip_10_action.setText(f"->{self.text_skip1}10{self.text_skip2}")

    def toogle_run_animation(self):
        if self.animation_running:
            self.stop_animation()
        else:
            self.start_animation()
            
        

    def start_animation(self):
        frames = sorted(os.listdir(self.frame_dir))
        if not frames:
            print("Keine Frames", "Bitte wähle ein Video, um Frames zu extrahieren.")
            return

        self.animation_running = True
        self.start_action.setEnabled(False)
        self.stop_action.setEnabled(True)

        # Starte Animation in einem separaten Thread
        self.animation_thread = Thread(target=self.animate_wallpaper)
        self.animation_thread.start()

    def animate_wallpaper(self):
        frames = sorted(os.listdir(self.frame_dir))
        monitor = self.get_primary_monitor()
        workspace = self.get_active_workspace()
        
        while self.animation_running:
            for i, frame in enumerate(frames):
                if not self.animation_running:
                    return
                if self.frame_skip > 0 and i % self.frame_skip == 0:  # Nur jeden n-ten Frame anzeigen
                    frame_path = os.path.join(self.frame_dir, frame)
                    try:
                        subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-p", f"/backdrop/screen0/{monitor}/{workspace}/last-image", "-s", frame_path], check=True)
                        time.sleep(self.sleep_time)  # Schlafzeit anpassen
                    except subprocess.CalledProcessError as e:
                        print(f"Fehler beim Setzen des Wallpapers: {e}")
                    

    def stop_animation(self):
        self.animation_running = False
        if self.animation_thread:
            self.animation_thread.join()

        # Setze ursprünglichen Hintergrund zurück
        monitor = self.get_primary_monitor()
        workspace = self.get_active_workspace()
        if monitor and workspace and self.original_wallpaper:
            try:
                subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-p", f"/backdrop/screen0/{monitor}/{workspace}/last-image", "-s", self.original_wallpaper], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Fehler beim Zurücksetzen des Wallpapers: {e}")

        self.start_action.setEnabled(True)
        self.stop_action.setEnabled(False)

    #def prevent_close(self, event=None):
        # Verhindert, dass das Programm durch andere Events geschlossen wird
    #    if event is not None:
    #        event.ignore()

    def closeEvent(self, event):
            self.quit_application()
            event.accept()  # Das Fenster darf geschlossen werden


    def quit_application(self):
        self.stop_animation()  # Sicherstellen, dass Animationen gestoppt werden
        self.tray_icon.hide()
        # Aktiviert das Beenden nur durch den Beenden-Button
        # self.app.aboutToQuit.disconnect(self.prevent_close)
        self.app.quit()
        
    def exit_app(self):
        self.stop_animation()
        self.tray_icon.hide()
        sys.exit()


if __name__ == "__main__":
    app = AnimatedWallpaperApp()
    sys.exit(app.app.exec_())
