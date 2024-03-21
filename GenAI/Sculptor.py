import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

XML_HEADER = """<?xml version="1.0" encoding="UTF-8"?>"""
DEFINITIONS_TAG = """<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:adonis="http://www.boc-group.com"
    xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
    xmlns:model="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:omgdc="http://www.omg.org/spec/DD/20100524/DC"
    xmlns:omgdi="http://www.omg.org/spec/DD/20100524/DI"
    xmlns:semantic="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:xmi="http://www.omg.org/XMI"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    id="definition__4"
    typeLanguage="http://www.w3.org/2001/XMLSchema"
    xsi:schemaLocation="http://www.omg.org/spec/BPMN/20100524/MODEL http://www.omg.org/spec/BPMN/2.0/20100501/BPMN20.xsd"
    targetNamespace="http://www.boc-group.com">"""


class Sculptor:

    def __init__(self):
        pass

    def sculpt(self, process, graphic):
        with open(parent_dir + '/static/process.bpmn', 'w') as file:
            file.write(XML_HEADER)
            file.write(DEFINITIONS_TAG)
            file.write(process)
            file.write(graphic)
            file.write("</definitions>")


        return "Process and graphic have been sculpted into a BPMN file"