from RIAnalytics.settings import FILES_DIR
import os


def handle_uploaded_file(f, filename):
    with open(os.path.join(FILES_DIR,filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True
