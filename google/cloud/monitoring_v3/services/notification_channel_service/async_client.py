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
from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api import label_pb2  # type: ignore
from google.api import launch_stage_pb2  # type: ignore
from google.cloud.monitoring_v3.services.notification_channel_service import pagers
from google.cloud.monitoring_v3.types import mutation_record
from google.cloud.monitoring_v3.types import notification
from google.cloud.monitoring_v3.types import notification_service
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from .transports.base import NotificationChannelServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import NotificationChannelServiceGrpcAsyncIOTransport
from .client import NotificationChannelServiceClient


class NotificationChannelServiceAsyncClient:
    """The Notification Channel API provides access to configuration
    that controls how messages related to incidents are sent.
    """

    _client: NotificationChannelServiceClient

    DEFAULT_ENDPOINT = NotificationChannelServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = NotificationChannelServiceClient.DEFAULT_MTLS_ENDPOINT

    notification_channel_path = staticmethod(
        NotificationChannelServiceClient.notification_channel_path
    )
    parse_notification_channel_path = staticmethod(
        NotificationChannelServiceClient.parse_notification_channel_path
    )
    notification_channel_descriptor_path = staticmethod(
        NotificationChannelServiceClient.notification_channel_descriptor_path
    )
    parse_notification_channel_descriptor_path = staticmethod(
        NotificationChannelServiceClient.parse_notification_channel_descriptor_path
    )
    common_billing_account_path = staticmethod(
        NotificationChannelServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        NotificationChannelServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(
        NotificationChannelServiceClient.common_folder_path
    )
    parse_common_folder_path = staticmethod(
        NotificationChannelServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        NotificationChannelServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        NotificationChannelServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        NotificationChannelServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        NotificationChannelServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        NotificationChannelServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        NotificationChannelServiceClient.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            NotificationChannelServiceAsyncClient: The constructed client.
        """
        return NotificationChannelServiceClient.from_service_account_info.__func__(NotificationChannelServiceAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            NotificationChannelServiceAsyncClient: The constructed client.
        """
        return NotificationChannelServiceClient.from_service_account_file.__func__(NotificationChannelServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> NotificationChannelServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            NotificationChannelServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(NotificationChannelServiceClient).get_transport_class,
        type(NotificationChannelServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, NotificationChannelServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the notification channel service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.NotificationChannelServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = NotificationChannelServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_notification_channel_descriptors(
        self,
        request: notification_service.ListNotificationChannelDescriptorsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNotificationChannelDescriptorsAsyncPager:
        r"""Lists the descriptors for supported channel types.
        The use of descriptors makes it possible for new channel
        types to be dynamically added.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.ListNotificationChannelDescriptorsRequest`):
                The request object. The
                `ListNotificationChannelDescriptors` request.
            name (:class:`str`):
                Required. The REST resource name of the parent from
                which to retrieve the notification channel descriptors.
                The expected syntax is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                Note that this
                `names <https://cloud.google.com/monitoring/api/v3#project_name>`__
                the parent container in which to look for the
                descriptors; to retrieve a single descriptor by name,
                use the
                [GetNotificationChannelDescriptor][google.monitoring.v3.NotificationChannelService.GetNotificationChannelDescriptor]
                operation, instead.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.notification_channel_service.pagers.ListNotificationChannelDescriptorsAsyncPager:
                The ListNotificationChannelDescriptors response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = notification_service.ListNotificationChannelDescriptorsRequest(
            request
        )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_notification_channel_descriptors,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListNotificationChannelDescriptorsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_notification_channel_descriptor(
        self,
        request: notification_service.GetNotificationChannelDescriptorRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification.NotificationChannelDescriptor:
        r"""Gets a single channel descriptor. The descriptor
        indicates which fields are expected / permitted for a
        notification channel of the given type.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.GetNotificationChannelDescriptorRequest`):
                The request object. The
                `GetNotificationChannelDescriptor` response.
            name (:class:`str`):
                Required. The channel type for which to execute the
                request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/notificationChannelDescriptors/[CHANNEL_TYPE]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.NotificationChannelDescriptor:
                A description of a notification
                channel. The descriptor includes the
                properties of the channel and the set of
                labels or fields that must be specified
                to configure channels of a given type.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = notification_service.GetNotificationChannelDescriptorRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_notification_channel_descriptor,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_notification_channels(
        self,
        request: notification_service.ListNotificationChannelsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNotificationChannelsAsyncPager:
        r"""Lists the notification channels that have been
        created for the project.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.ListNotificationChannelsRequest`):
                The request object. The `ListNotificationChannels`
                request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                on which to execute the request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This names the container in which to look for the
                notification channels; it does not name a specific
                channel. To query a specific channel by REST resource
                name, use the
                [``GetNotificationChannel``][google.monitoring.v3.NotificationChannelService.GetNotificationChannel]
                operation.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.notification_channel_service.pagers.ListNotificationChannelsAsyncPager:
                The ListNotificationChannels response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = notification_service.ListNotificationChannelsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_notification_channels,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListNotificationChannelsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_notification_channel(
        self,
        request: notification_service.GetNotificationChannelRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification.NotificationChannel:
        r"""Gets a single notification channel. The channel
        includes the relevant configuration details with which
        the channel was created. However, the response may
        truncate or omit passwords, API keys, or other private
        key matter and thus the response may not be 100%
        identical to the information that was supplied in the
        call to the create method.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.GetNotificationChannelRequest`):
                The request object. The `GetNotificationChannel`
                request.
            name (:class:`str`):
                Required. The channel for which to execute the request.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/notificationChannels/[CHANNEL_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.NotificationChannel:
                A NotificationChannel is a medium through which an alert is
                   delivered when a policy violation is detected.
                   Examples of channels include email, SMS, and
                   third-party messaging applications. Fields containing
                   sensitive information like authentication tokens or
                   contact info are only partially populated on
                   retrieval.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = notification_service.GetNotificationChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_notification_channel,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_notification_channel(
        self,
        request: notification_service.CreateNotificationChannelRequest = None,
        *,
        name: str = None,
        notification_channel: notification.NotificationChannel = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification.NotificationChannel:
        r"""Creates a new notification channel, representing a
        single notification endpoint such as an email address,
        SMS number, or PagerDuty service.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.CreateNotificationChannelRequest`):
                The request object. The `CreateNotificationChannel`
                request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                on which to execute the request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This names the container into which the channel will be
                written, this does not name the newly created channel.
                The resulting channel's name will have a normalized
                version of this field as a prefix, but will add
                ``/notificationChannels/[CHANNEL_ID]`` to identify the
                channel.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            notification_channel (:class:`google.cloud.monitoring_v3.types.NotificationChannel`):
                Required. The definition of the ``NotificationChannel``
                to create.

                This corresponds to the ``notification_channel`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.NotificationChannel:
                A NotificationChannel is a medium through which an alert is
                   delivered when a policy violation is detected.
                   Examples of channels include email, SMS, and
                   third-party messaging applications. Fields containing
                   sensitive information like authentication tokens or
                   contact info are only partially populated on
                   retrieval.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, notification_channel])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = notification_service.CreateNotificationChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if notification_channel is not None:
            request.notification_channel = notification_channel

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_notification_channel,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_notification_channel(
        self,
        request: notification_service.UpdateNotificationChannelRequest = None,
        *,
        update_mask: field_mask_pb2.FieldMask = None,
        notification_channel: notification.NotificationChannel = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification.NotificationChannel:
        r"""Updates a notification channel. Fields not specified
        in the field mask remain unchanged.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.UpdateNotificationChannelRequest`):
                The request object. The `UpdateNotificationChannel`
                request.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The fields to update.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            notification_channel (:class:`google.cloud.monitoring_v3.types.NotificationChannel`):
                Required. A description of the changes to be applied to
                the specified notification channel. The description must
                provide a definition for fields to be updated; the names
                of these fields should also be included in the
                ``update_mask``.

                This corresponds to the ``notification_channel`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.NotificationChannel:
                A NotificationChannel is a medium through which an alert is
                   delivered when a policy violation is detected.
                   Examples of channels include email, SMS, and
                   third-party messaging applications. Fields containing
                   sensitive information like authentication tokens or
                   contact info are only partially populated on
                   retrieval.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([update_mask, notification_channel])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = notification_service.UpdateNotificationChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if update_mask is not None:
            request.update_mask = update_mask
        if notification_channel is not None:
            request.notification_channel = notification_channel

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_notification_channel,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("notification_channel.name", request.notification_channel.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_notification_channel(
        self,
        request: notification_service.DeleteNotificationChannelRequest = None,
        *,
        name: str = None,
        force: bool = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a notification channel.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.DeleteNotificationChannelRequest`):
                The request object. The `DeleteNotificationChannel`
                request.
            name (:class:`str`):
                Required. The channel for which to execute the request.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/notificationChannels/[CHANNEL_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            force (:class:`bool`):
                If true, the notification channel
                will be deleted regardless of its use in
                alert policies (the policies will be
                updated to remove the channel). If
                false, channels that are still
                referenced by an existing alerting
                policy will fail to be deleted in a
                delete operation.

                This corresponds to the ``force`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, force])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = notification_service.DeleteNotificationChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if force is not None:
            request.force = force

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_notification_channel,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def send_notification_channel_verification_code(
        self,
        request: notification_service.SendNotificationChannelVerificationCodeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Causes a verification code to be delivered to the channel. The
        code can then be supplied in ``VerifyNotificationChannel`` to
        verify the channel.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.SendNotificationChannelVerificationCodeRequest`):
                The request object. The
                `SendNotificationChannelVerificationCode` request.
            name (:class:`str`):
                Required. The notification channel to
                which to send a verification code.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = notification_service.SendNotificationChannelVerificationCodeRequest(
            request
        )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.send_notification_channel_verification_code,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def get_notification_channel_verification_code(
        self,
        request: notification_service.GetNotificationChannelVerificationCodeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification_service.GetNotificationChannelVerificationCodeResponse:
        r"""Requests a verification code for an already verified
        channel that can then be used in a call to
        VerifyNotificationChannel() on a different channel with
        an equivalent identity in the same or in a different
        project. This makes it possible to copy a channel
        between projects without requiring manual reverification
        of the channel. If the channel is not in the verified
        state, this method will fail (in other words, this may
        only be used if the
        SendNotificationChannelVerificationCode and
        VerifyNotificationChannel paths have already been used
        to put the given channel into the verified state).

        There is no guarantee that the verification codes
        returned by this method will be of a similar structure
        or form as the ones that are delivered to the channel
        via SendNotificationChannelVerificationCode; while
        VerifyNotificationChannel() will recognize both the
        codes delivered via
        SendNotificationChannelVerificationCode() and returned
        from GetNotificationChannelVerificationCode(), it is
        typically the case that the verification codes delivered
        via
        SendNotificationChannelVerificationCode() will be
        shorter and also have a shorter expiration (e.g. codes
        such as "G-123456") whereas GetVerificationCode() will
        typically return a much longer, websafe base 64 encoded
        string that has a longer expiration time.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.GetNotificationChannelVerificationCodeRequest`):
                The request object. The
                `GetNotificationChannelVerificationCode` request.
            name (:class:`str`):
                Required. The notification channel
                for which a verification code is to be
                generated and retrieved. This must name
                a channel that is already verified; if
                the specified channel is not verified,
                the request will fail.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.GetNotificationChannelVerificationCodeResponse:
                The GetNotificationChannelVerificationCode request.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = notification_service.GetNotificationChannelVerificationCodeRequest(
            request
        )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_notification_channel_verification_code,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def verify_notification_channel(
        self,
        request: notification_service.VerifyNotificationChannelRequest = None,
        *,
        name: str = None,
        code: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> notification.NotificationChannel:
        r"""Verifies a ``NotificationChannel`` by proving receipt of the
        code delivered to the channel as a result of calling
        ``SendNotificationChannelVerificationCode``.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.VerifyNotificationChannelRequest`):
                The request object. The `VerifyNotificationChannel`
                request.
            name (:class:`str`):
                Required. The notification channel to
                verify.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            code (:class:`str`):
                Required. The verification code that was delivered to
                the channel as a result of invoking the
                ``SendNotificationChannelVerificationCode`` API method
                or that was retrieved from a verified channel via
                ``GetNotificationChannelVerificationCode``. For example,
                one might have "G-123456" or "TKNZGhhd2EyN3I1MnRnMjRv"
                (in general, one is only guaranteed that the code is
                valid UTF-8; one should not make any assumptions
                regarding the structure or format of the code).

                This corresponds to the ``code`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.NotificationChannel:
                A NotificationChannel is a medium through which an alert is
                   delivered when a policy violation is detected.
                   Examples of channels include email, SMS, and
                   third-party messaging applications. Fields containing
                   sensitive information like authentication tokens or
                   contact info are only partially populated on
                   retrieval.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, code])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = notification_service.VerifyNotificationChannelRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if code is not None:
            request.code = code

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.verify_notification_channel,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-monitoring",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("NotificationChannelServiceAsyncClient",)
