import webbrowser

def main():
    url = 'https://docs.python.org/'

    # Open URL in a new tab, if a browser window is already open.
    webbrowser.open_new_tab(url)

    # Open URL in new window, raising the window if possible.
    webbrowser.open_new(url)

if __name__ == "__main__":
    main()