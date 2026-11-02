import cv2

import mediapipe as mp

import customtkinter as ctk

from PIL import Image

import threading
import time
import os
import json
import re
import shutil

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# PROJECT MODULES
# ============================================================

from modules.face_detection import detect_face
from modules.eye_contact import calculate_eye_contact
from modules.head_pose import estimate_head_pose
from modules.smile import detect_smile
from modules.posture import detect_posture
from modules.hand_gesture import detect_hand_gesture
from modules.session_tracker import SessionTracker
from modules.feedback import generate_feedback

from modules.report_manager import (
    save_session,
    load_history
)

from modules.audio_recorder import AudioRecorder
from modules.speech_to_text import SpeechToText
from modules.speech_analyzer import analyze_speech


# ============================================================
# APPEARANCE
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# COLORS
# ============================================================

BG = "#070B12"
HEADER = "#0B111B"
CARD = "#101824"
CARD_2 = "#131E2D"
BORDER = "#202C3B"

TEXT = "#F4F7FB"
MUTED = "#8290A3"
SOFT_TEXT = "#B7C1CF"

GREEN = "#22C55E"
BLUE = "#3B82F6"
CYAN = "#22D3EE"
YELLOW = "#F59E0B"
RED = "#EF4444"
PURPLE = "#A855F7"


# ============================================================
# PERSON DATA
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_FOLDER = os.path.join(
    BASE_DIR,
    "data"
)

PEOPLE_FILE = os.path.join(
    DATA_FOLDER,
    "people.json"
)

REPORTS_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)


# ============================================================
# MAIN APPLICATION
# ============================================================

