# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import mock
import packaging.version

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api import label_pb2  # type: ignore
from google.api import launch_stage_pb2  # type: ignore
from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.monitoring_v3.services.notification_channel_service import (
    NotificationChannelServiceAsyncClient,
)
from google.cloud.monitoring_v3.services.notification_channel_service import (
    NotificationChannelServiceClient,
)
from google.cloud.monitoring_v3.services.notification_channel_service import pagers
from google.cloud.monitoring_v3.services.notification_channel_service import transports
from google.cloud.monitoring_v3.services.notification_channel_service.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.monitoring_v3.types import mutation_record
from google.cloud.monitoring_v3.types import notification
from google.cloud.monitoring_v3.types import notification_service
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
import google.auth


# TODO(busunkim): Once google-auth >= 1.25.0 is required transitively
# through google-api-core:
# - Delete the auth "less than" test cases
# - Delete these pytest markers (Make the "greater than or equal to" tests the default).
requires_google_auth_lt_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) >= packaging.version.parse("1.25.0"),
    reason="This test requires google-auth < 1.25.0",
)
requires_google_auth_gte_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) < packaging.version.parse("1.25.0"),
    reason="This test requires google-auth >= 1.25.0",
)


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert NotificationChannelServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        NotificationChannelServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        NotificationChannelServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        NotificationChannelServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        NotificationChannelServiceClient._get_default_mtls_endpoint(
            sandbox_mtls_endpoint
        )
        == sandbox_mtls_endpoint
    )
    assert (
        NotificationChannelServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class",
    [NotificationChannelServiceClient, NotificationChannelServiceAsyncClient,],
)
def test_notification_channel_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "monitoring.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.NotificationChannelServiceGrpcTransport, "grpc"),
        (transports.NotificationChannelServiceGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_notification_channel_service_client_service_account_always_use_jwt(
    transport_class, transport_name
):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize(
    "client_class",
    [NotificationChannelServiceClient, NotificationChannelServiceAsyncClient,],
)
def test_notification_channel_service_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "monitoring.googleapis.com:443"


def test_notification_channel_service_client_get_transport_class():
    transport = NotificationChannelServiceClient.get_transport_class()
    available_transports = [
        transports.NotificationChannelServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = NotificationChannelServiceClient.get_transport_class("grpc")
    assert transport == transports.NotificationChannelServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            NotificationChannelServiceClient,
            transports.NotificationChannelServiceGrpcTransport,
            "grpc",
        ),
        (
            NotificationChannelServiceAsyncClient,
            transports.NotificationChannelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    NotificationChannelServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(NotificationChannelServiceClient),
)
@mock.patch.object(
    NotificationChannelServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(NotificationChannelServiceAsyncClient),
)
def test_notification_channel_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(
        NotificationChannelServiceClient, "get_transport_class"
    ) as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(
        NotificationChannelServiceClient, "get_transport_class"
    ) as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            NotificationChannelServiceClient,
            transports.NotificationChannelServiceGrpcTransport,
            "grpc",
            "true",
        ),
        (
            NotificationChannelServiceAsyncClient,
            transports.NotificationChannelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            NotificationChannelServiceClient,
            transports.NotificationChannelServiceGrpcTransport,
            "grpc",
            "false",
        ),
        (
            NotificationChannelServiceAsyncClient,
            transports.NotificationChannelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    NotificationChannelServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(NotificationChannelServiceClient),
)
@mock.patch.object(
    NotificationChannelServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(NotificationChannelServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_notification_channel_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            NotificationChannelServiceClient,
            transports.NotificationChannelServiceGrpcTransport,
            "grpc",
        ),
        (
            NotificationChannelServiceAsyncClient,
            transports.NotificationChannelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_notification_channel_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (
            NotificationChannelServiceClient,
            transports.NotificationChannelServiceGrpcTransport,
            "grpc",
        ),
        (
            NotificationChannelServiceAsyncClient,
            transports.NotificationChannelServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_notification_channel_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


def test_notification_channel_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.monitoring_v3.services.notification_channel_service.transports.NotificationChannelServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = NotificationChannelServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


def test_list_notification_channel_descriptors(
    transport: str = "grpc",
    request_type=notification_service.ListNotificationChannelDescriptorsRequest,
):
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification_service.ListNotificationChannelDescriptorsResponse(
            next_page_token="next_page_token_value",
        )
        response = client.list_notification_channel_descriptors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == notification_service.ListNotificationChannelDescriptorsRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotificationChannelDescriptorsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_notification_channel_descriptors_from_dict():
    test_list_notification_channel_descriptors(request_type=dict)


def test_list_notification_channel_descriptors_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors), "__call__"
    ) as call:
        client.list_notification_channel_descriptors()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == notification_service.ListNotificationChannelDescriptorsRequest()
        )


