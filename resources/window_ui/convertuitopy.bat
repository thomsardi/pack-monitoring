@echo off
pyuic5 -x gui.ui -o gui.py
pyuic5 -x serialsetting.ui -o serialsetting.py
pyuic5 -x serialmonitor.ui -o serialmonitor.py
pyuic5 -x uploader.ui -o uploader.py
pyuic5 -x mainscreen.ui -o mainscreen.py
pyuic5 -x mainwindow.ui -o mainwindow.py
pyuic5 -x homewindow.ui -o homewindow.py
pyuic5 -x databaseconnection.ui -o databaseconnection.py
pyuic5 -x batterydetails.ui -o batterydetails.py
pyuic5 -x rmswindow.ui -o rmswindow.py
pyuic5 -x chargerwindow.ui -o chargerwindow.py
pyuic5 -x inverterwindow.ui -o inverterwindow.py
pyuic5 -x maininfowindow.ui -o maininfowindow.py
pyuic5 -x mainwindowtest.ui -o mainwindowtest.py
