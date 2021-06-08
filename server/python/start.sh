#!/bin/bash
echo "Starting CherryPy..."
supervisord -c /wav2vec2-server/cherrypy.conf
sleep infinity