@pytest.mark.asyncio
async def test_list_notification_channel_descriptors_async(
    transport: str = "grpc_asyncio",
    request_type=notification_service.ListNotificationChannelDescriptorsRequest,
):
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_service.ListNotificationChannelDescriptorsResponse(
                next_page_token="next_page_token_value",
            )
        )
        response = await client.list_notification_channel_descriptors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0] == notification_service.ListNotificationChannelDescriptorsRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotificationChannelDescriptorsAsyncPager)
    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_notification_channel_descriptors_async_from_dict():
    await test_list_notification_channel_descriptors_async(request_type=dict)


def test_list_notification_channel_descriptors_field_headers():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.ListNotificationChannelDescriptorsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors), "__call__"
    ) as call:
        call.return_value = (
            notification_service.ListNotificationChannelDescriptorsResponse()
        )
        client.list_notification_channel_descriptors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_notification_channel_descriptors_field_headers_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.ListNotificationChannelDescriptorsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_service.ListNotificationChannelDescriptorsResponse()
        )
        await client.list_notification_channel_descriptors(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_list_notification_channel_descriptors_flattened():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            notification_service.ListNotificationChannelDescriptorsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_notification_channel_descriptors(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_list_notification_channel_descriptors_flattened_error():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_notification_channel_descriptors(
            notification_service.ListNotificationChannelDescriptorsRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_list_notification_channel_descriptors_flattened_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            notification_service.ListNotificationChannelDescriptorsResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_service.ListNotificationChannelDescriptorsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_notification_channel_descriptors(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_list_notification_channel_descriptors_flattened_error_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_notification_channel_descriptors(
            notification_service.ListNotificationChannelDescriptorsRequest(),
            name="name_value",
        )


def test_list_notification_channel_descriptors_pager():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                ],
                next_page_token="abc",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[], next_page_token="def",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[notification.NotificationChannelDescriptor(),],
                next_page_token="ghi",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_notification_channel_descriptors(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(
            isinstance(i, notification.NotificationChannelDescriptor) for i in results
        )


def test_list_notification_channel_descriptors_pages():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                ],
                next_page_token="abc",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[], next_page_token="def",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[notification.NotificationChannelDescriptor(),],
                next_page_token="ghi",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_notification_channel_descriptors(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_notification_channel_descriptors_async_pager():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                ],
                next_page_token="abc",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[], next_page_token="def",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[notification.NotificationChannelDescriptor(),],
                next_page_token="ghi",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_notification_channel_descriptors(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, notification.NotificationChannelDescriptor) for i in responses
        )


@pytest.mark.asyncio
async def test_list_notification_channel_descriptors_async_pages():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channel_descriptors),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                ],
                next_page_token="abc",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[], next_page_token="def",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[notification.NotificationChannelDescriptor(),],
                next_page_token="ghi",
            ),
            notification_service.ListNotificationChannelDescriptorsResponse(
                channel_descriptors=[
                    notification.NotificationChannelDescriptor(),
                    notification.NotificationChannelDescriptor(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (
            await client.list_notification_channel_descriptors(request={})
        ).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_notification_channel_descriptor(
    transport: str = "grpc",
    request_type=notification_service.GetNotificationChannelDescriptorRequest,
):
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_descriptor), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannelDescriptor(
            name="name_value",
            type_="type__value",
            display_name="display_name_value",
            description="description_value",
        )
        response = client.get_notification_channel_descriptor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.GetNotificationChannelDescriptorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification.NotificationChannelDescriptor)
    assert response.name == "name_value"
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


def test_get_notification_channel_descriptor_from_dict():
    test_get_notification_channel_descriptor(request_type=dict)


def test_get_notification_channel_descriptor_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_descriptor), "__call__"
    ) as call:
        client.get_notification_channel_descriptor()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.GetNotificationChannelDescriptorRequest()


