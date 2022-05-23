# application start from here.
from website import NoteApp

app = NoteApp()

if __name__ == "__main__":
    app.run(debug=True)
