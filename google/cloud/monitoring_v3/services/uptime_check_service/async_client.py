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

from google.api import monitored_resource_pb2  # type: ignore
from google.cloud.monitoring_v3.services.uptime_check_service import pagers
from google.cloud.monitoring_v3.types import uptime
from google.cloud.monitoring_v3.types import uptime_service
from google.protobuf import duration_pb2  # type: ignore
from .transports.base import UptimeCheckServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import UptimeCheckServiceGrpcAsyncIOTransport
from .client import UptimeCheckServiceClient


class UptimeCheckServiceAsyncClient:
    """The UptimeCheckService API is used to manage (list, create, delete,
    edit) Uptime check configurations in the Stackdriver Monitoring
    product. An Uptime check is a piece of configuration that determines
    which resources and services to monitor for availability. These
    configurations can also be configured interactively by navigating to
    the [Cloud Console] (http://console.cloud.google.com), selecting the
    appropriate project, clicking on "Monitoring" on the left-hand side
    to navigate to Stackdriver, and then clicking on "Uptime".
    """

    _client: UptimeCheckServiceClient

    DEFAULT_ENDPOINT = UptimeCheckServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = UptimeCheckServiceClient.DEFAULT_MTLS_ENDPOINT

    uptime_check_config_path = staticmethod(
        UptimeCheckServiceClient.uptime_check_config_path
    )
    parse_uptime_check_config_path = staticmethod(
        UptimeCheckServiceClient.parse_uptime_check_config_path
    )
    common_billing_account_path = staticmethod(
        UptimeCheckServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        UptimeCheckServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(UptimeCheckServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        UptimeCheckServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        UptimeCheckServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        UptimeCheckServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(UptimeCheckServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        UptimeCheckServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(UptimeCheckServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        UptimeCheckServiceClient.parse_common_location_path
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
            UptimeCheckServiceAsyncClient: The constructed client.
        """
        return UptimeCheckServiceClient.from_service_account_info.__func__(UptimeCheckServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            UptimeCheckServiceAsyncClient: The constructed client.
        """
        return UptimeCheckServiceClient.from_service_account_file.__func__(UptimeCheckServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> UptimeCheckServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            UptimeCheckServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(UptimeCheckServiceClient).get_transport_class,
        type(UptimeCheckServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, UptimeCheckServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the uptime check service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.UptimeCheckServiceTransport]): The
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
        self._client = UptimeCheckServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_uptime_check_configs(
        self,
        request: uptime_service.ListUptimeCheckConfigsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListUptimeCheckConfigsAsyncPager:
        r"""Lists the existing valid Uptime check configurations
        for the project (leaving out any invalid
        configurations).

        Args:
            request (:class:`google.cloud.monitoring_v3.types.ListUptimeCheckConfigsRequest`):
                The request object. The protocol for the
                `ListUptimeCheckConfigs` request.
            parent (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                whose Uptime check configurations are listed. The format
                is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.uptime_check_service.pagers.ListUptimeCheckConfigsAsyncPager:
                The protocol for the ListUptimeCheckConfigs response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = uptime_service.ListUptimeCheckConfigsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_uptime_check_configs,
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
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListUptimeCheckConfigsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_uptime_check_config(
        self,
        request: uptime_service.GetUptimeCheckConfigRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> uptime.UptimeCheckConfig:
        r"""Gets a single Uptime check configuration.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.GetUptimeCheckConfigRequest`):
                The request object. The protocol for the
                `GetUptimeCheckConfig` request.
            name (:class:`str`):
                Required. The Uptime check configuration to retrieve.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/uptimeCheckConfigs/[UPTIME_CHECK_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.UptimeCheckConfig:
                This message configures which
                resources and services to monitor for
                availability.

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

        request = uptime_service.GetUptimeCheckConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_uptime_check_config,
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

    async def create_uptime_check_config(
        self,
        request: uptime_service.CreateUptimeCheckConfigRequest = None,
        *,
        parent: str = None,
        uptime_check_config: uptime.UptimeCheckConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> uptime.UptimeCheckConfig:
        r"""Creates a new Uptime check configuration.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.CreateUptimeCheckConfigRequest`):
                The request object. The protocol for the
                `CreateUptimeCheckConfig` request.
            parent (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                in which to create the Uptime check. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            uptime_check_config (:class:`google.cloud.monitoring_v3.types.UptimeCheckConfig`):
                Required. The new Uptime check
                configuration.

                This corresponds to the ``uptime_check_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.UptimeCheckConfig:
                This message configures which
                resources and services to monitor for
                availability.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, uptime_check_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = uptime_service.CreateUptimeCheckConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if uptime_check_config is not None:
            request.uptime_check_config = uptime_check_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_uptime_check_config,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def update_uptime_check_config(
        self,
        request: uptime_service.UpdateUptimeCheckConfigRequest = None,
        *,
        uptime_check_config: uptime.UptimeCheckConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> uptime.UptimeCheckConfig:
        r"""Updates an Uptime check configuration. You can either replace
        the entire configuration with a new one or replace only certain
        fields in the current configuration by specifying the fields to
        be updated via ``updateMask``. Returns the updated
        configuration.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.UpdateUptimeCheckConfigRequest`):
                The request object. The protocol for the
                `UpdateUptimeCheckConfig` request.
            uptime_check_config (:class:`google.cloud.monitoring_v3.types.UptimeCheckConfig`):
                Required. If an ``updateMask`` has been specified, this
                field gives the values for the set of fields mentioned
                in the ``updateMask``. If an ``updateMask`` has not been
                given, this Uptime check configuration replaces the
                current configuration. If a field is mentioned in
                ``updateMask`` but the corresonding field is omitted in
                this partial Uptime check configuration, it has the
                effect of deleting/clearing the field from the
                configuration on the server.

                The following fields can be updated: ``display_name``,
                ``http_check``, ``tcp_check``, ``timeout``,
                ``content_matchers``, and ``selected_regions``.

                This corresponds to the ``uptime_check_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.UptimeCheckConfig:
                This message configures which
                resources and services to monitor for
                availability.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([uptime_check_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = uptime_service.UpdateUptimeCheckConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if uptime_check_config is not None:
            request.uptime_check_config = uptime_check_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_uptime_check_config,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("uptime_check_config.name", request.uptime_check_config.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_uptime_check_config(
        self,
        request: uptime_service.DeleteUptimeCheckConfigRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an Uptime check configuration. Note that this
        method will fail if the Uptime check configuration is
        referenced by an alert policy or other dependent configs
        that would be rendered invalid by the deletion.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.DeleteUptimeCheckConfigRequest`):
                The request object. The protocol for the
                `DeleteUptimeCheckConfig` request.
            name (:class:`str`):
                Required. The Uptime check configuration to delete. The
                format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/uptimeCheckConfigs/[UPTIME_CHECK_ID]

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

        request = uptime_service.DeleteUptimeCheckConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_uptime_check_config,
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

    async def list_uptime_check_ips(
        self,
        request: uptime_service.ListUptimeCheckIpsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListUptimeCheckIpsAsyncPager:
        r"""Returns the list of IP addresses that checkers run
        from

        Args:
            request (:class:`google.cloud.monitoring_v3.types.ListUptimeCheckIpsRequest`):
                The request object. The protocol for the
                `ListUptimeCheckIps` request.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.uptime_check_service.pagers.ListUptimeCheckIpsAsyncPager:
                The protocol for the ListUptimeCheckIps response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = uptime_service.ListUptimeCheckIpsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_uptime_check_ips,
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

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListUptimeCheckIpsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

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


__all__ = ("UptimeCheckServiceAsyncClient",)