@pytest.mark.asyncio
async def test_get_notification_channel_descriptor_async(
    transport: str = "grpc_asyncio",
    request_type=notification_service.GetNotificationChannelDescriptorRequest,
):
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_descriptor), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannelDescriptor(
                name="name_value",
                type_="type__value",
                display_name="display_name_value",
                description="description_value",
            )
        )
        response = await client.get_notification_channel_descriptor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.GetNotificationChannelDescriptorRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification.NotificationChannelDescriptor)
    assert response.name == "name_value"
    assert response.type_ == "type__value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"


@pytest.mark.asyncio
async def test_get_notification_channel_descriptor_async_from_dict():
    await test_get_notification_channel_descriptor_async(request_type=dict)


def test_get_notification_channel_descriptor_field_headers():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.GetNotificationChannelDescriptorRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_descriptor), "__call__"
    ) as call:
        call.return_value = notification.NotificationChannelDescriptor()
        client.get_notification_channel_descriptor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_notification_channel_descriptor_field_headers_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.GetNotificationChannelDescriptorRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_descriptor), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannelDescriptor()
        )
        await client.get_notification_channel_descriptor(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_notification_channel_descriptor_flattened():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_descriptor), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannelDescriptor()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_notification_channel_descriptor(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_notification_channel_descriptor_flattened_error():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_notification_channel_descriptor(
            notification_service.GetNotificationChannelDescriptorRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_notification_channel_descriptor_flattened_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_descriptor), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannelDescriptor()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannelDescriptor()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_notification_channel_descriptor(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_notification_channel_descriptor_flattened_error_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_notification_channel_descriptor(
            notification_service.GetNotificationChannelDescriptorRequest(),
            name="name_value",
        )


def test_list_notification_channels(
    transport: str = "grpc",
    request_type=notification_service.ListNotificationChannelsRequest,
):
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification_service.ListNotificationChannelsResponse(
            next_page_token="next_page_token_value", total_size=1086,
        )
        response = client.list_notification_channels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.ListNotificationChannelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotificationChannelsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


def test_list_notification_channels_from_dict():
    test_list_notification_channels(request_type=dict)


def test_list_notification_channels_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels), "__call__"
    ) as call:
        client.list_notification_channels()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.ListNotificationChannelsRequest()


@pytest.mark.asyncio
async def test_list_notification_channels_async(
    transport: str = "grpc_asyncio",
    request_type=notification_service.ListNotificationChannelsRequest,
):
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_service.ListNotificationChannelsResponse(
                next_page_token="next_page_token_value", total_size=1086,
            )
        )
        response = await client.list_notification_channels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.ListNotificationChannelsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNotificationChannelsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.total_size == 1086


@pytest.mark.asyncio
async def test_list_notification_channels_async_from_dict():
    await test_list_notification_channels_async(request_type=dict)


def test_list_notification_channels_field_headers():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.ListNotificationChannelsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels), "__call__"
    ) as call:
        call.return_value = notification_service.ListNotificationChannelsResponse()
        client.list_notification_channels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_notification_channels_field_headers_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.ListNotificationChannelsRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_service.ListNotificationChannelsResponse()
        )
        await client.list_notification_channels(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_list_notification_channels_flattened():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification_service.ListNotificationChannelsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_notification_channels(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_list_notification_channels_flattened_error():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_notification_channels(
            notification_service.ListNotificationChannelsRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_list_notification_channels_flattened_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification_service.ListNotificationChannelsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_service.ListNotificationChannelsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_notification_channels(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_list_notification_channels_flattened_error_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_notification_channels(
            notification_service.ListNotificationChannelsRequest(), name="name_value",
        )


def test_list_notification_channels_pager():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                ],
                next_page_token="abc",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[], next_page_token="def",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[notification.NotificationChannel(),],
                next_page_token="ghi",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", ""),)),
        )
        pager = client.list_notification_channels(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, notification.NotificationChannel) for i in results)


def test_list_notification_channels_pages():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                ],
                next_page_token="abc",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[], next_page_token="def",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[notification.NotificationChannel(),],
                next_page_token="ghi",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_notification_channels(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_notification_channels_async_pager():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                ],
                next_page_token="abc",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[], next_page_token="def",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[notification.NotificationChannel(),],
                next_page_token="ghi",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_notification_channels(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, notification.NotificationChannel) for i in responses)


