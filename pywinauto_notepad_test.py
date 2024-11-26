import unittest
import logging
import time
from pywinauto import Desktop, Application

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class NotepadTest(unittest.TestCase):
    def setUp(self):
        # Define variables
        self.timeout = 5
        self.notepad_title = "Untitled"
        self.input_text = "Hello World"
        self.input_clear = ""

        # Start Notepad and store application and window references
        self.app = Application(backend="win32").start("notepad.exe")
        self.dlg = Desktop(backend="win32")[self.notepad_title]
        self.dlg.wait("visible", self.timeout)
        logging.info("Notepad application started and window detected.")

    def test_notepad_typing(self):
        logging.info("Running the test: test_notepad_typing.")
        
        # Type text and verify
        logging.info(f"Typing text: {self.input_text}")
        self.dlg.Edit.set_edit_text(self.input_text)
        actual_text = self.dlg.Edit.window_text()
        logging.info(f"Text in Notepad: {actual_text}")

        # Wait for 2 second before assertion
        time.sleep(2)
        
        self.assertEqual(
            self.input_text,
            actual_text,
            "The text in the Notepad edit field does not match the expected input."
        )
        logging.info("Assertion passed: Typed text matches the expected input.")

    def tearDown(self):
        # Handle title change and clear text
        try:
            updated_dlg = Desktop(backend="win32")[self.input_text]
            logging.info("Clearing the text in Notepad.")
            updated_dlg.Edit.set_edit_text(self.input_clear)
        except Exception as e:
            logging.warning(f"Failed to find the updated dialog: {e}")

        # Close Notepad without saving
        logging.info("Closing Notepad application.")
        try:
            self.dlg.close()
        except Exception as e:
            logging.error(f"Error during Notepad closure: {e}")

if __name__ == "__main__":
    unittest.main()
