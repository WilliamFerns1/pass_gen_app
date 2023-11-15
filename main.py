from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import pyperclip
import random
import string

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Password:
    def __init__(self, length, uppercase, lowercase, digits, symbols):
        self.length = length
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.digits = digits
        self.symbols = symbols

    def generate(self):
        password = ''

        if self.uppercase:
            password += string.ascii_uppercase
        if self.lowercase:
            password += string.ascii_lowercase
        if self.digits:
            password += string.digits
        if self.symbols:
            password += string.punctuation

        completed_password = "".join(random.sample(password, self.length))
        return completed_password

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
def generate_password(
    request: Request,
    length: int = Form(...),
    uppercase: bool = Form(None),
    lowercase: bool = Form(None),
    digits: bool = Form(None),
    symbols: bool = Form(None),
):

    password_generator = Password(length, uppercase, lowercase, digits, symbols)
    generated_password = password_generator.generate()

    # Copy the password to the clipboard using pyperclip
    pyperclip.copy(generated_password)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "generated_password": generated_password}
    )