@pytest.mark.asyncio
async def test_list_notification_channels_async_pages():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_notification_channels),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                ],
                next_page_token="abc",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[], next_page_token="def",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[notification.NotificationChannel(),],
                next_page_token="ghi",
            ),
            notification_service.ListNotificationChannelsResponse(
                notification_channels=[
                    notification.NotificationChannel(),
                    notification.NotificationChannel(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_notification_channels(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_notification_channel(
    transport: str = "grpc",
    request_type=notification_service.GetNotificationChannelRequest,
):
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel(
            type_="type__value",
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            verification_status=notification.NotificationChannel.VerificationStatus.UNVERIFIED,
        )
        response = client.get_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.GetNotificationChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification.NotificationChannel)
    assert response.type_ == "type__value"
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.verification_status
        == notification.NotificationChannel.VerificationStatus.UNVERIFIED
    )


def test_get_notification_channel_from_dict():
    test_get_notification_channel(request_type=dict)


def test_get_notification_channel_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel), "__call__"
    ) as call:
        client.get_notification_channel()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.GetNotificationChannelRequest()


@pytest.mark.asyncio
async def test_get_notification_channel_async(
    transport: str = "grpc_asyncio",
    request_type=notification_service.GetNotificationChannelRequest,
):
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel(
                type_="type__value",
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                verification_status=notification.NotificationChannel.VerificationStatus.UNVERIFIED,
            )
        )
        response = await client.get_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.GetNotificationChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification.NotificationChannel)
    assert response.type_ == "type__value"
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.verification_status
        == notification.NotificationChannel.VerificationStatus.UNVERIFIED
    )


@pytest.mark.asyncio
async def test_get_notification_channel_async_from_dict():
    await test_get_notification_channel_async(request_type=dict)


def test_get_notification_channel_field_headers():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.GetNotificationChannelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel), "__call__"
    ) as call:
        call.return_value = notification.NotificationChannel()
        client.get_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_notification_channel_field_headers_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.GetNotificationChannelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel()
        )
        await client.get_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_notification_channel_flattened():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_notification_channel(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_notification_channel_flattened_error():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_notification_channel(
            notification_service.GetNotificationChannelRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_notification_channel_flattened_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_notification_channel(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_notification_channel_flattened_error_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_notification_channel(
            notification_service.GetNotificationChannelRequest(), name="name_value",
        )


def test_create_notification_channel(
    transport: str = "grpc",
    request_type=notification_service.CreateNotificationChannelRequest,
):
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel(
            type_="type__value",
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            verification_status=notification.NotificationChannel.VerificationStatus.UNVERIFIED,
        )
        response = client.create_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.CreateNotificationChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification.NotificationChannel)
    assert response.type_ == "type__value"
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.verification_status
        == notification.NotificationChannel.VerificationStatus.UNVERIFIED
    )


def test_create_notification_channel_from_dict():
    test_create_notification_channel(request_type=dict)


def test_create_notification_channel_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_channel), "__call__"
    ) as call:
        client.create_notification_channel()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.CreateNotificationChannelRequest()


@pytest.mark.asyncio
async def test_create_notification_channel_async(
    transport: str = "grpc_asyncio",
    request_type=notification_service.CreateNotificationChannelRequest,
):
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel(
                type_="type__value",
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                verification_status=notification.NotificationChannel.VerificationStatus.UNVERIFIED,
            )
        )
        response = await client.create_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.CreateNotificationChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification.NotificationChannel)
    assert response.type_ == "type__value"
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.verification_status
        == notification.NotificationChannel.VerificationStatus.UNVERIFIED
    )


@pytest.mark.asyncio
async def test_create_notification_channel_async_from_dict():
    await test_create_notification_channel_async(request_type=dict)


def test_create_notification_channel_field_headers():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.CreateNotificationChannelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_channel), "__call__"
    ) as call:
        call.return_value = notification.NotificationChannel()
        client.create_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_notification_channel_field_headers_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.CreateNotificationChannelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_channel), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel()
        )
        await client.create_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_create_notification_channel_flattened():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_notification_channel(
            name="name_value",
            notification_channel=notification.NotificationChannel(type_="type__value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].notification_channel == notification.NotificationChannel(
            type_="type__value"
        )


def test_create_notification_channel_flattened_error():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_notification_channel(
            notification_service.CreateNotificationChannelRequest(),
            name="name_value",
            notification_channel=notification.NotificationChannel(type_="type__value"),
        )


@pytest.mark.asyncio
async def test_create_notification_channel_flattened_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_notification_channel(
            name="name_value",
            notification_channel=notification.NotificationChannel(type_="type__value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].notification_channel == notification.NotificationChannel(
            type_="type__value"
        )


@pytest.mark.asyncio
async def test_create_notification_channel_flattened_error_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_notification_channel(
            notification_service.CreateNotificationChannelRequest(),
            name="name_value",
            notification_channel=notification.NotificationChannel(type_="type__value"),
        )


def test_update_notification_channel(
    transport: str = "grpc",
    request_type=notification_service.UpdateNotificationChannelRequest,
):
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel(
            type_="type__value",
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            verification_status=notification.NotificationChannel.VerificationStatus.UNVERIFIED,
        )
        response = client.update_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.UpdateNotificationChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification.NotificationChannel)
    assert response.type_ == "type__value"
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.verification_status
        == notification.NotificationChannel.VerificationStatus.UNVERIFIED
    )


