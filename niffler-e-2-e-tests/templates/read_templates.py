import xmlschema
from jinja2 import Environment, select_autoescape, FileSystemLoader
from xmlschema import XMLSchema11

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
def user_iso_soap_xml(request: str) -> str:
    template = env.get_template('/templates/xml/request.xml')
    return template.render({'user_soap': request})

def update_user_data_xml(update_user_data: str) -> str:
    template = env.get_template('/templates/xml/update_user_data.xml')
    return template.render({'full_name_soap_user': update_user_data})

def xsd_response(operation: str) -> XMLSchema11:
    envelope_xsd = env.get_template('./templates/xsd/envelope.xsd')
    user_iso_code_xsd_response = envelope_xsd.render({
        'operation_xsd': f'{operation}.xsd',
        'operation': operation})

    with open('./templates/xsd/temp.xsd', 'w') as f:
        f.write(user_iso_code_xsd_response)

    return xmlschema.XMLSchema11('./templates/xsd/temp.xsd')
