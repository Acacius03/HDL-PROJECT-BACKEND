import sqlite3
from pathlib import Path
from face_recognition import load_image_file, face_locations, face_encodings, compare_faces
import numpy as np
from collections import Counter
from PIL import Image, ImageDraw

from Database import Database

DEFAULT_ENCODINGS_PATH = Path("./output/encodings.pkl")

BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"

DATABASE_PATH = "db.sqlite3"
class FaceRecognition:
    def __init__(self, model: str = "hog") -> None:
        # Attributes
        self.model = model
        self.db = Database(DATABASE_PATH)

        self._create_table()

    # Read/Write to Database

    def _create_table(self) -> None:
        self.db.execute('CREATE TABLE IF NOT EXISTS face_encodings (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT NOT NULL, encoding BLOB NOT NULL)')

    def _save_encodings_batch(self, batch_data: list) -> None:
        self.db.execute_many("INSERT INTO face_encodings (uuid, encoding) VALUES (?, ?)", batch_data)

    def _save_encoding(self, uuid: str, encoding_bytes) -> None:
        self.db.execute_with_params("INSERT INTO face_encodings (uuid, encoding) VALUES (?, ?)", (uuid, encoding_bytes))

    def load_encodings(self):
        """Load all encodings from the database."""
        face_encodings = self.db.get_multiple("SELECT uuid, encoding FROM face_encodings")

        uuids = []
        encodings = []
        for uuid, encoding_blob in face_encodings:
            uuids.append(uuid)
            encoding_array = np.frombuffer(encoding_blob, dtype=np.float64)
            encodings.append(encoding_array)

        return {"uuid": uuids, "encodings": encodings}

    # Face Recognition
    def scan_face_image(self, image_location: any) -> any:
        image = load_image_file(image_location)
        locations = face_locations(image, model=self.model)
        encodings = face_encodings(image, locations)
        return image, locations, encodings

    def _encoding_exists(self, encoding_bytes) -> bool:
        """Check if the encoding already exists in the database."""
        return self.db.get_with_params("SELECT COUNT(*) FROM face_encodings WHERE encoding = ?", (encoding_bytes,))[0] > 0
   
    def encode_new_face(self, img_path: str ) -> bool:
        img_file = Path(img_path)
        if img_file.exists():
            uuid = img_file.parent.name
            _, _, encodings = self.scan_face_image(img_path)
            for encoding in encodings:
                encoding_bytes = sqlite3.Binary(encoding.tobytes())
                if not self._encoding_exists(encoding_bytes):
                    self._save_encoding(uuid, encoding_bytes)
                    return True
        return False

    def encode_training_faces(self, folder_path: str) -> None:
        batch_insert_data = []

        for filepath in Path(folder_path).glob("*/*"):
            uuid = filepath.parent.name
            _, _, encodings = self.scan_face_image(filepath)
            for encoding in encodings:
                encoding_bytes = sqlite3.Binary(encoding.tobytes())
                if not self._encoding_exists(encoding_bytes):
                    batch_insert_data.append((uuid, encoding_bytes))

        # Execute batch insert
        if batch_insert_data:
            self._save_encodings_batch(batch_insert_data)

    def recognize_faces(self, image_location: any) -> None:
        image, locations, encodings = self.scan_face_image(image_location)

        pillow_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pillow_image)

        for bounding_box, unknown_encoding in zip(locations, encodings):
            uuid = self._recognize_face(unknown_encoding, self.load_encodings())
            if not uuid: uuid = "Unknown"  # noqa: E701
            self._display_face(draw, bounding_box, uuid)

        del draw
        pillow_image.show()
        return uuid

    def _display_face(self, draw, bounding_box, uuid):
        top, right, bottom, left = bounding_box
        draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
        text_left, text_top, text_right, text_bottom = draw.textbbox(
            (left, bottom), uuid
        )
        draw.rectangle(
            ((text_left, text_top), (text_right, text_bottom)),
            fill="blue",
            outline="blue",
        )
        draw.text(
            (text_left, text_top),
            uuid,
            fill="white",
        )

    def _recognize_face(self, unknown_encoding, loaded_encodings):
        boolean_matches = compare_faces(
            loaded_encodings["encodings"], unknown_encoding
        )
        votes = Counter(
            uuid
            for match, uuid in zip(boolean_matches, loaded_encodings["uuid"])
            if match
        )
        if votes: return votes.most_common(1)[0][0]  # noqa: E701

    def validate(self, folder_path:str):
        for filepath in Path(folder_path).rglob("*"):
            if filepath.is_file():
                self.recognize_faces(
                    image_location=str(filepath.absolute()), model=self.model
                )

FR = FaceRecognition()