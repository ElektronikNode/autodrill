#!/bin/bash

AUTODRILL_DIR="autodrill"
UI_DIR="${AUTODRILL_DIR}/ui"

pyuic4 -o ${UI_DIR}/ui_mainwindow.py ${UI_DIR}/mainwindow.ui
pyuic4 -o ${UI_DIR}/ui_dialogDrills.py ${UI_DIR}/dialogDrills.ui
pyuic4 -o ${UI_DIR}/ui_dialogDrillParameter.py ${UI_DIR}/dialogDrillParameter.ui
pyuic4 -o ${UI_DIR}/ui_dialogCamera.py ${UI_DIR}/dialogCamera.ui
