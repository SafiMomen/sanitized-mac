WINDOW_STYLING = """

ApplicationTab, 
ConfigTab {
    width: 100%;
    height: 1fr;
    min-height: 10;

    background: black;
    color: white;
    padding: 1 2;

    layout: vertical;
}

Screen {
    background: black;
    color: white;
    padding: 1 2;
}

ApplicationTab Static,
ApplicationTab Input,
ApplicationTab Log {
    background: transparent;
    color: white;
    border: none;
}

ApplicationTab Button,
ConfigTab Button {
    background: transparent;
    border: none;
    min-width: 10;
    width: auto;
    padding: 0 1;
}

ApplicationTab Button:hover,
ConfigTab Button:hover {
    background: transparent;
    text-style: underline;
}

ApplicationTab Button:focus,
ConfigTab Button:hover {
    background: transparent;
    text-style: reverse;
}

ApplicationTab #title {
    height: 2;
    text-style: bold;
}

ApplicationTab #path {
    height: 3;
    margin-bottom: 1;
}

ApplicationTab #controls {
    height: 2;
}

ApplicationTab #status {
    height: 2;
}

ApplicationTab #log {
    height: 1fr;
    padding: 0 1;
}


"""