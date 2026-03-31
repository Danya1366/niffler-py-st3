import json
import pytest
import allure
import requests

from faker import Faker
from fixtures.kafka_fixtures import kafka
from models.user import UserName
from allure import step


@pytest.mark.xdist_group("group1")
@allure.feature('Регистрация')
@allure.story('KAFKA')
class TestAuthRegistrationKafkaTest:
    @allure.title('Проверка сообщения после успешной регистрации')
    def test_message_should_be_produced_to_kafka_after_successful_registration(self, auth_client, kafka):
        username = Faker().user_name()
        password = Faker().password(special_chars=False)
        print(kafka.list_topics_names())

        topic_partitions = kafka.subscribe_listen_new_offsets("users")

        result = auth_client.register(username, password)
        assert result.status_code == 201

        event = kafka.log_msg_and_json(topic_partitions)

        with step("Check that message from kafka exists"):
            assert event != '' and event != b''

        with step("Check message content"):
            UserName.model_validate(json.loads(event.decode('utf8')))
            assert json.loads(event.decode('utf8'))['username'] == username

    @allure.title('Проверка ошибки после повторной регистрации')
    def test_second_registration(self, auth_client, kafka):
        username = Faker().user_name()
        password = Faker().password(special_chars=False)
        print(kafka.list_topics_names())

        topic_partitions = kafka.subscribe_listen_new_offsets("users")

        result = auth_client.register(username, password)
        assert result.status_code == 201

        event = kafka.log_msg_and_json(topic_partitions)

        with step("Check that message from kafka exists"):
            assert event != '' and event != b''

        with step("Check message content"):
            UserName.model_validate(json.loads(event.decode('utf8')))
            assert json.loads(event.decode('utf8'))['username'] == username

        with step("Try to register same user again"):
            try:
                auth_client.register(username, password)
                assert False, "Expected 400 error but got success"
            except requests.exceptions.HTTPError as e:
                assert e.response.status_code == 400
                assert f"Username `{username}` already exists" in e.response.text

            # Проверяем что второе сообщение тоже пришло в Kafka
        with step("Check that second message was produced to kafka"):
            event_2 = kafka.log_msg_and_json(topic_partitions)
            assert event_2 != '' and event_2 != b''

        with step("Check second message content"):
            UserName.model_validate(json.loads(event_2.decode('utf8')))
            assert json.loads(event_2.decode('utf8'))['username'] == username

    @allure.title('Проверка сообщения после регистрации в Кафка и проверка пользователя в базе данных')
    def test_registration_and_user_in_db(self, auth_client, kafka, auth_db):
        username = Faker().user_name()
        password = Faker().password(special_chars=False)

        topic_partitions = kafka.subscribe_listen_new_offsets("users")

        result = auth_client.register(username, password)
        assert result.status_code == 201

        event = kafka.log_msg_and_json(topic_partitions)

        with step("Check that message from kafka exists"):
            assert event != '' and event != b''

        with step("Check message content"):
            UserName.model_validate(json.loads(event.decode('utf8')))
            assert json.loads(event.decode('utf8'))['username'] == username

        with step("Check user in DB"):
            users = auth_db.get_user(username)
            assert len(users) == 1
            assert users[0].username == username
