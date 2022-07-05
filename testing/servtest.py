# start a simple http server at port 9000:

if __name__ in "__main__":
    import http.server
    import socketserver

    PORT = 9000
    DIRECTORY = "./"


    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)


    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