def test_update_notification_channel_from_dict():
    test_update_notification_channel(request_type=dict)


def test_update_notification_channel_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_channel), "__call__"
    ) as call:
        client.update_notification_channel()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.UpdateNotificationChannelRequest()


@pytest.mark.asyncio
async def test_update_notification_channel_async(
    transport: str = "grpc_asyncio",
    request_type=notification_service.UpdateNotificationChannelRequest,
):
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel(
                type_="type__value",
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                verification_status=notification.NotificationChannel.VerificationStatus.UNVERIFIED,
            )
        )
        response = await client.update_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.UpdateNotificationChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification.NotificationChannel)
    assert response.type_ == "type__value"
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.verification_status
        == notification.NotificationChannel.VerificationStatus.UNVERIFIED
    )


@pytest.mark.asyncio
async def test_update_notification_channel_async_from_dict():
    await test_update_notification_channel_async(request_type=dict)


def test_update_notification_channel_field_headers():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.UpdateNotificationChannelRequest()

    request.notification_channel.name = "notification_channel.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_channel), "__call__"
    ) as call:
        call.return_value = notification.NotificationChannel()
        client.update_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "notification_channel.name=notification_channel.name/value",
    ) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_notification_channel_field_headers_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.UpdateNotificationChannelRequest()

    request.notification_channel.name = "notification_channel.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_channel), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel()
        )
        await client.update_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        "x-goog-request-params",
        "notification_channel.name=notification_channel.name/value",
    ) in kw["metadata"]


def test_update_notification_channel_flattened():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_notification_channel(
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            notification_channel=notification.NotificationChannel(type_="type__value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])
        assert args[0].notification_channel == notification.NotificationChannel(
            type_="type__value"
        )


def test_update_notification_channel_flattened_error():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_notification_channel(
            notification_service.UpdateNotificationChannelRequest(),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            notification_channel=notification.NotificationChannel(type_="type__value"),
        )


@pytest.mark.asyncio
async def test_update_notification_channel_flattened_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_notification_channel(
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            notification_channel=notification.NotificationChannel(type_="type__value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])
        assert args[0].notification_channel == notification.NotificationChannel(
            type_="type__value"
        )


@pytest.mark.asyncio
async def test_update_notification_channel_flattened_error_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_notification_channel(
            notification_service.UpdateNotificationChannelRequest(),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
            notification_channel=notification.NotificationChannel(type_="type__value"),
        )


def test_delete_notification_channel(
    transport: str = "grpc",
    request_type=notification_service.DeleteNotificationChannelRequest,
):
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.DeleteNotificationChannelRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_notification_channel_from_dict():
    test_delete_notification_channel(request_type=dict)


def test_delete_notification_channel_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_channel), "__call__"
    ) as call:
        client.delete_notification_channel()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.DeleteNotificationChannelRequest()


@pytest.mark.asyncio
async def test_delete_notification_channel_async(
    transport: str = "grpc_asyncio",
    request_type=notification_service.DeleteNotificationChannelRequest,
):
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.DeleteNotificationChannelRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_notification_channel_async_from_dict():
    await test_delete_notification_channel_async(request_type=dict)


def test_delete_notification_channel_field_headers():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.DeleteNotificationChannelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_channel), "__call__"
    ) as call:
        call.return_value = None
        client.delete_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_notification_channel_field_headers_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.DeleteNotificationChannelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_channel), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_notification_channel_flattened():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_notification_channel(
            name="name_value", force=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].force == True


def test_delete_notification_channel_flattened_error():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_notification_channel(
            notification_service.DeleteNotificationChannelRequest(),
            name="name_value",
            force=True,
        )


