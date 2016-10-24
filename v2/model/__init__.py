import sys;
import os;
import os.path;
import json;
import logging;
import datetime, time;

import core;
import core.player;
import core.timeout;
import model.playlist;

import model.source;
import model.service;

CONFIG = {};
LAYOUTS={};
LAYOUT_SCHEDULE={};
LAYOUT_INTERVAL=[];

PLAYLISTS={};
PRIORITY={};
READY=False;


class ModelException(Exception): pass
class SourceException(ModelException): pass
class FileNotFoundException(SourceException): pass
class InvalidResponseException(SourceException): pass
class NetworkException(SourceException): pass
class DataException(SourceException): pass

class LayoutException(ModelException): pass
class PlaylistException(ModelException): pass


class ServiceFactory():
    SOURCE = None;
    def create_source(self):
        if( not ServiceFactory.SOURCE ):
            playlist_file="cache/playlist.json";
            ServiceFactory.SOURCE = model.source.FileSource(playlist_file);
        return ServiceFactory.SOURCE;

    def create_playlist_service(self):
        source = ServiceFactory().create_source();
        service = model.service.PlaylistService(source);
        service.load();
        return service;

    def create_content_service(self):
        source = ServiceFactory().create_source();
        service = model.service.ContentService(source);
        service.load();
        return service;

    def create_configuration_service(self):
        source = ServiceFactory().create_source();
        service = model.service.ConfigurationService(source);
        service.load();
        return service;

    def create_layout_service(self):
        source = ServiceFactory().create_source();
        service = model.service.LayoutService(source);
        service.load()
        return service;