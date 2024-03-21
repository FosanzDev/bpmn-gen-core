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
        """
        Sculptor class is responsible for creating the BPMN file from the process and graphic generated by the AI.
        Its task is as simple as adding the XML header and the definitions tag to the process and graphic.
        """
        pass

    def sculpt(self, process, graphic):
        """
        Wrap the process and graphic into a BPMN file.
        :param process: generated process
        :param graphic: generated graphic
        :return: BPMN file
        """
        return XML_HEADER + DEFINITIONS_TAG + process + graphic + "</definitions>"