@pytest.mark.asyncio
async def test_delete_notification_channel_flattened_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_notification_channel(
            name="name_value", force=True,
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].force == True


@pytest.mark.asyncio
async def test_delete_notification_channel_flattened_error_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_notification_channel(
            notification_service.DeleteNotificationChannelRequest(),
            name="name_value",
            force=True,
        )


def test_send_notification_channel_verification_code(
    transport: str = "grpc",
    request_type=notification_service.SendNotificationChannelVerificationCodeRequest,
):
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_notification_channel_verification_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.send_notification_channel_verification_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == notification_service.SendNotificationChannelVerificationCodeRequest()
        )

    # Establish that the response is the type that we expect.
    assert response is None


def test_send_notification_channel_verification_code_from_dict():
    test_send_notification_channel_verification_code(request_type=dict)


def test_send_notification_channel_verification_code_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_notification_channel_verification_code), "__call__"
    ) as call:
        client.send_notification_channel_verification_code()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == notification_service.SendNotificationChannelVerificationCodeRequest()
        )


@pytest.mark.asyncio
async def test_send_notification_channel_verification_code_async(
    transport: str = "grpc_asyncio",
    request_type=notification_service.SendNotificationChannelVerificationCodeRequest,
):
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_notification_channel_verification_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.send_notification_channel_verification_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == notification_service.SendNotificationChannelVerificationCodeRequest()
        )

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_send_notification_channel_verification_code_async_from_dict():
    await test_send_notification_channel_verification_code_async(request_type=dict)


def test_send_notification_channel_verification_code_field_headers():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.SendNotificationChannelVerificationCodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_notification_channel_verification_code), "__call__"
    ) as call:
        call.return_value = None
        client.send_notification_channel_verification_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_send_notification_channel_verification_code_field_headers_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.SendNotificationChannelVerificationCodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_notification_channel_verification_code), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.send_notification_channel_verification_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_send_notification_channel_verification_code_flattened():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_notification_channel_verification_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.send_notification_channel_verification_code(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_send_notification_channel_verification_code_flattened_error():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.send_notification_channel_verification_code(
            notification_service.SendNotificationChannelVerificationCodeRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_send_notification_channel_verification_code_flattened_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.send_notification_channel_verification_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.send_notification_channel_verification_code(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_send_notification_channel_verification_code_flattened_error_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.send_notification_channel_verification_code(
            notification_service.SendNotificationChannelVerificationCodeRequest(),
            name="name_value",
        )


def test_get_notification_channel_verification_code(
    transport: str = "grpc",
    request_type=notification_service.GetNotificationChannelVerificationCodeRequest,
):
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_verification_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification_service.GetNotificationChannelVerificationCodeResponse(
            code="code_value",
        )
        response = client.get_notification_channel_verification_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == notification_service.GetNotificationChannelVerificationCodeRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, notification_service.GetNotificationChannelVerificationCodeResponse
    )
    assert response.code == "code_value"


def test_get_notification_channel_verification_code_from_dict():
    test_get_notification_channel_verification_code(request_type=dict)


def test_get_notification_channel_verification_code_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_verification_code), "__call__"
    ) as call:
        client.get_notification_channel_verification_code()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == notification_service.GetNotificationChannelVerificationCodeRequest()
        )


@pytest.mark.asyncio
async def test_get_notification_channel_verification_code_async(
    transport: str = "grpc_asyncio",
    request_type=notification_service.GetNotificationChannelVerificationCodeRequest,
):
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_verification_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_service.GetNotificationChannelVerificationCodeResponse(
                code="code_value",
            )
        )
        response = await client.get_notification_channel_verification_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert (
            args[0]
            == notification_service.GetNotificationChannelVerificationCodeRequest()
        )

    # Establish that the response is the type that we expect.
    assert isinstance(
        response, notification_service.GetNotificationChannelVerificationCodeResponse
    )
    assert response.code == "code_value"


@pytest.mark.asyncio
async def test_get_notification_channel_verification_code_async_from_dict():
    await test_get_notification_channel_verification_code_async(request_type=dict)


