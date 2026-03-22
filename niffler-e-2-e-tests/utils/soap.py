from xml.etree import ElementTree


def check_result_operation(xml_str: str, etalon: str) -> bool:
    root = ElementTree.fromstring(xml_str)
    return root[1][0][0][1].text == etalon

def check_result_update_operation(xml_str: str, etalon: str) -> bool:
    root = ElementTree.fromstring(xml_str)
    return root[1][0][0][2].text == etalon