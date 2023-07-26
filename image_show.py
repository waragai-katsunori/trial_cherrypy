import os
import cherrypy

class ImageServer(object):
    @cherrypy.expose
    def index(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Image Upload</title>
        </head>
        <body>
            <h1>Image Upload Example</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="image" accept="image/*">
                <input type="submit" value="Upload">
            </form>
        </body>
        </html>
        """

    @cherrypy.expose
    def upload(self, image):
        if not image.file:
            return "Please choose an image to upload."

        # Get the filename and extension
        filename = os.path.basename(image.filename)
        extension = os.path.splitext(filename)[1]

        # Create a unique filename
        import uuid
        unique_filename = str(uuid.uuid4()) + extension

        # Save the uploaded file to the 'images' folder
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", unique_filename)
        with open(save_path, 'wb') as f:
            while True:
                data = image.file.read(8192)
                if not data:
                    break
                f.write(data)

        return f"Image '{filename}' uploaded successfully as '{unique_filename}'."

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    cherrypy.quickstart(ImageServer())