def test_get_notification_channel_verification_code_field_headers():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.GetNotificationChannelVerificationCodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_verification_code), "__call__"
    ) as call:
        call.return_value = (
            notification_service.GetNotificationChannelVerificationCodeResponse()
        )
        client.get_notification_channel_verification_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_notification_channel_verification_code_field_headers_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.GetNotificationChannelVerificationCodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_verification_code), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_service.GetNotificationChannelVerificationCodeResponse()
        )
        await client.get_notification_channel_verification_code(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_notification_channel_verification_code_flattened():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_verification_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            notification_service.GetNotificationChannelVerificationCodeResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_notification_channel_verification_code(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_notification_channel_verification_code_flattened_error():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_notification_channel_verification_code(
            notification_service.GetNotificationChannelVerificationCodeRequest(),
            name="name_value",
        )


@pytest.mark.asyncio
async def test_get_notification_channel_verification_code_flattened_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_notification_channel_verification_code), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = (
            notification_service.GetNotificationChannelVerificationCodeResponse()
        )

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification_service.GetNotificationChannelVerificationCodeResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_notification_channel_verification_code(
            name="name_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_notification_channel_verification_code_flattened_error_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_notification_channel_verification_code(
            notification_service.GetNotificationChannelVerificationCodeRequest(),
            name="name_value",
        )


def test_verify_notification_channel(
    transport: str = "grpc",
    request_type=notification_service.VerifyNotificationChannelRequest,
):
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel(
            type_="type__value",
            name="name_value",
            display_name="display_name_value",
            description="description_value",
            verification_status=notification.NotificationChannel.VerificationStatus.UNVERIFIED,
        )
        response = client.verify_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.VerifyNotificationChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification.NotificationChannel)
    assert response.type_ == "type__value"
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.verification_status
        == notification.NotificationChannel.VerificationStatus.UNVERIFIED
    )


def test_verify_notification_channel_from_dict():
    test_verify_notification_channel(request_type=dict)


def test_verify_notification_channel_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_notification_channel), "__call__"
    ) as call:
        client.verify_notification_channel()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.VerifyNotificationChannelRequest()


@pytest.mark.asyncio
async def test_verify_notification_channel_async(
    transport: str = "grpc_asyncio",
    request_type=notification_service.VerifyNotificationChannelRequest,
):
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel(
                type_="type__value",
                name="name_value",
                display_name="display_name_value",
                description="description_value",
                verification_status=notification.NotificationChannel.VerificationStatus.UNVERIFIED,
            )
        )
        response = await client.verify_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == notification_service.VerifyNotificationChannelRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, notification.NotificationChannel)
    assert response.type_ == "type__value"
    assert response.name == "name_value"
    assert response.display_name == "display_name_value"
    assert response.description == "description_value"
    assert (
        response.verification_status
        == notification.NotificationChannel.VerificationStatus.UNVERIFIED
    )


@pytest.mark.asyncio
async def test_verify_notification_channel_async_from_dict():
    await test_verify_notification_channel_async(request_type=dict)


def test_verify_notification_channel_field_headers():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.VerifyNotificationChannelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_notification_channel), "__call__"
    ) as call:
        call.return_value = notification.NotificationChannel()
        client.verify_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_verify_notification_channel_field_headers_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = notification_service.VerifyNotificationChannelRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_notification_channel), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel()
        )
        await client.verify_notification_channel(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_verify_notification_channel_flattened():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.verify_notification_channel(
            name="name_value", code="code_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].code == "code_value"


def test_verify_notification_channel_flattened_error():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.verify_notification_channel(
            notification_service.VerifyNotificationChannelRequest(),
            name="name_value",
            code="code_value",
        )


@pytest.mark.asyncio
async def test_verify_notification_channel_flattened_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.verify_notification_channel), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = notification.NotificationChannel()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            notification.NotificationChannel()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.verify_notification_channel(
            name="name_value", code="code_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].code == "code_value"


@pytest.mark.asyncio
async def test_verify_notification_channel_flattened_error_async():
    client = NotificationChannelServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.verify_notification_channel(
            notification_service.VerifyNotificationChannelRequest(),
            name="name_value",
            code="code_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.NotificationChannelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = NotificationChannelServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.NotificationChannelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = NotificationChannelServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.NotificationChannelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = NotificationChannelServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.NotificationChannelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = NotificationChannelServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.NotificationChannelServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.NotificationChannelServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NotificationChannelServiceGrpcTransport,
        transports.NotificationChannelServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport, transports.NotificationChannelServiceGrpcTransport,
    )


def test_notification_channel_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.NotificationChannelServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_notification_channel_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.monitoring_v3.services.notification_channel_service.transports.NotificationChannelServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.NotificationChannelServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_notification_channel_descriptors",
        "get_notification_channel_descriptor",
        "list_notification_channels",
        "get_notification_channel",
        "create_notification_channel",
        "update_notification_channel",
        "delete_notification_channel",
        "send_notification_channel_verification_code",
        "get_notification_channel_verification_code",
        "verify_notification_channel",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_notification_channel_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.monitoring_v3.services.notification_channel_service.transports.NotificationChannelServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.NotificationChannelServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_notification_channel_service_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.monitoring_v3.services.notification_channel_service.transports.NotificationChannelServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.NotificationChannelServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id="octopus",
        )


def test_notification_channel_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.monitoring_v3.services.notification_channel_service.transports.NotificationChannelServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.NotificationChannelServiceTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_notification_channel_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        NotificationChannelServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_notification_channel_service_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        NotificationChannelServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NotificationChannelServiceGrpcTransport,
        transports.NotificationChannelServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_notification_channel_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NotificationChannelServiceGrpcTransport,
        transports.NotificationChannelServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_notification_channel_service_transport_auth_adc_old_google_auth(
    transport_class,
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.NotificationChannelServiceGrpcTransport, grpc_helpers),
        (transports.NotificationChannelServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_notification_channel_service_transport_create_channel(
    transport_class, grpc_helpers
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "monitoring.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/monitoring",
                "https://www.googleapis.com/auth/monitoring.read",
            ),
            scopes=["1", "2"],
            default_host="monitoring.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NotificationChannelServiceGrpcTransport,
        transports.NotificationChannelServiceGrpcAsyncIOTransport,
    ],
)
def test_notification_channel_service_grpc_transport_client_cert_source_for_mtls(
    transport_class,
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_notification_channel_service_host_no_port():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="monitoring.googleapis.com"
        ),
    )
    assert client.transport._host == "monitoring.googleapis.com:443"