class CommunicationAI(ctk.CTk):

    def __init__(self):

        super().__init__()

        # ====================================================
        # WINDOW
        # ====================================================

        self.title(
            "Communication AI"
        )

        self.geometry(
            "1420x860"
        )

        self.minsize(
            1200,
            740
        )

        self.configure(
            fg_color=BG
        )

        # ====================================================
        # PERSON SYSTEM
        # ====================================================

        self.people = self.load_people()

        self.current_person = (
            self.get_last_selected_person()
        )

        # Dedicated person folders are the source of truth for session data.
        # Synchronize all existing profiles at startup.
        self.sync_all_person_histories()

        # ====================================================
        # CAMERA
        # ====================================================

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():

            print(
                "ERROR: Cannot open webcam."
            )

        # ====================================================
        # MEDIAPIPE
        # ====================================================

        self.mp_face_mesh = (
            mp.solutions.face_mesh
        )

        self.mp_drawing = (
            mp.solutions.drawing_utils
        )

        self.face_mesh = (
            self.mp_face_mesh.FaceMesh(
                max_num_faces=5,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
        )

        # ====================================================
        # SESSION
        # ====================================================

        self.session = SessionTracker()

        self.session_start_time = None

        self.last_result = None
        self.last_feedback = None
        self.last_report_path = None

        # ====================================================
        # AUDIO & SPEECH
        # ====================================================

        self.audio_recorder = AudioRecorder()
        self.speech_engine = None
        self.speech_analysis = None
        self.audio_file_path = None

        print("Loading speech models in background...")
        threading.Thread(
            target=self._init_speech_engine,
            daemon=True
        ).start()

        # ====================================================
        # CAMERA VARIABLES
        # ====================================================

        self.running = True
        self.current_frame = None

        # ====================================================
        # EVALUATION TARGET LOCK
        # ====================================================

        # The evaluation uses one face as the primary target when
        # multiple people are visible.  The target is selected when
        # an evaluation starts and then tracked by face position.
        self.target_locked = False
        self.target_center = None
        self.target_face_area = 0.0
        self.target_missing_frames = 0
        self.target_max_missing_frames = 18
        self.target_status = "WAITING"

    def _init_speech_engine(self):
        """Load speech model in the background to avoid blocking the UI."""
        try:
            self.speech_engine = SpeechToText(
                model_size="medium.en"
            )
            print("Speech model loaded successfully.")
        except Exception as e:
            print(f"FAILED to load speech model: {e}")

        # ====================================================
        # BUILD UI
        # ====================================================

        self.create_layout()

        # ====================================================
        # CAMERA THREAD
        # ====================================================

        self.camera_thread = threading.Thread(
            target=self.camera_loop,
            daemon=True
        )

        self.camera_thread.start()

        self.update_camera()
        self.update_timer()

        # ====================================================
        # CLOSE EVENT
        # ====================================================

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )


    # ========================================================
    # PERSON DATABASE
    # ========================================================

    def ensure_data_folder(self):

        if not os.path.exists(
            DATA_FOLDER
        ):

            os.makedirs(
                DATA_FOLDER
            )


    def load_people(self):

        self.ensure_data_folder()

        if not os.path.exists(
            PEOPLE_FILE
        ):

            data = {
                "people": [],
                "last_selected": ""
            }

            self.save_people_data(
                data
            )

            return data

        try:

            with open(
                PEOPLE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if not isinstance(
                data,
                dict
            ):

                data = {}

            if not isinstance(
                data.get("people"),
                list
            ):

                data["people"] = []

            if not isinstance(
                data.get("last_selected"),
                str
            ):

                data["last_selected"] = ""

            return data

        except (
            json.JSONDecodeError,
            OSError
        ):

            data = {
                "people": [],
                "last_selected": ""
            }

            self.save_people_data(
                data
            )

            return data


    def save_people_data(
        self,
        data=None
    ):

        self.ensure_data_folder()

        if data is None:

            data = self.people

        try:

            with open(
                PEOPLE_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except OSError as e:

            print(
                "Could not save people data:"
            )

            print(e)

            return False


    def sync_all_person_histories(self):

        changed = False

        for person in self.people.get("people", []):

            if not isinstance(person, dict):
                continue

            name = str(person.get("name", "")).strip()

            if not name:
                continue

            disk_sessions = self.load_person_sessions_from_disk(name)

            if person.get("sessions", []) != disk_sessions:
                person["sessions"] = disk_sessions
                changed = True

        if changed:
            self.save_people_data()


    def get_people_names(self):

        names = []

        for person in self.people.get(
            "people",
            []
        ):

            if isinstance(
                person,
                dict
            ):

                name = person.get(
                    "name",
                    ""
                )

                if name:

                    names.append(
                        name
                    )

        return names


    def get_last_selected_person(self):

        names = self.get_people_names()

        last_selected = (
            self.people.get(
                "last_selected",
                ""
            )
        )

        if (
            last_selected
            and last_selected in names
        ):

            return last_selected

        if names:

            return names[0]

        return ""


    def create_person_record(
        self,
        name
    ):

        record = {
            "name": name,
            "sessions": []
        }

        self.people.setdefault(
            "people",
            []
        ).append(
            record
        )

        self.people[
            "last_selected"
        ] = name

        self.save_people_data()

        return record


    def find_person(
        self,
        name
    ):

        for person in self.people.get(
            "people",
            []
        ):

            if (
                isinstance(person, dict)
                and person.get("name") == name
            ):

                return person

        return None


    # ========================================================
    # PERSON SESSION DATA
    # ========================================================

    def get_person_sessions(
        self,
        person_name=None
    ):

        if person_name is None:

            person_name = (
                self.current_person
            )

        if not person_name:

            return []

        person = self.find_person(
            person_name
        )

        if not person:

            return []

        sessions = person.get(
            "sessions",
            []
        )

        if isinstance(
            sessions,
            list
        ):

            return sessions

        return []


    def save_person_session(
        self,
        person_name,
        session_data
    ):

        person = self.find_person(
            person_name
        )

        if not person:

            person = self.create_person_record(
                person_name
            )

        if "sessions" not in person:

            person["sessions"] = []

        person["sessions"].append(
            session_data
        )

        self.people[
            "last_selected"
        ] = person_name

        self.save_people_data()


    # ========================================================
    # SAFE PERSON FOLDER NAME
    # ========================================================

    def safe_folder_name(
        self,
        name
    ):

        # Keep the folder name readable while preventing path traversal
        # and Windows-invalid filename characters.
        cleaned = re.sub(
            r'[^A-Za-z0-9 _-]',
            "_",
            str(name)
        )

        cleaned = re.sub(
            r'\s+',
            " ",
            cleaned
        ).strip(" .")

        if not cleaned:
            cleaned = "Person"

        return cleaned[:80]


    # ========================================================
    # CREATE PERSON REPORT FOLDER
    # ========================================================

    def prepare_person_report_folder(
        self,
        person_name
    ):

        folder_name = self.safe_folder_name(
            person_name
        )

        folder = os.path.join(
            REPORTS_FOLDER,
            folder_name
        )

        os.makedirs(
            folder,
            exist_ok=True
        )

        return folder


    def person_history_file(self, person_name):
        """Return the persistent session-history file for one person."""
        folder = self.prepare_person_report_folder(person_name)
        return os.path.join(folder, "session_history.json")


    def load_person_sessions_from_disk(self, person_name):
        """Load one person's sessions from their own history file."""
        if not person_name:
            return []

        path = self.person_history_file(person_name)

        if not os.path.exists(path):
            return []

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (json.JSONDecodeError, OSError) as e:
            print("Could not load person history:", e)

        return []


    def save_person_sessions_to_disk(self, person_name, sessions):
        """Persist one person's sessions independently of every other person."""
        if not person_name:
            return False

        path = self.person_history_file(person_name)

        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(
                    sessions,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return True

        except OSError as e:
            print("Could not save person history:", e)
            return False


    def sync_person_sessions(self, person_name):
        """
        Keep the in-memory people index synchronized with the person's
        dedicated session_history.json file.
        """
        person = self.find_person(person_name)

        if not person:
            return []

        sessions = self.load_person_sessions_from_disk(person_name)

        person["sessions"] = sessions
        self.save_people_data()

        return sessions


    # ========================================================
    # SAVE PERSON REPORT
    # ========================================================

    def save_person_report_copy(
        self,
        person_name,
        report_path
    ):

        if not report_path:

            return report_path

        if not os.path.exists(
            report_path
        ):

            return report_path

        try:

            folder = (
                self.prepare_person_report_folder(
                    person_name
                )
            )

            filename = os.path.basename(
                report_path
            )

            destination = os.path.join(
                folder,
                filename
            )

            shutil.copy2(
                report_path,
                destination
            )

            # ------------------------------------------------
            # Add person information to the report copy
            # ------------------------------------------------

            try:

                with open(
                    destination,
                    "r",
                    encoding="utf-8"
                ) as file:

                    content = file.read()

                content = (
                    "PERSON: "
                    + person_name
                    + "\n\n"
                    + content
                )

                with open(
                    destination,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        content
                    )

            except OSError:

                pass

            # Maintain a small index of generated reports for this person.
            try:
                index_path = os.path.join(
                    folder,
                    "reports.json"
                )

                if os.path.exists(index_path):
                    with open(
                        index_path,
                        "r",
                        encoding="utf-8"
                    ) as file:
                        report_index = json.load(file)
                else:
                    report_index = []

                if not isinstance(report_index, list):
                    report_index = []

                report_record = {
                    "filename": filename,
                    "path": destination,
                    "person": person_name,
                    "created": time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                }

                report_index.append(report_record)

                with open(
                    index_path,
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(
                        report_index,
                        file,
                        indent=4,
                        ensure_ascii=False
                    )

            except (OSError, json.JSONDecodeError):
                pass

            return destination

        except OSError as e:

            print(
                "Could not create person report copy:"
            )

            print(e)

            return report_path


    # ========================================================
    # PERSON SELECTION
    # ========================================================

    def refresh_person_selector(self):

        if not hasattr(
            self,
            "person_menu"
        ):

            return

        names = self.get_people_names()

        values = (
            names
            if names
            else ["No Person"]
        )

        self.person_menu.configure(
            values=values
        )

        if (
            self.current_person
            and self.current_person in names
        ):

            self.person_menu.set(
                self.current_person
            )

        else:

            self.person_menu.set(
                "Select Person"
            )


    def select_person(
        self,
        selected_name
    ):

        if selected_name == "No Person":

            return

        if not selected_name:

            return

        # ----------------------------------------------------
        # Don't switch person during evaluation
        # ----------------------------------------------------

        if self.session.running:

            self.person_menu.set(
                self.current_person
            )

            self.show_message(
                "Evaluation In Progress",
                (
                    "Please end the current evaluation "
                    "before switching to another person."
                ),
                YELLOW
            )

            return

        if not self.find_person(
            selected_name
        ):

            return

        self.current_person = (
            selected_name
        )

        self.people[
            "last_selected"
        ] = selected_name

        self.save_people_data()

        self.update_person_display()

        print(
            f"Current person: {selected_name}"
        )


    def update_person_display(self):

        if hasattr(
            self,
            "person_status_label"
        ):

            if self.current_person:

                self.person_status_label.configure(
                    text=(
                        "CURRENT PERSON: "
                        + self.current_person
                    ),
                    text_color=CYAN
                )

            else:

                self.person_status_label.configure(
                    text="NO PERSON SELECTED",
                    text_color=YELLOW
                )

        self.refresh_person_selector()


    # ========================================================
    # NEW PERSON DIALOG
    # ========================================================

    def show_new_person_dialog(
        self,
        parent=None
    ):

        if self.session.running:

            self.show_message(
                "Evaluation In Progress",
                (
                    "Please end the current evaluation "
                    "before creating another person."
                ),
                YELLOW,
                parent
            )

            return

        if parent is None:

            parent = self

        dialog = ctk.CTkToplevel(
            parent
        )

        dialog.title(
            "Create New Person"
        )

        dialog.geometry(
            "500x330"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            fg_color=BG
        )

        dialog.transient(
            parent
        )

        dialog.grab_set()

        container = ctk.CTkFrame(
            dialog,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            container,
            text="Create New Person",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            pady=(25, 5)
        )

        ctk.CTkLabel(
            container,
            text=(
                "Enter the person's name.\n"
                "Their evaluations and analytics will be stored separately."
            ),
            text_color=MUTED,
            justify="center",
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            pady=(0, 18)
        )

        name_entry = ctk.CTkEntry(
            container,
            width=360,
            height=42,
            corner_radius=9,
            placeholder_text="Person name"
        )

        name_entry.pack()

        name_entry.focus()

        error_label = ctk.CTkLabel(
            container,
            text="",
            text_color=RED,
            font=ctk.CTkFont(
                size=11
            )
        )

        error_label.pack(
            pady=(7, 0)
        )

        buttons = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        buttons.pack(
            pady=(18, 10)
        )

        ctk.CTkButton(
            buttons,
            text="CANCEL",
            width=125,
            height=40,
            corner_radius=9,
            fg_color=CARD_2,
            hover_color="#24334A",
            border_width=1,
            border_color=BORDER,
            command=dialog.destroy
        ).pack(
            side="left",
            padx=5
        )

        def create_person():

            name = name_entry.get().strip()

            if not name:

                error_label.configure(
                    text="Please enter a name."
                )

                return

            if len(name) > 60:

                error_label.configure(
                    text="Name must be 60 characters or less."
                )

                return

            existing_names = [
                item.lower()
                for item in self.get_people_names()
            ]

            if name.lower() in existing_names:

                error_label.configure(
                    text="This person already exists."
                )

                return

            self.create_person_record(
                name
            )

            self.current_person = name

            self.update_person_display()

            dialog.destroy()

            self.show_message(
                "Person Created",
                (
                    f"{name} has been created successfully.\n\n"
                    "All future evaluations will be saved under this person."
                ),
                GREEN
            )

        create_button = ctk.CTkButton(
            buttons,
            text="CREATE PERSON",
            width=150,
            height=40,
            corner_radius=9,
            fg_color=BLUE,
            hover_color="#2563EB",
            command=create_person
        )

        create_button.pack(
            side="left",
            padx=5
        )

        dialog.bind(
            "<Return>",
            lambda event: create_person()
        )


    # ========================================================
    # MESSAGE DIALOG
    # ========================================================

    def show_message(
        self,
        title,
        message,
        color=BLUE,
        parent=None
    ):

        if parent is None:

            parent = self

        dialog = ctk.CTkToplevel(
            parent
        )

        dialog.title(
            title
        )

        dialog.geometry(
            "450x235"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            fg_color=BG
        )

        dialog.transient(
            parent
        )

        dialog.grab_set()

        card = ctk.CTkFrame(
            dialog,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color=color,
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            pady=(25, 10)
        )

        ctk.CTkLabel(
            card,
            text=message,
            text_color=SOFT_TEXT,
            justify="center",
            wraplength=380,
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            pady=(0, 18)
        )

        ctk.CTkButton(
            card,
            text="OK",
            width=100,
            height=36,
            corner_radius=9,
            fg_color=BLUE,
            hover_color="#2563EB",
            command=dialog.destroy
        ).pack()


    # ========================================================
    # MAIN UI
    # ========================================================

    def create_layout(self):

        # ====================================================
        # HEADER
        # ====================================================

        header = ctk.CTkFrame(
            self,
            height=105,
            corner_radius=0,
            fg_color=HEADER
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        # ====================================================
        # BRAND
        # ====================================================

        brand = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        brand.pack(
            side="left",
            padx=30,
            pady=13
        )

        ctk.CTkLabel(
            brand,
            text="COMMUNICATION AI",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            brand,
            text="AI-powered communication performance coach",
            text_color=MUTED,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w"
        )

        # ====================================================
        # HEADER RIGHT
        # ====================================================

        header_right = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        header_right.pack(
            side="right",
            padx=25
        )

        # ====================================================
        # SYSTEM STATUS
        # ====================================================

        self.live_label = ctk.CTkLabel(
            header_right,
            text="●  SYSTEM READY",
            text_color=GREEN,
            fg_color=CARD,
            corner_radius=14,
            width=145,
            height=36,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        self.live_label.pack(
            side="right",
            padx=(8, 0)
        )

        # ====================================================
        # HISTORY
        # ====================================================

        ctk.CTkButton(
            header_right,
            text="History",
            width=105,
            height=38,
            corner_radius=10,
            fg_color=CARD,
            hover_color=CARD_2,
            border_width=1,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.show_history
        ).pack(
            side="right",
            padx=5
        )

        # ====================================================
        # ANALYTICS
        # ====================================================

        ctk.CTkButton(
            header_right,
            text="Analytics",
            width=115,
            height=38,
            corner_radius=10,
            fg_color=BLUE,
            hover_color="#2563EB",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=self.show_analytics
        ).pack(
            side="right",
            padx=5
        )

        # ====================================================
        # PERSON AREA
        # ====================================================

        person_area = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        person_area.pack(
            side="right",
            padx=(10, 0)
        )

        ctk.CTkLabel(
            person_area,
            text="PERSON",
            text_color=MUTED,
            font=ctk.CTkFont(
                size=9,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        selector_row = ctk.CTkFrame(
            person_area,
            fg_color="transparent"
        )

        selector_row.pack()

        self.person_menu = ctk.CTkOptionMenu(
            selector_row,
            width=180,
            height=36,
            corner_radius=9,
            fg_color=CARD,
            button_color=BLUE,
            button_hover_color="#2563EB",
            dropdown_fg_color=CARD,
            dropdown_hover_color=CARD_2,
            dropdown_text_color=TEXT,
            text_color=TEXT,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            values=[
                "No Person"
            ],
            command=self.select_person
        )

        self.person_menu.pack(
            side="left",
            padx=(0, 5)
        )

        ctk.CTkButton(
            selector_row,
            text="+ NEW",
            width=75,
            height=36,
            corner_radius=9,
            fg_color="#172235",
            hover_color="#24334A",
            border_width=1,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            command=self.show_new_person_dialog
        ).pack(
            side="left"
        )

        # ====================================================
        # PERSON STATUS
        # ====================================================

        self.person_status_label = ctk.CTkLabel(
            self,
            text="",
            text_color=CYAN,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        )

        self.person_status_label.pack(
            anchor="w",
            padx=30,
            pady=(8, 0)
        )

        # ====================================================
        # MAIN CONTENT
        # ====================================================

        main = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        main.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(10, 22)
        )

        main.grid_columnconfigure(
            0,
            weight=3
        )

        main.grid_columnconfigure(
            1,
            weight=2
        )

        main.grid_rowconfigure(
            0,
            weight=1
        )

        # ====================================================
        # LEFT AREA
        # ====================================================

        left = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 14)
        )

        # ====================================================
        # CAMERA HEADING
        # ====================================================

        camera_heading = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )

        camera_heading.pack(
            fill="x",
            pady=(0, 10)
        )

        ctk.CTkLabel(
            camera_heading,
            text="Live Communication Analysis",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        self.recording_label = ctk.CTkLabel(
            camera_heading,
            text="READY",
            text_color=MUTED,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        self.recording_label.pack(
            side="right"
        )

        self.target_status_label = ctk.CTkLabel(
            camera_heading,
            text="TARGET: WAITING",
            text_color=MUTED,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        )

        self.target_status_label.pack(
            side="right",
            padx=(0, 18)
        )

        # ====================================================
        # CAMERA CARD
        # ====================================================

        camera_card = ctk.CTkFrame(
            left,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )


        self.camera_label = ctk.CTkLabel(
            camera_card,
            text="Starting camera...",
            text_color=MUTED
        )

        self.camera_label.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12
        )

        # ====================================================
        # LIVE TRANSCRIPTION BOX
        # ====================================================

        self.transcription_card = ctk.CTkFrame(
            left,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        
        # Ensure it always stays visible between camera and controls.

        ctk.CTkLabel(
            self.transcription_card,
            text="LIVE TRANSCRIPT:",
            text_color=CYAN,
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 0))

        self.live_transcription_box = ctk.CTkTextbox(
            self.transcription_card,
            fg_color="transparent",
            text_color=TEXT,
            height=120,
            font=ctk.CTkFont(size=13),
            wrap="word",
            state="disabled"
        )
        self.live_transcription_box.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )
        
        self.live_transcription_box.configure(state="normal")
        self.live_transcription_box.insert("end", "Waiting for session...")
        self.live_transcription_box.configure(state="disabled")
        # ====================================================
        # CONTROL CARD
        # ====================================================

        control = ctk.CTkFrame(
            left,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )


        timer_area = ctk.CTkFrame(
            control,
            fg_color="transparent"
        )

        timer_area.pack(
            side="left",
            padx=25,
            pady=18
        )

        ctk.CTkLabel(
            timer_area,
            text="SESSION TIME",
            text_color=MUTED,
            font=ctk.CTkFont(
                size=9,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        self.timer_label = ctk.CTkLabel(
            timer_area,
            text="00:00",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        self.timer_label.pack(
            anchor="w"
        )

        button_area = ctk.CTkFrame(
            control,
            fg_color="transparent"
        )

        button_area.pack(
            side="right",
            padx=20,
            pady=18
        )

        self.start_button = ctk.CTkButton(
            button_area,
            text="Start Evaluation",
            width=190,
            height=48,
            corner_radius=10,
            fg_color=BLUE,
            hover_color="#2563EB",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.start_session
        )

        self.start_button.pack(
            side="right",
            padx=5
        )

        self.stop_button = ctk.CTkButton(
            button_area,
            text="End Session",
            width=160,
            height=48,
            corner_radius=10,
            fg_color="#991F1F",
            hover_color="#B91C1C",
            state="disabled",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.stop_session
        )

        self.stop_button.pack(
            side="right",
            padx=5
        )

        # ====================================================
        # APPLY PACKING FOR LEFT PANEL
        # ====================================================

        control.pack(side="bottom", fill="x", pady=(14, 0))
        self.transcription_card.pack(side="bottom", fill="x", pady=(14, 0))
        camera_card.pack(side="top", fill="both", expand=True)

        # ====================================================
        # RIGHT PANEL
        # ====================================================

        self.right_panel = ctk.CTkScrollableFrame(
            main,
            fg_color="transparent",
            corner_radius=0
        )

        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(14, 0)
        )

        ctk.CTkLabel(
            self.right_panel,
            text="Real-Time Performance",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        # ====================================================
        # METRIC CARDS
        # ====================================================

        self.face_value = self.create_metric_card(
            "Face Detection",
            "Waiting...",
            GREEN
        )

        (
            self.eye_value,
            self.eye_bar
        ) = self.create_metric_card(
            "Eye Contact",
            "0%",
            CYAN,
            True
        )

        self.head_value = self.create_metric_card(
            "Head Position",
            "Unknown",
            BLUE
        )

        (
            self.smile_value,
            self.smile_bar
        ) = self.create_metric_card(
            "Facial Expression",
            "0%",
            PURPLE,
            True
        )

        (
            self.posture_value,
            self.posture_bar
        ) = self.create_metric_card(
            "Posture",
            "0%",
            GREEN,
            True
        )

        self.gesture_value = self.create_metric_card(
            "Gesture Activity",
            "No Hands",
            YELLOW
        )

        # ====================================================
        # LIVE SCORE
        # ====================================================

        score_card = ctk.CTkFrame(
            self.right_panel,
            fg_color=CARD,
            corner_radius=17,
            border_width=1,
            border_color=BORDER
        )

        score_card.pack(
            fill="x",
            pady=(10, 15)
        )

        ctk.CTkLabel(
            score_card,
            text="LIVE PERFORMANCE SCORE",
            text_color=MUTED,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            pady=(17, 2)
        )

        self.score_label = ctk.CTkLabel(
            score_card,
            text="0",
            text_color=CYAN,
            font=ctk.CTkFont(
                size=48,
                weight="bold"
            )
        )

        self.score_label.pack()

        ctk.CTkLabel(
            score_card,
            text="/ 100",
            text_color=MUTED,
            font=ctk.CTkFont(
                size=12
            )
        ).pack()

        self.rating_label = ctk.CTkLabel(
            score_card,
            text="READY",
            text_color=MUTED,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        self.rating_label.pack(
            pady=(4, 17)
        )

        # ====================================================
        # INITIAL PERSON DISPLAY
        # ====================================================

        self.refresh_person_selector()

        self.update_person_display()


    # ========================================================
    # METRIC CARD
    # ========================================================

    def create_metric_card(
        self,
        title,
        value,
        accent_color,
        progress=False
    ):

        card = ctk.CTkFrame(
            self.right_panel,
            fg_color=CARD,
            corner_radius=13,
            border_width=1,
            border_color=BORDER
        )

        card.pack(
            fill="x",
            pady=5
        )

        row = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=17,
            pady=(13, 7)
        )

        ctk.CTkLabel(
            row,
            text=title,
            text_color=MUTED,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        value_label = ctk.CTkLabel(
            row,
            text=value,
            text_color=accent_color,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        value_label.pack(
            side="right"
        )

        if progress:

            bar = ctk.CTkProgressBar(
                card,
                height=6,
                corner_radius=3,
                progress_color=accent_color,
                fg_color="#263244"
            )

            bar.pack(
                fill="x",
                padx=17,
                pady=(0, 13)
            )

            bar.set(
                0
            )

            return (
                value_label,
                bar
            )

        ctk.CTkFrame(
            card,
            height=4,
            fg_color="transparent"
        ).pack()

        return value_label


    # ========================================================
    # EVALUATION TARGET LOCK
    # ========================================================

    def reset_target_lock(self):

        self.target_locked = False
        self.target_center = None
        self.target_face_area = 0.0
        self.target_missing_frames = 0
        self.target_status = "WAITING"

        if hasattr(self, "target_status_label"):
            self.target_status_label.configure(
                text="TARGET: WAITING",
                text_color=MUTED
            )


    def _face_geometry(self, face_landmarks, frame_width, frame_height):
        """Return bbox, center and area for a MediaPipe face."""

        xs = [
            max(0.0, min(1.0, landmark.x))
            for landmark in face_landmarks.landmark
        ]
        ys = [
            max(0.0, min(1.0, landmark.y))
            for landmark in face_landmarks.landmark
        ]

        if not xs or not ys:
            return None

        x1 = int(min(xs) * frame_width)
        y1 = int(min(ys) * frame_height)
        x2 = int(max(xs) * frame_width)
        y2 = int(max(ys) * frame_height)

        x1 = max(0, min(frame_width - 1, x1))
        y1 = max(0, min(frame_height - 1, y1))
        x2 = max(x1 + 1, min(frame_width, x2))
        y2 = max(y1 + 1, min(frame_height, y2))

        width = x2 - x1
        height = y2 - y1
        area = float(width * height)
        center = (
            (x1 + x2) / 2.0,
            (y1 + y2) / 2.0
        )

        return (x1, y1, x2, y2, center, area)


    def _select_primary_face(self, faces, frame_width, frame_height):
        """Select the most suitable face before a target has been locked."""

        if not faces:
            return None

        frame_center = (
            frame_width / 2.0,
            frame_height / 2.0
        )

        candidates = []

        for face in faces:
            geometry = self._face_geometry(
                face,
                frame_width,
                frame_height
            )

            if geometry is None:
                continue

            x1, y1, x2, y2, center, area = geometry

            distance = (
                ((center[0] - frame_center[0]) / max(frame_width, 1)) ** 2
                + ((center[1] - frame_center[1]) / max(frame_height, 1)) ** 2
            ) ** 0.5

            # Larger/closer faces are preferred, with a modest preference
            # for the person positioned near the camera center.
            area_score = min(1.0, area / (frame_width * frame_height * 0.20))
            center_score = max(0.0, 1.0 - distance / 0.70)
            score = area_score * 0.75 + center_score * 0.25

            candidates.append((score, face, geometry))

        if not candidates:
            return None

        return max(candidates, key=lambda item: item[0])


    def _select_locked_face(self, faces, frame_width, frame_height):
        """Track the already locked target by its previous face center."""

        if not faces or self.target_center is None:
            return None

        previous = self.target_center
        candidates = []

        for face in faces:
            geometry = self._face_geometry(
                face,
                frame_width,
                frame_height
            )

            if geometry is None:
                continue

            x1, y1, x2, y2, center, area = geometry

            distance = (
                ((center[0] - previous[0]) / max(frame_width, 1)) ** 2
                + ((center[1] - previous[1]) / max(frame_height, 1)) ** 2
            ) ** 0.5

            # Reject a face that is too far from the previous target.
            if distance > 0.35:
                continue

            area_ratio = (
                area / self.target_face_area
                if self.target_face_area > 1
                else 1.0
            )

            area_similarity = max(
                0.0,
                1.0 - min(1.0, abs(area_ratio - 1.0))
            )

            distance_score = max(
                0.0,
                1.0 - distance / 0.35
            )

            score = distance_score * 0.75 + area_similarity * 0.25
            candidates.append((score, face, geometry))

        if not candidates:
            return None

        return max(candidates, key=lambda item: item[0])


    def _draw_target_box(self, frame, geometry, label="EVALUATION TARGET"):
        """Draw the selected face and a clear target label."""

        if geometry is None:
            return

        x1, y1, x2, y2, _, _ = geometry

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (34, 197, 94),
            3
        )

        label_y = max(25, y1 - 8)

        cv2.rectangle(
            frame,
            (x1, max(0, label_y - 24)),
            (min(frame.shape[1], x1 + max(190, len(label) * 11)), label_y + 3),
            (16, 24, 36),
            -1
        )

        cv2.putText(
            frame,
            label,
            (x1 + 8, label_y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (34, 197, 94),
            2,
            cv2.LINE_AA
        )


    def update_target_status_ui(self, text, color):

        if hasattr(self, "target_status_label"):
            self.after(
                0,
                lambda: self.target_status_label.configure(
                    text=text,
                    text_color=color
                )
            )


    # ========================================================
    # CAMERA LOOP
    # ========================================================

    def camera_loop(self):

        while self.running:

            success, frame = (
                self.cap.read()
            )

            if not success:

                time.sleep(
                    0.01
                )

                continue

            frame = cv2.flip(
                frame,
                1
            )

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            frame_height, frame_width = frame.shape[:2]

            # =================================================
            # FACE DETECTION
            # =================================================

            frame, base_detected = (
                detect_face(
                    frame,
                    rgb
                )
            )

            # =================================================
            # FACE MESH / MULTI-FACE TARGETING
            # =================================================

            mesh_result = (
                self.face_mesh.process(
                    rgb
                )
            )

            all_faces = (
                mesh_result.multi_face_landmarks
                if mesh_result.multi_face_landmarks
                else []
            )

            target_face = None
            target_geometry = None

            if self.session.running:

                if not self.target_locked:

                    selected = self._select_primary_face(
                        all_faces,
                        frame_width,
                        frame_height
                    )

                    if selected is not None:

                        _, target_face, target_geometry = selected

                        (
                            _,
                            _,
                            _,
                            _,
                            center,
                            area
                        ) = target_geometry

                        self.target_locked = True
                        self.target_center = center
                        self.target_face_area = area
                        self.target_missing_frames = 0
                        self.target_status = "LOCKED"

                        self.update_target_status_ui(
                            "TARGET: LOCKED",
                            GREEN
                        )

                else:

                    selected = self._select_locked_face(
                        all_faces,
                        frame_width,
                        frame_height
                    )

                    if selected is not None:

                        _, target_face, target_geometry = selected

                        (
                            _,
                            _,
                            _,
                            _,
                            center,
                            area
                        ) = target_geometry

                        self.target_center = center
                        self.target_face_area = (
                            self.target_face_area * 0.80
                            + area * 0.20
                        )
                        self.target_missing_frames = 0

                    else:

                        self.target_missing_frames += 1

                        if (
                            self.target_missing_frames
                            <= self.target_max_missing_frames
                        ):

                            self.update_target_status_ui(
                                "TARGET: SEARCHING",
                                YELLOW
                            )

                        else:

                            # The target has been absent for long enough
                            # to safely allow a new target to be acquired.
                            self.target_locked = False
                            self.target_center = None
                            self.target_face_area = 0.0
                            self.target_missing_frames = 0
                            self.update_target_status_ui(
                                "TARGET: REACQUIRING",
                                YELLOW
                            )

            else:

                # Preview mode: select a face for display/analysis, but do
                # not lock it as the evaluation target until Start Evaluation.
                # This prevents a real face from incorrectly appearing as
                # "IGNORED" while the application is simply waiting to start.
                selected = self._select_primary_face(
                    all_faces,
                    frame_width,
                    frame_height
                )

                if selected is not None:
                    _, target_face, target_geometry = selected
                    self.update_target_status_ui(
                        "TARGET: PREVIEW",
                        CYAN
                    )
                else:
                    self.update_target_status_ui(
                        "TARGET: READY",
                        MUTED
                    )

            # -------------------------------------------------
            # Draw all non-target faces lightly so the user can
            # see that they are detected but ignored.
            # -------------------------------------------------

            for face in all_faces:

                geometry = self._face_geometry(
                    face,
                    frame_width,
                    frame_height
                )

                if geometry is None:
                    continue

                is_target = (
                    target_face is not None
                    and face is target_face
                )

                if is_target:
                    continue

                x1, y1, x2, y2, _, _ = geometry

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (120, 130, 145),
                    1
                )

                cv2.putText(
                    frame,
                    "IGNORED",
                    (x1, max(18, y1 - 6)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.45,
                    (150, 160, 175),
                    1,
                    cv2.LINE_AA
                )

            # =================================================
            # TARGET ANALYSIS
            # =================================================

            eye_contact = 0
            head_pose = "Unknown"
            smile_status = "Unknown"
            smile_score = 0

            if target_face is not None:

                self._draw_target_box(
                    frame,
                    target_geometry,
                    "EVALUATION TARGET" if self.session.running else "PREVIEW TARGET"
                )

                self.mp_drawing.draw_landmarks(
                    frame,
                    target_face,
                    self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=(
                        self.mp_drawing.DrawingSpec(
                            color=(35, 205, 160),
                            thickness=1,
                            circle_radius=1
                        )
                    )
                )

                # ---------------------------------------------
                # Eye contact
                # ---------------------------------------------

                (
                    eye_contact,
                    frame
                ) = calculate_eye_contact(
                    frame,
                    target_face
                )

                # ---------------------------------------------
                # Head pose
                # ---------------------------------------------

                (
                    head_pose,
                    _
                ) = estimate_head_pose(
                    frame,
                    target_face
                )

                # ---------------------------------------------
                # Smile
                # ---------------------------------------------

                (
                    smile_status,
                    _,
                    smile_score
                ) = detect_smile(
                    target_face
                )

            # =================================================
            # POSTURE
            # =================================================

            (
                posture_status,
                _,
                posture_score
            ) = detect_posture(
                frame,
                rgb
            )

            # =================================================
            # GESTURES
            # =================================================

            (
                gesture_status,
                _,
                gesture_score,
                hand_count
            ) = detect_hand_gesture(
                frame,
                rgb
            )

            # =================================================
            # TARGET PRESENCE
            # =================================================

            detected = target_face is not None

            # If a target is temporarily lost, do not immediately
            # turn the session into a zero score.  The SessionTracker
            # will continue receiving the current target-presence state.
            if self.session.running and self.target_locked and not detected:
                detected = False

            # =================================================
            # SESSION
            # =================================================

            if self.session.running:

                self.session.update(
                    detected,
                    eye_contact,
                    head_pose,
                    smile_score,
                    posture_score,
                    hand_count
                )

            # =================================================
            # SCORES
            # =================================================

            if head_pose == "Straight":

                head_score = 100

            elif head_pose != "Unknown":

                head_score = 60

            else:

                head_score = 0

            face_score = (
                100
                if detected
                else 0
            )

            overall_score = int(
                eye_contact * 0.35
                + head_score * 0.20
                + posture_score * 0.25
                + face_score * 0.10
                + smile_score * 0.05
                + gesture_score * 0.05
            )

            # =================================================
            # RATING
            # =================================================

            if not detected:

                rating = "NO TARGET"
                score_color = RED

            elif overall_score >= 85:

                rating = "EXCELLENT"
                score_color = GREEN

            elif overall_score >= 70:

                rating = "GOOD"
                score_color = CYAN

            elif overall_score >= 50:

                rating = "AVERAGE"
                score_color = YELLOW

            else:

                rating = "NEEDS IMPROVEMENT"
                score_color = RED

            # =================================================
            # UI DATA
            # =================================================

            self.after(
                0,
                self.update_metrics,
                detected,
                eye_contact,
                head_pose,
                smile_status,
                smile_score,
                posture_status,
                posture_score,
                gesture_status,
                overall_score,
                rating,
                score_color
            )

            # =================================================
            # CAMERA FRAME
            # =================================================

            self.current_frame = (
                cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )
            )


    # ========================================================
    # UPDATE CAMERA
    # ========================================================

    def update_camera(self):

        if self.current_frame is not None:

            if getattr(self, 'is_analyzing', False):
                pass # Do not override the 'Analyzing Speech' overlay
            else:
                image = Image.fromarray(
                    self.current_frame
                )

                width = max(
                    self.camera_label.winfo_width() - 20,
                    600
                )

                height = max(
                    self.camera_label.winfo_height() - 20,
                    400
                )

                image.thumbnail(
                    (
                        width,
                        height
                    )
                )

                camera_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=image.size
                )

                self.camera_label.configure(
                    image=camera_image,
                    text=""
                )

                self.camera_label.image = (
                    camera_image
                )

        if self.running:

            self.after(
                30,
                self.update_camera
            )


    # ========================================================
    # UPDATE METRICS
    # ========================================================

    def update_metrics(
        self,
        detected,
        eye_contact,
        head_pose,
        smile_status,
        smile_score,
        posture_status,
        posture_score,
        gesture_status,
        overall_score,
        rating,
        score_color
    ):

        if detected:

            self.face_value.configure(
                text="Detected",
                text_color=GREEN
            )

        else:

            self.face_value.configure(
                text="Not Detected",
                text_color=RED
            )

        # ----------------------------------------------------
        # Eye contact
        # ----------------------------------------------------

        self.eye_value.configure(
            text=f"{eye_contact}%"
        )

        self.eye_bar.set(
            max(
                0,
                min(
                    1,
                    eye_contact / 100
                )
            )
        )

        # ----------------------------------------------------
        # Head
        # ----------------------------------------------------

        self.head_value.configure(
            text=head_pose
        )

        # ----------------------------------------------------
        # Smile
        # ----------------------------------------------------

        self.smile_value.configure(
            text=(
                f"{smile_status}  "
                f"{smile_score}%"
            )
        )

        self.smile_bar.set(
            max(
                0,
                min(
                    1,
                    smile_score / 100
                )
            )
        )

        # ----------------------------------------------------
        # Posture
        # ----------------------------------------------------

        self.posture_value.configure(
            text=(
                f"{posture_status}  "
                f"{posture_score}%"
            )
        )

        self.posture_bar.set(
            max(
                0,
                min(
                    1,
                    posture_score / 100
                )
            )
        )

        # ----------------------------------------------------
        # Gesture
        # ----------------------------------------------------

        self.gesture_value.configure(
            text=gesture_status
        )

        # ----------------------------------------------------
        # Score
        # ----------------------------------------------------

        self.score_label.configure(
            text=str(overall_score),
            text_color=score_color
        )

        self.rating_label.configure(
            text=rating,
            text_color=score_color
        )


    # ========================================================
    # START SESSION
    # ========================================================

    def start_session(self):

        # ----------------------------------------------------
        # Person required
        # ----------------------------------------------------

        if not self.current_person:

            self.show_message(
                "Select Person",
                (
                    "Please create or select a person "
                    "before starting an evaluation."
                ),
                YELLOW
            )

            return

        if self.session.running:

            return

        # Start each evaluation with a fresh target lock.
        self.reset_target_lock()

        self.session.start()

        self.session_start_time = (
            time.time()
        )

        self.last_result = None
        self.last_feedback = None
        self.last_report_path = None
        self.speech_analysis = None

        # ------------------------------------------------
        # Start audio recording
        # ------------------------------------------------

        self.audio_file_path = os.path.join(
            REPORTS_FOLDER,
            "temp_session_audio.wav"
        )

        self.audio_recorder.start_recording(
            self.audio_file_path
        )

        self.start_button.configure(
            state="disabled"
        )

        self.stop_button.configure(
            state="normal"
        )

        self.person_menu.configure(
            state="disabled"
        )

        self.recording_label.configure(
            text="● RECORDING (Audio + Video)",
            text_color=RED
        )

        self.live_label.configure(
            text="●  EVALUATING",
            text_color=GREEN
        )

        # ------------------------------------------------
        # Start Live Transcription UI & Loop
        # ------------------------------------------------
        
        self.live_transcription_box.configure(state="normal")
        self.live_transcription_box.delete("1.0", "end")
        self.live_transcription_box.insert("end", "Listening...")
        self.live_transcription_box.configure(state="disabled")
        
        threading.Thread(
            target=self._live_transcription_loop,
            daemon=True
        ).start()

    def _live_transcription_loop(self):
        """Continuously transcribe the audio buffer to provide a live feed."""
        import tempfile
        import scipy.io.wavfile as wavfile
        
        temp_dir = tempfile.gettempdir()
        live_wav_path = os.path.join(temp_dir, "communication_ai_live.wav")
        last_text = ""
        
        while self.session.running:
            time.sleep(3.0)  # Update every 3 seconds
            
            if not self.session.running:
                break
                
            try:
                # Get audio buffer
                audio_array = self.audio_recorder.get_current_audio()
                if audio_array is None or len(audio_array) < 16000:
                    continue # Not enough audio yet
                
                # We save to a temporary wav because speech_engine.transcribe expects a file path
                wavfile.write(live_wav_path, self.audio_recorder.sample_rate, audio_array)
                
                if not self.session.running:
                    break
                    
                if self.speech_engine is None:
                    continue # Wait for engine to initialize
                    
                result = self.speech_engine.transcribe(live_wav_path)
                
                if isinstance(result, dict):
                    text = result.get("text", "").strip()
                elif isinstance(result, str):
                    text = result.strip()
                else:
                    text = ""
                
                if text and text != last_text:
                    last_text = text
                    
                    # Update text box safely on main thread
                    def update_ui(t=text):
                        if not self.session.running: 
                            return
                        self.live_transcription_box.configure(state="normal")
                        self.live_transcription_box.delete("1.0", "end")
                        self.live_transcription_box.insert("end", t)
                        self.live_transcription_box.see("end")  # Auto scroll
                        self.live_transcription_box.configure(state="disabled")
                        
                    self.after(0, update_ui)
                    
            except Exception as e:
                print(f"Live transcription error: {e}")
                
        # Clean up
        try:
            if os.path.exists(live_wav_path):
                os.remove(live_wav_path)
        except:
            pass


    # ========================================================
    # STOP SESSION
    # ========================================================

    def stop_session(self):

        if not self.session.running:

            return

        person_name = (
            self.current_person
        )

        self.last_result = (
            self.session.stop()
        )
        
        self.speech_analysis = None
        
        # Stop live transcription loop
        # (It will cleanly exit since session.running is now False)
        self.live_transcription_box.configure(state="normal")
        self.live_transcription_box.insert("end", "\n[Session Ended]")
        self.live_transcription_box.configure(state="disabled")

        # ------------------------------------------------
        # Stop audio recording
        # ------------------------------------------------

        audio_path = (
            self.audio_recorder.stop_recording()
        )

        if self.last_result:

            self.is_analyzing = True

            # Empty the camera label image and show big loading text on it
            import customtkinter as ctk_local
            self.camera_label.configure(
                image="",
                text="⏳ Analyzing Speech...",
                text_color="#EAB308", # Yellow
                font=ctk_local.CTkFont(size=22, weight="bold")
            )

            # Disable UI while processing
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="disabled")
            self.person_menu.configure(state="disabled")
            
            self.recording_label.configure(
                text="ANALYZING SPEECH...",
                text_color=YELLOW
            )
            
            self.live_label.configure(
                text="●  PROCESSING",
                text_color=YELLOW
            )

            # ------------------------------------------------
            # Run analysis in background thread
            # ------------------------------------------------
            threading.Thread(
                target=self._process_speech_and_finish,
                args=(audio_path, person_name),
                daemon=True
            ).start()
        
        else:
            self._finalize_session()
            
    def _process_speech_and_finish(self, audio_path, person_name):
        
        if audio_path and os.path.exists(audio_path):
            try:
                print("\nTranscribing audio...")
                transcript_result = (
                    self.speech_engine.transcribe(
                        audio_path
                    )
                )

                transcript_text = (
                    transcript_result.get("text", "")
                )

                words_data = (
                    transcript_result.get("words", [])
                )

                session_duration = (
                    self.last_result.get("duration", 0)
                )

                if transcript_text.strip():
                    print("Analyzing speech...")
                    self.speech_analysis = (
                        analyze_speech(
                            transcript_text,
                            words_data,
                            session_duration
                        )
                    )

            except Exception as e:
                print(f"Speech analysis error: {e}")

        # ------------------------------------------------
        # Add speech analysis to results
        # ------------------------------------------------
        if self.speech_analysis:
            self.last_result["speech_analysis"] = self.speech_analysis

        self.last_feedback = generate_feedback(self.last_result)

        # ------------------------------------------------
        # Create original report
        # ------------------------------------------------
        _, original_report_path = save_session(
            self.last_result,
            self.last_feedback
        )

        # ------------------------------------------------
        # Save in person database
        # ------------------------------------------------
        session_data = dict(self.last_result)
        session_data["person"] = person_name
        session_data["feedback"] = self.last_feedback

        self.save_person_session(
            person_name,
            session_data
        )

        self.last_report_path = (
            self.save_person_report_copy(
                person_name,
                original_report_path
            )
        )
        
        # Go back to main thread to update UI
        self.after(0, self._finalize_session, True)
            
    def _finalize_session(self, show_results=False):
        
        self.is_analyzing = False

        if show_results:
            self.show_results()

        self.start_button.configure(
            state="normal"
        )

        self.stop_button.configure(
            state="disabled"
        )

        self.person_menu.configure(
            state="normal"
        )

        self.recording_label.configure(
            text="READY",
            text_color=MUTED
        )

        self.reset_target_lock()

        self.live_label.configure(
            text="●  SYSTEM READY",
            text_color=GREEN
        )

        self.session_start_time = None


    # ========================================================
    # RESULTS
    # ========================================================

    def show_results(self):

        result = self.last_result
        feedback = self.last_feedback

        window = ctk.CTkToplevel(
            self
        )

        window.title(
            "Evaluation Results"
        )

        window.geometry(
            "980x760"
        )

        window.minsize(
            850,
            650
        )

        window.configure(
            fg_color=BG
        )

        # ====================================================
        # RESULT HEADER
        # ====================================================

        header = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(25, 10)
        )

        ctk.CTkLabel(
            header,
            text="Evaluation Complete",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text=(
                f"Communication performance report "
                f"for {self.current_person}"
            ),
            text_color=MUTED,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w"
        )

        # ====================================================
        # SCORE CARD
        # ====================================================

        score_card = ctk.CTkFrame(
            window,
            fg_color=CARD,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        score_card.pack(
            fill="x",
            padx=35,
            pady=10
        )

        score_left = ctk.CTkFrame(
            score_card,
            fg_color="transparent"
        )

        score_left.pack(
            side="left",
            padx=25,
            pady=20
        )

        ctk.CTkLabel(
            score_left,
            text="FINAL SCORE",
            text_color=MUTED,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        final_score = result.get(
            "final_score",
            0
        )

        if final_score >= 85:

            result_color = GREEN

        elif final_score >= 70:

            result_color = CYAN

        elif final_score >= 50:

            result_color = YELLOW

        else:

            result_color = RED

        ctk.CTkLabel(
            score_left,
            text=f"{final_score}/100",
            text_color=result_color,
            font=ctk.CTkFont(
                size=36,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            score_left,
            text=result.get(
                "rating",
                "Unknown"
            ).upper(),
            text_color=result_color,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            score_card,
            text=(
                "✓ Report saved for "
                + self.current_person
            ),
            text_color=GREEN,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            side="right",
            padx=30
        )

        # ====================================================
        # METRIC CARDS
        # ====================================================

        metrics = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )

        metrics.pack(
            fill="x",
            padx=30,
            pady=5
        )

        metric_values = [
            (
                "Eye Contact",
                result.get(
                    "eye_contact",
                    0
                )
            ),
            (
                "Head Stability",
                result.get(
                    "head_stability",
                    0
                )
            ),
            (
                "Posture",
                result.get(
                    "posture",
                    0
                )
            ),
            (
                "Expression",
                result.get(
                    "smile",
                    0
                )
            ),
            (
                "Gestures",
                result.get(
                    "gesture_usage",
                    0
                )
            )
        ]

        for i, (
            name,
            value
        ) in enumerate(
            metric_values
        ):

            metrics.grid_columnconfigure(
                i,
                weight=1
            )

            card = ctk.CTkFrame(
                metrics,
                fg_color=CARD,
                corner_radius=12,
                border_width=1,
                border_color=BORDER
            )

            card.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=5
            )

            ctk.CTkLabel(
                card,
                text=name,
                text_color=MUTED,
                font=ctk.CTkFont(
                    size=10
                )
            ).pack(
                pady=(12, 2)
            )

            ctk.CTkLabel(
                card,
                text=f"{value}%",
                text_color=TEXT,
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                )
            ).pack(
                pady=(0, 12)
            )

        # ====================================================
        # FEEDBACK
        # ====================================================

        feedback_frame = ctk.CTkScrollableFrame(
            window,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        feedback_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=15
        )

        ctk.CTkLabel(
            feedback_frame,
            text="AI Feedback",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            feedback_frame,
            text=feedback.get(
                "summary",
                ""
            ),
            text_color=SOFT_TEXT,
            justify="left",
            wraplength=800
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

        self.add_feedback_section(
            feedback_frame,
            "Strengths",
            feedback.get(
                "strengths",
                []
            ),
            GREEN,
            "✓"
        )

        self.add_feedback_section(
            feedback_frame,
            "Areas to Improve",
            feedback.get(
                "improvements",
                []
            ),
            YELLOW,
            "•"
        )

        self.add_feedback_section(
            feedback_frame,
            "Suggestions",
            feedback.get(
                "suggestions",
                []
            ),
            CYAN,
            "→"
        )

        # ====================================================
        # SPEECH ANALYSIS SECTION
        # ====================================================

        speech = result.get(
            "speech_analysis", None
        )

        if speech and speech.get(
            "word_count", 0
        ) > 0:

            speech_scores = speech.get(
                "speech_score", {}
            )

            speech_total = speech_scores.get(
                "total", 0.0
            )

            # ------------------------------------------------
            # Speech score color
            # ------------------------------------------------

            if speech_total >= 8.0:
                sp_color = GREEN
            elif speech_total >= 6.0:
                sp_color = CYAN
            elif speech_total >= 4.0:
                sp_color = YELLOW
            else:
                sp_color = RED

            # ------------------------------------------------
            # Speech header card
            # ------------------------------------------------

            speech_card = ctk.CTkFrame(
                feedback_frame,
                fg_color=CARD_2,
                corner_radius=14
            )

            speech_card.pack(
                fill="x",
                padx=15,
                pady=(20, 10)
            )

            # Title row
            speech_header = ctk.CTkFrame(
                speech_card,
                fg_color="transparent"
            )

            speech_header.pack(
                fill="x",
                padx=20,
                pady=(15, 5)
            )

            ctk.CTkLabel(
                speech_header,
                text="🎤 SPEECH ANALYSIS",
                text_color=TEXT,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                speech_header,
                text=(
                    f"Speech Score: "
                    f"{speech_total}/10"
                ),
                text_color=sp_color,
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                )
            ).pack(
                side="right"
            )

            # ------------------------------------------------
            # Sub-score cards
            # ------------------------------------------------

            sub_frame = ctk.CTkFrame(
                speech_card,
                fg_color="transparent"
            )

            sub_frame.pack(
                fill="x",
                padx=15,
                pady=10
            )

            sub_scores = [
                (
                    "Fluency",
                    speech_scores.get(
                        "fluency", 0
                    ),
                    3.0
                ),
                (
                    "Grammar",
                    speech_scores.get(
                        "grammar", 0
                    ),
                    2.5
                ),
                (
                    "Confidence",
                    speech_scores.get(
                        "confidence", 0
                    ),
                    2.0
                ),
                (
                    "Clarity",
                    speech_scores.get(
                        "clarity", 0
                    ),
                    2.5
                )
            ]

            for i, (
                name,
                val,
                max_val
            ) in enumerate(
                sub_scores
            ):

                sub_frame.columnconfigure(
                    i,
                    weight=1
                )

                mini_card = ctk.CTkFrame(
                    sub_frame,
                    fg_color=BG,
                    corner_radius=10
                )

                mini_card.grid(
                    row=0,
                    column=i,
                    padx=4,
                    pady=5,
                    sticky="nsew"
                )

                ctk.CTkLabel(
                    mini_card,
                    text=name,
                    text_color=MUTED,
                    font=ctk.CTkFont(
                        size=10
                    )
                ).pack(
                    pady=(8, 2)
                )

                ctk.CTkLabel(
                    mini_card,
                    text=(
                        f"{val}/{max_val}"
                    ),
                    text_color=TEXT,
                    font=ctk.CTkFont(
                        size=14,
                        weight="bold"
                    )
                ).pack(
                    pady=(0, 8)
                )

            # ------------------------------------------------
            # Speech stats row
            # ------------------------------------------------

            fluency_data = speech.get(
                "fluency", {}
            )

            pauses_data = speech.get(
                "pauses", {}
            )

            fillers_data = speech.get(
                "fillers", {}
            )

            grammar_data = speech.get(
                "grammar", {}
            )

            stats_text = (
                f"WPM: "
                f"{fluency_data.get('effective_wpm', 0)}"
                f"  |  Pauses: "
                f"{pauses_data.get('total_pauses', 0)}"
                f" (long: "
                f"{pauses_data.get('long_pauses', 0)})"
                f"  |  Fillers: "
                f"{fillers_data.get('total_fillers', 0)}"
                f"  |  Grammar Errors: "
                f"{grammar_data.get('total_errors', 0)}"
            )

            ctk.CTkLabel(
                speech_card,
                text=stats_text,
                text_color=SOFT_TEXT,
                font=ctk.CTkFont(
                    size=11
                )
            ).pack(
                padx=20,
                pady=(0, 12),
                anchor="w"
            )

            # ------------------------------------------------
            # Transcript display
            # ------------------------------------------------

            transcript = speech.get(
                "transcript", ""
            )

            if transcript:

                ctk.CTkLabel(
                    speech_card,
                    text="TRANSCRIPT",
                    text_color=MUTED,
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold"
                    )
                ).pack(
                    padx=20,
                    anchor="w"
                )

                transcript_box = ctk.CTkTextbox(
                    speech_card,
                    fg_color=BG,
                    text_color=SOFT_TEXT,
                    corner_radius=10,
                    height=100,
                    font=ctk.CTkFont(
                        size=12
                    ),
                    wrap="word"
                )

                transcript_box.pack(
                    fill="x",
                    padx=15,
                    pady=(5, 15)
                )

                transcript_box.insert(
                    "1.0",
                    transcript
                )

                transcript_box.configure(
                    state="disabled"
                )

        # ====================================================
        # RESULT BUTTONS
        # ====================================================

        buttons = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )

        buttons.pack(
            pady=(0, 20)
        )

        ctk.CTkButton(
            buttons,
            text="New Evaluation",
            width=150,
            height=42,
            corner_radius=10,
            fg_color=BLUE,
            hover_color="#2563EB",
            command=window.destroy
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="View Analytics",
            width=145,
            height=42,
            corner_radius=10,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            hover_color=CARD_2,
            command=lambda: (
                window.destroy(),
                self.show_analytics()
            )
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Open Reports",
            width=140,
            height=42,
            corner_radius=10,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            hover_color=CARD_2,
            command=self.open_reports_folder
        ).pack(
            side="left",
            padx=5
        )


    # ========================================================
    # FEEDBACK SECTION
    # ========================================================

    def add_feedback_section(
        self,
        parent,
        title,
        items,
        color,
        bullet
    ):

        ctk.CTkLabel(
            parent,
            text=title,
            text_color=color,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(12, 4)
        )

        if not items:

            items = [
                "No major issues detected."
            ]

        for item in items:

            ctk.CTkLabel(
                parent,
                text=f"{bullet}  {item}",
                text_color=TEXT,
                anchor="w",
                justify="left",
                wraplength=780
            ).pack(
                fill="x",
                padx=25,
                pady=3
            )


    # ========================================================
    # ANALYTICS CALCULATOR
    # ========================================================

    def calculate_person_analytics(
        self,
        person_name=None
    ):

        sessions = (
            self.get_person_sessions(
                person_name
            )
        )

        total = len(
            sessions
        )

        if total == 0:

            return {
                "total_sessions": 0,
                "average_score": 0,
                "best_score": 0,
                "improvement": 0,
                "scores": [],
                "average_eye_contact": 0,
                "average_head_stability": 0,
                "average_posture": 0,
                "average_smile": 0,
                "average_gesture_usage": 0,
                "average_face_presence": 0
            }

        def values_for(
            key
        ):

            values = []

            for session_data in sessions:

                try:

                    values.append(
                        float(
                            session_data.get(
                                key,
                                0
                            )
                        )
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    values.append(
                        0
                    )

            return values

        scores = values_for(
            "final_score"
        )

        eye = values_for(
            "eye_contact"
        )

        head = values_for(
            "head_stability"
        )

        posture = values_for(
            "posture"
        )

        smile = values_for(
            "smile"
        )

        gesture = values_for(
            "gesture_usage"
        )

        face = values_for(
            "face_presence"
        )

        average_score = (
            sum(scores) / len(scores)
        )

        best_score = max(
            scores
        )

        if len(scores) >= 2:

            improvement = (
                scores[-1]
                - scores[0]
            )

        else:

            improvement = 0

        return {
            "total_sessions": total,
            "average_score": round(
                average_score,
                1
            ),
            "best_score": round(
                best_score,
                1
            ),
            "improvement": round(
                improvement,
                1
            ),
            "scores": scores,
            "average_eye_contact": round(
                sum(eye) / len(eye),
                1
            ),
            "average_head_stability": round(
                sum(head) / len(head),
                1
            ),
            "average_posture": round(
                sum(posture) / len(posture),
                1
            ),
            "average_smile": round(
                sum(smile) / len(smile),
                1
            ),
            "average_gesture_usage": round(
                sum(gesture) / len(gesture),
                1
            ),
            "average_face_presence": round(
                sum(face) / len(face),
                1
            )
        }


    # ========================================================
    # ANALYTICS WINDOW
    # ========================================================

    def show_analytics(self):

        if not self.current_person:

            self.show_message(
                "Select Person",
                (
                    "Please create or select a person "
                    "to view their analytics."
                ),
                YELLOW
            )

            return

        analytics = (
            self.calculate_person_analytics(
                self.current_person
            )
        )

        window = ctk.CTkToplevel(
            self
        )

        window.title(
            "Progress Analytics"
        )

        window.geometry(
            "1250x820"
        )

        window.minsize(
            1050,
            720
        )

        window.configure(
            fg_color=BG
        )

        # ====================================================
        # HEADER
        # ====================================================

        header = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(25, 10)
        )

        header_left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        header_left.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            header_left,
            text="Progress Analytics",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header_left,
            text=(
                f"Performance history for "
                f"{self.current_person}"
            ),
            text_color=MUTED,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w"
        )

        # ====================================================
        # HEADER BUTTONS
        # ====================================================

        ctk.CTkButton(
            header,
            text="＋ NEW PERSON",
            width=160,
            height=42,
            corner_radius=10,
            fg_color="#172235",
            hover_color="#24334A",
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            command=lambda: (
                window.destroy(),
                self.show_new_person_dialog()
            )
        ).pack(
            side="right",
            padx=(10, 0)
        )

        # ====================================================
        # PERSON SELECTOR
        # ====================================================

        analytics_person_area = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )

        analytics_person_area.pack(
            fill="x",
            padx=35,
            pady=(0, 12)
        )

        ctk.CTkLabel(
            analytics_person_area,
            text="VIEWING PROFILE",
            text_color=MUTED,
            font=ctk.CTkFont(
                size=9,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=(0, 8)
        )

        analytics_menu = ctk.CTkOptionMenu(
            analytics_person_area,
            width=210,
            height=36,
            corner_radius=9,
            values=self.get_people_names(),
            fg_color=CARD,
            button_color=BLUE,
            button_hover_color="#2563EB",
            dropdown_fg_color=CARD,
            dropdown_hover_color=CARD_2,
            text_color=TEXT,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            command=lambda name: (
                self.select_person(name),
                window.destroy(),
                self.show_analytics()
            )
        )

        analytics_menu.set(
            self.current_person
        )

        analytics_menu.pack(
            side="left"
        )

        # ====================================================
        # NO SESSIONS
        # ====================================================

        if analytics[
            "total_sessions"
        ] == 0:

            empty = ctk.CTkFrame(
                window,
                fg_color=CARD,
                corner_radius=18,
                border_width=1,
                border_color=BORDER
            )

            empty.pack(
                fill="both",
                expand=True,
                padx=35,
                pady=20
            )

            ctk.CTkLabel(
                empty,
                text="No Evaluations Yet",
                text_color=TEXT,
                font=ctk.CTkFont(
                    size=24,
                    weight="bold"
                )
            ).pack(
                pady=(150, 10)
            )

            ctk.CTkLabel(
                empty,
                text=(
                    f"{self.current_person} does not have "
                    "any completed evaluations yet.\n\n"
                    "Start an evaluation to begin tracking "
                    "communication performance."
                ),
                text_color=MUTED,
                justify="center",
                font=ctk.CTkFont(
                    size=12
                )
            ).pack()

            ctk.CTkButton(
                empty,
                text="START EVALUATION",
                width=180,
                height=42,
                corner_radius=10,
                fg_color=BLUE,
                hover_color="#2563EB",
                command=window.destroy
            ).pack(
                pady=25
            )

            return

        # ====================================================
        # STAT CARDS
        # ====================================================

        stats = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            padx=35,
            pady=5
        )

        stat_data = [
            (
                "TOTAL SESSIONS",
                analytics[
                    "total_sessions"
                ],
                BLUE
            ),
            (
                "AVERAGE SCORE",
                analytics[
                    "average_score"
                ],
                CYAN
            ),
            (
                "BEST SCORE",
                analytics[
                    "best_score"
                ],
                GREEN
            ),
            (
                "IMPROVEMENT",
                (
                    f"+{analytics['improvement']}"
                    if analytics["improvement"] > 0
                    else str(
                        analytics["improvement"]
                    )
                ),
                (
                    GREEN
                    if analytics["improvement"] > 0
                    else (
                        RED
                        if analytics["improvement"] < 0
                        else YELLOW
                    )
                )
            )
        ]

        for i, (
            title,
            value,
            color
        ) in enumerate(
            stat_data
        ):

            stats.grid_columnconfigure(
                i,
                weight=1
            )

            card = ctk.CTkFrame(
                stats,
                fg_color=CARD,
                corner_radius=14,
                border_width=1,
                border_color=BORDER
            )

            card.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=5
            )

            ctk.CTkLabel(
                card,
                text=title,
                text_color=MUTED,
                font=ctk.CTkFont(
                    size=9,
                    weight="bold"
                )
            ).pack(
                pady=(15, 3)
            )

            ctk.CTkLabel(
                card,
                text=str(value),
                text_color=color,
                font=ctk.CTkFont(
                    size=25,
                    weight="bold"
                )
            ).pack(
                pady=(0, 15)
            )

        # ====================================================
        # CONTENT AREA
        # ====================================================

        content = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=15
        )

        content.grid_columnconfigure(
            0,
            weight=3
        )

        content.grid_columnconfigure(
            1,
            weight=2
        )

        content.grid_rowconfigure(
            0,
            weight=1
        )

        # ====================================================
        # TREND CARD
        # ====================================================

        trend_card = ctk.CTkFrame(
            content,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        trend_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        ctk.CTkLabel(
            trend_card,
            text="Performance Trend",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        ctk.CTkLabel(
            trend_card,
            text=(
                "Overall score across sessions"
            ),
            text_color=MUTED,
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        chart_frame = ctk.CTkFrame(
            trend_card,
            fg_color="transparent"
        )

        chart_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        figure = Figure(
            figsize=(6.5, 4.5),
            dpi=100
        )

        figure.patch.set_facecolor(
            CARD
        )

        axis = figure.add_subplot(
            111
        )

        axis.set_facecolor(
            CARD
        )

        scores = analytics[
            "scores"
        ]

        sessions_x = list(
            range(
                1,
                len(scores) + 1
            )
        )

        axis.plot(
            sessions_x,
            scores,
            marker="o",
            linewidth=2
        )

        axis.set_ylim(
            0,
            100
        )

        axis.set_xlabel(
            "Session",
            color=MUTED
        )

        axis.set_ylabel(
            "Score",
            color=MUTED
        )

        axis.grid(
            True,
            alpha=0.15
        )

        axis.tick_params(
            colors=MUTED
        )

        for spine in axis.spines.values():

            spine.set_color(
                BORDER
            )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # SKILLS CARD
        # ====================================================

        skill_card = ctk.CTkFrame(
            content,
            fg_color=CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )

        skill_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        ctk.CTkLabel(
            skill_card,
            text="Average Skills",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        ctk.CTkLabel(
            skill_card,
            text=(
                f"Performance across "
                f"{analytics['total_sessions']} sessions"
            ),
            text_color=MUTED,
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        skill_data = [
            (
                "Eye Contact",
                analytics[
                    "average_eye_contact"
                ],
                CYAN
            ),
            (
                "Head Stability",
                analytics[
                    "average_head_stability"
                ],
                BLUE
            ),
            (
                "Posture",
                analytics[
                    "average_posture"
                ],
                GREEN
            ),
            (
                "Facial Expression",
                analytics[
                    "average_smile"
                ],
                PURPLE
            ),
            (
                "Gesture Usage",
                analytics[
                    "average_gesture_usage"
                ],
                YELLOW
            ),
            (
                "Face Presence",
                analytics[
                    "average_face_presence"
                ],
                GREEN
            )
        ]

        for (
            name,
            value,
            color
        ) in skill_data:

            self.create_analytics_skill(
                skill_card,
                name,
                value,
                color
            )

        # ====================================================
        # TREND STATUS
        # ====================================================

        improvement = (
            analytics[
                "improvement"
            ]
        )

        if improvement > 0:

            trend_title = "Improving"

            trend_message = (
                "Overall communication performance "
                "is moving upward."
            )

            trend_color = GREEN

        elif improvement < 0:

            trend_title = "Needs Attention"

            trend_message = (
                "Recent performance is lower than "
                "the first recorded session."
            )

            trend_color = RED

        else:

            trend_title = "Stable"

            trend_message = (
                "Performance is currently stable. "
                "Continue practicing regularly."
            )

            trend_color = YELLOW

        trend_status = ctk.CTkFrame(
            skill_card,
            fg_color=CARD_2,
            corner_radius=12
        )

        trend_status.pack(
            fill="x",
            padx=18,
            pady=(18, 20)
        )

        ctk.CTkLabel(
            trend_status,
            text=trend_title.upper(),
            text_color=trend_color,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 3)
        )

        ctk.CTkLabel(
            trend_status,
            text=trend_message,
            text_color=SOFT_TEXT,
            justify="left",
            wraplength=300,
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )


    # ========================================================
    # ANALYTICS SKILL BAR
    # ========================================================

    def create_analytics_skill(
        self,
        parent,
        name,
        value,
        color
    ):

        row = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=18,
            pady=6
        )

        top = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )

        top.pack(
            fill="x"
        )

        ctk.CTkLabel(
            top,
            text=name,
            text_color=SOFT_TEXT,
            font=ctk.CTkFont(
                size=11
            )
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            top,
            text=f"{value}%",
            text_color=color,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            side="right"
        )

        bar = ctk.CTkProgressBar(
            row,
            height=6,
            corner_radius=3,
            progress_color=color,
            fg_color="#263244"
        )

        bar.pack(
            fill="x",
            pady=(5, 0)
        )

        bar.set(
            max(
                0,
                min(
                    1,
                    float(value) / 100
                )
            )
        )


    # ========================================================
    # SESSION HISTORY
    # ========================================================

    def show_history(self):

        if not self.current_person:

            self.show_message(
                "Select Person",
                (
                    "Please create or select a person "
                    "to view session history."
                ),
                YELLOW
            )

            return

        history = (
            self.get_person_sessions(
                self.current_person
            )
        )

        window = ctk.CTkToplevel(
            self
        )

        window.title(
            "Session History"
        )

        window.geometry(
            "950x700"
        )

        window.minsize(
            800,
            600
        )

        window.configure(
            fg_color=BG
        )

        # ====================================================
        # HEADER
        # ====================================================

        header = ctk.CTkFrame(
            window,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(28, 5)
        )

        ctk.CTkLabel(
            header,
            text="Session History",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text=(
                f"Previous evaluations for "
                f"{self.current_person}"
            ),
            text_color=MUTED,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # ====================================================
        # SESSION COUNT
        # ====================================================

        ctk.CTkLabel(
            window,
            text=(
                f"{len(history)} evaluation"
                + (
                    "s"
                    if len(history) != 1
                    else ""
                )
            ),
            text_color=CYAN,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=35,
            pady=(0, 12)
        )

        # ====================================================
        # HISTORY FRAME
        # ====================================================

        history_frame = ctk.CTkScrollableFrame(
            window,
            fg_color="transparent"
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        if not history:

            empty = ctk.CTkFrame(
                history_frame,
                fg_color=CARD,
                corner_radius=15,
                border_width=1,
                border_color=BORDER
            )

            empty.pack(
                fill="x",
                padx=5,
                pady=10
            )

            ctk.CTkLabel(
                empty,
                text="No evaluations yet",
                text_color=TEXT,
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                )
            ).pack(
                pady=(30, 5)
            )

            ctk.CTkLabel(
                empty,
                text=(
                    "Complete an evaluation to see "
                    "your session history here."
                ),
                text_color=MUTED
            ).pack(
                pady=(0, 30)
            )

            return

        # ----------------------------------------------------
        # Latest first
        # ----------------------------------------------------

        for session_data in reversed(
            history
        ):

            card = ctk.CTkFrame(
                history_frame,
                fg_color=CARD,
                corner_radius=14,
                border_width=1,
                border_color=BORDER
            )

            card.pack(
                fill="x",
                padx=5,
                pady=6
            )

            left = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            left.pack(
                side="left",
                fill="x",
                expand=True,
                padx=20,
                pady=15
            )

            ctk.CTkLabel(
                left,
                text=(
                    f"Session "
                    f"{session_data.get('id', '')}"
                ),
                text_color=TEXT,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                )
            ).pack(
                anchor="w"
            )

            ctk.CTkLabel(
                left,
                text=(
                    f"{session_data.get('date', '')}"
                    f"   •   "
                    f"{session_data.get('time', '')}"
                    f"   •   "
                    f"{session_data.get('duration', 0)} sec"
                ),
                text_color=MUTED,
                font=ctk.CTkFont(
                    size=11
                )
            ).pack(
                anchor="w",
                pady=(3, 0)
            )

            score = session_data.get(
                "final_score",
                0
            )

            if score >= 85:

                color = GREEN

            elif score >= 70:

                color = CYAN

            elif score >= 50:

                color = YELLOW

            else:

                color = RED

            ctk.CTkLabel(
                card,
                text=f"{score}/100",
                text_color=color,
                font=ctk.CTkFont(
                    size=22,
                    weight="bold"
                )
            ).pack(
                side="right",
                padx=25
            )

            ctk.CTkLabel(
                card,
                text=session_data.get(
                    "rating",
                    "Unknown"
                ),
                text_color=MUTED,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                )
            ).pack(
                side="right",
                padx=5
            )


    # ========================================================
    # OPEN REPORTS
    # ========================================================

    def open_reports_folder(self):

        if self.current_person:

            folder = (
                self.prepare_person_report_folder(
                    self.current_person
                )
            )

        elif self.last_report_path:

            folder = os.path.dirname(
                self.last_report_path
            )

        else:

            folder = REPORTS_FOLDER

            os.makedirs(
                folder,
                exist_ok=True
            )

        if os.path.exists(
            folder
        ):

            try:

                os.startfile(
                    folder
                )

            except Exception as e:

                print(
                    "Could not open reports folder:"
                )

                print(e)


    # ========================================================
    # TIMER
    # ========================================================

    def update_timer(self):

        if (
            self.session.running
            and self.session_start_time
        ):

            elapsed = int(
                time.time()
                - self.session_start_time
            )

            minutes = (
                elapsed // 60
            )

            seconds = (
                elapsed % 60
            )

            self.timer_label.configure(
                text=(
                    f"{minutes:02d}:"
                    f"{seconds:02d}"
                )
            )

        else:

            self.timer_label.configure(
                text="00:00"
            )

        if self.running:

            self.after(
                500,
                self.update_timer
            )


    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_application(self):

        self.running = False

        if self.session.running:

            self.session.stop()

        if self.cap.isOpened():

            self.cap.release()

        try:

            self.face_mesh.close()

        except Exception:

            pass

        self.destroy()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app = CommunicationAI()

    app.mainloop()