import allure
from faker import Faker
from xmlschema import XMLSchemaChildrenValidationError

from templates.read_templates import user_iso_soap_xml, xsd_response, update_user_data_xml
from utils.soap import check_result_operation, check_result_update_operation

fake = Faker("ru_RU")


@allure.feature('SOAP')
class TestSoap:

    def test_niffler(self, soap_session):
        response = soap_session.post(
            soap_session.base_url,
            data=user_iso_soap_xml('qa_guru')
        )
        assert response.status_code == 200
        try:
            xsd_response('userResponse').validate(response.text)
        except XMLSchemaChildrenValidationError as xsd_e:
            raise AssertionError(xsd_e)

        assert check_result_operation(response.text, 'qa_guru')

    def test_update_user_data(self, soap_session):

        fullname = fake.name()

        response = soap_session.post(
            soap_session.base_url,
            data=update_user_data_xml(fullname)
        )
        assert response.status_code == 200
        print(response.text)
        try:
            xsd_response('userResponse').validate(response.text)
        except XMLSchemaChildrenValidationError as xsd_e:
            raise AssertionError(xsd_e)

        assert check_result_update_operation(response.text, fullname)