def test_notification_channel_service_host_with_port():
    client = NotificationChannelServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="monitoring.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "monitoring.googleapis.com:8000"


def test_notification_channel_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.NotificationChannelServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_notification_channel_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.NotificationChannelServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NotificationChannelServiceGrpcTransport,
        transports.NotificationChannelServiceGrpcAsyncIOTransport,
    ],
)
def test_notification_channel_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.NotificationChannelServiceGrpcTransport,
        transports.NotificationChannelServiceGrpcAsyncIOTransport,
    ],
)
def test_notification_channel_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_notification_channel_path():
    project = "squid"
    notification_channel = "clam"
    expected = "projects/{project}/notificationChannels/{notification_channel}".format(
        project=project, notification_channel=notification_channel,
    )
    actual = NotificationChannelServiceClient.notification_channel_path(
        project, notification_channel
    )
    assert expected == actual


def test_parse_notification_channel_path():
    expected = {
        "project": "whelk",
        "notification_channel": "octopus",
    }
    path = NotificationChannelServiceClient.notification_channel_path(**expected)

    # Check that the path construction is reversible.
    actual = NotificationChannelServiceClient.parse_notification_channel_path(path)
    assert expected == actual


def test_notification_channel_descriptor_path():
    project = "oyster"
    channel_descriptor = "nudibranch"
    expected = "projects/{project}/notificationChannelDescriptors/{channel_descriptor}".format(
        project=project, channel_descriptor=channel_descriptor,
    )
    actual = NotificationChannelServiceClient.notification_channel_descriptor_path(
        project, channel_descriptor
    )
    assert expected == actual


def test_parse_notification_channel_descriptor_path():
    expected = {
        "project": "cuttlefish",
        "channel_descriptor": "mussel",
    }
    path = NotificationChannelServiceClient.notification_channel_descriptor_path(
        **expected
    )

    # Check that the path construction is reversible.
    actual = NotificationChannelServiceClient.parse_notification_channel_descriptor_path(
        path
    )
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = NotificationChannelServiceClient.common_billing_account_path(
        billing_account
    )
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = NotificationChannelServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = NotificationChannelServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(folder=folder,)
    actual = NotificationChannelServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = NotificationChannelServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = NotificationChannelServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = NotificationChannelServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = NotificationChannelServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = NotificationChannelServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(project=project,)
    actual = NotificationChannelServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = NotificationChannelServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = NotificationChannelServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = NotificationChannelServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = NotificationChannelServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = NotificationChannelServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.NotificationChannelServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = NotificationChannelServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.NotificationChannelServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = NotificationChannelServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
