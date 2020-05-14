#!/usr/bin/env bash
set -e
args=("$@")

function installTestPythonDependencies {
    pip3 install -r "./requirements.txt"
}

function runPyTest {
    echo "Printing service"
    echo ${args[1]}
    echo "########################"
    installTestPythonDependencies
    python -m pytest --html=report.html ./src/tests/test_base.py -s
    echo "------------------------"
}

function sendMail {
    echo "Printing Send Mail"
    echo "########################"
    python ./src/utils/send_mail.py
    echo "------------------------"
    echo "Removing report"
    echo "########################"
    #rm -rf report.html
    echo "------------------------"
}

case "$1" in
#    apitest) runPyTest && sendMail || sendMail;;
#    sendmail) sendMail
     apitest) runPyTest
esac
