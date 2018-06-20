import mock

from snipssonos.use_cases.inject_entities import InjectEntitiesUseCase
from snipssonos.entities.artist import Artist
from snipssonos.shared.response_object import ResponseSuccess, ResponseFailure
from snipssonos.use_cases.request_objects import InjectEntitiesRequestFactory

ARTIST_ENTITY_NAME = "snips/artist"


@mock.patch('snipssonos.services.spotify.music_customization_service.SpotifyCustomizationService')
@mock.patch('snipssonos.services.injection_service.InjectEntitiesService')
def test_inject_entities_successful(custom_mock, injection_mock):
    custom_mock_instance = custom_mock.return_value
    injection_mock_instance = injection_mock.return_value

    custom_mock_instance.fetch_top_artist.return_value = [Artist("uri_1", "Kendrick Lamar"),
                                                          Artist("uri_2", "Beyonce")]

    inject_entities_request = InjectEntitiesRequestFactory.from_dict({'entity_name': ARTIST_ENTITY_NAME})
    inject_entities = InjectEntitiesUseCase(custom_mock_instance, injection_mock_instance)

    response = inject_entities.process_request(inject_entities_request)

    assert isinstance(response, ResponseSuccess)


@mock.patch('snipssonos.services.spotify.music_customization_service.SpotifyCustomizationService')
@mock.patch('snipssonos.services.injection_service.InjectEntitiesService')
def test_inject_entities_failure(custom_mock, injection_mock):
    custom_mock_instance = custom_mock.return_value
    injection_mock_instance = injection_mock.return_value

    custom_mock_instance.fetch_top_artist.return_value = []
    inject_entities_request = InjectEntitiesRequestFactory.from_dict({'entity_name': ARTIST_ENTITY_NAME})
    inject_entities = InjectEntitiesUseCase(custom_mock_instance, injection_mock_instance)

    response = inject_entities.process_request(inject_entities_request)

    assert isinstance(response, ResponseFailure)
    assert response.value['message'] == "An error occurred"
