class Size():
    def __init__(self, width, height):
        self.width = width;
        self.height = height;

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

class Position():
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

class MediaInfo():
    def __init__(self, init):
        self.id = 0;
        self.name = None;
        self.file = None;
        self.path = None;
        self.duration = 0;
        self.meta = None;
        self.overlay = None;
        self.schedule = None;

        try:
            self.id = init['id'];
            self.name = init['name'];
            self.file = init['file'];
            self.path = init['path'];
            self.duration = init['duration'];
            self.meta = init['meta'];
            self.overlay = init['overlay'];
            self.schedule = init['schedule'];
        except:
            pass;

    def __eq__(self, media):
        if( media is None ): 
            return False;
        return self.id == media.id;

    def type(self):
        import os;
        extension = os.path.splitext(self.file)[1][1:].strip() 
        if( extension.lower() in ['mp4', 'flv', 'wmv'] ):
            return 'video';
        if( extension.lower() in ['jpeg', 'bmp', 'gif', 'png', 'tif'] ):
            return 'image';
        if( extension.lower() in ['php', 'html', 'asp'] ):
            return 'html';
        if( extension.lower() in ['swf'] ):
            return 'template';
        return None

    def __str__(self):
        if( self.type() is None): return "<Media %s>" % self.id;
        else:
            return "<%s %s>" % ( self.type().upper(), self.id );