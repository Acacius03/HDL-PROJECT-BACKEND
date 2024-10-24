import sqlite3
from pathlib import Path
from face_recognition import load_image_file, face_locations, face_encodings, compare_faces
import numpy as np
from collections import Counter
from PIL import Image, ImageDraw

from Database import db

DEFAULT_ENCODINGS_PATH = Path("./output/encodings.pkl")

BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"

# Ensure directories exist
Path("training").mkdir(exist_ok=True)
# Path("./output").mkdir(exist_ok=True)
Path("validation").mkdir(exist_ok=True)

class FaceRecognition:
    def __init__(self, model: str = "hog") -> None:
        # Attributes
        self.model = model
        
        # Function Call
        self._create_table()
        self.record = self.load_encodings()

    # Read/Write to Database

    def _create_table(self) -> None:
        """Create a table for storing names and encodings if it doesn't exist."""
        db.execute('CREATE TABLE IF NOT EXISTS face_encodings (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, encoding BLOB NOT NULL)')

    def _save_encodings_batch(self, batch_data: list) -> None:
        """Save multiple encodings and names to the database in a single query."""
        db.execute_many("INSERT INTO face_encodings (name, encoding) VALUES (?, ?)", batch_data)

    def _save_encoding(self, name: str, encoding) -> None:
        """Save the encoding and name to the database."""
        encoding_bytes = sqlite3.Binary(encoding.tobytes())
        db.execute_with_params("INSERT INTO face_encodings (name, encoding) VALUES (?, ?)", (name, encoding_bytes))

    def load_encodings(self):
        """Load all encodings from the database."""
        face_encodings = db.get_multiple("SELECT name, encoding FROM face_encodings")

        names = []
        encodings = []
        for name, encoding_blob in face_encodings:
            names.append(name)
            encoding_array = np.frombuffer(encoding_blob, dtype=np.float64)
            encodings.append(encoding_array)

        return {"names": names, "encodings": encodings}

    # Face Recognition

    def scan_face_image(self, image_location: str) -> any:
        image = load_image_file(image_location)
        locations = face_locations(image, model=self.model)
        encodings = face_encodings(image, locations)
        return image, locations, encodings

    def _encoding_exists(self, encoding) -> bool:
        """Check if the encoding already exists in the database."""
        encoding_bytes = sqlite3.Binary(encoding.tobytes())
        return db.get_with_params("SELECT COUNT(*) FROM face_encodings WHERE encoding = ?", (encoding_bytes,))[0] > 0

    def encode_training_faces(self, folder_path: Path) -> None:
        batch_insert_data = []

        for filepath in folder_path.glob("*/*"):
            name = filepath.parent.name
            image = load_image_file(filepath)

            training_face_locations = face_locations(image, model=self.model)
            training_face_encodings = face_encodings(image, training_face_locations)

            print(f'\nChecking for face of {name}')
            for encoding in training_face_encodings:
                if not self._encoding_exists(encoding):
                    print(f'Saving face of {name}')
                    # Append the new encoding and name into the batch insert list
                    encoding_bytes = sqlite3.Binary(encoding.tobytes())
                    print(encoding_bytes)
                    batch_insert_data.append((name, encoding_bytes))
                else:
                    print(f'Face of {name} already exist!!')


        # Execute batch insert
        if batch_insert_data:
            self._save_encodings_batch(batch_insert_data)

    def recognize_faces(self, image_location: str) -> None:
        image, locations, encodings = self.scan_face_image(image_location)

        pillow_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pillow_image)

        for bounding_box, unknown_encoding in zip(locations, encodings):
            name = self._recognize_face(unknown_encoding, self.record)
            if not name: name = "Unknown"  # noqa: E701

            print(name, bounding_box)

            self._display_face(draw, bounding_box, name)

        del draw
        pillow_image.show()

    def _display_face(self, draw, bounding_box, name):
        top, right, bottom, left = bounding_box
        draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
        text_left, text_top, text_right, text_bottom = draw.textbbox(
            (left, bottom), name
        )
        draw.rectangle(
            ((text_left, text_top), (text_right, text_bottom)),
            fill="blue",
            outline="blue",
        )
        draw.text(
            (text_left, text_top),
            name,
            fill="white",
        )

    def _recognize_face(self, unknown_encoding, loaded_encodings):
        boolean_matches = compare_faces(
            loaded_encodings["encodings"], unknown_encoding
        )
        votes = Counter(
            name
            for match, name in zip(boolean_matches, loaded_encodings["names"])
            if match
        )
        if votes: return votes.most_common(1)[0][0]  # noqa: E701

    def validate(self):
        for filepath in Path("validation").rglob("*"):
            if filepath.is_file():
                self.recognize_faces(
                    image_location=str(filepath.absolute()), model=self.model
                )


# Example Usage:
FR = FaceRecognition()
# FR.encode_training_faces(Path('training'))
FR.validate()
db.close()
