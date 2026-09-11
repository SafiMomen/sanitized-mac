WINDOW_STYLING = """

Screen {
    background: black;
    color: white;
    padding: 1 2;
}

Static, Input, Log {
    background: transparent;
    color: white;
    border: none;
}

Button {
    background: transparent;
    border: none;
    min-width: 10;
    width: auto;
    padding: 0 1;
}

Button:hover {
    background: transparent;
    text-style: underline;
}

Button:focus {
    background: transparent;
    text-style: reverse;
}

#title {
    height: 2;
    text-style: bold;
}

#path {
    height: 3;
    margin-bottom: 1;
}

#controls {
    height: 2;
}

#status {
    height: 2;
}

#log {
    padding: 0 1;
}

"""