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
from google.api import metric_pb2  # type: ignore
from google.api import monitored_resource_pb2  # type: ignore
from google.cloud.monitoring_v3.services.metric_service import pagers
from google.cloud.monitoring_v3.types import common
from google.cloud.monitoring_v3.types import metric as gm_metric
from google.cloud.monitoring_v3.types import metric_service
from .transports.base import MetricServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import MetricServiceGrpcAsyncIOTransport
from .client import MetricServiceClient


class MetricServiceAsyncClient:
    """Manages metric descriptors, monitored resource descriptors,
    and time series data.
    """

    _client: MetricServiceClient

    DEFAULT_ENDPOINT = MetricServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = MetricServiceClient.DEFAULT_MTLS_ENDPOINT

    """metric_descriptor_path = staticmethod(MetricServiceClient.metric_descriptor_path)
    parse_metric_descriptor_path = staticmethod(MetricServiceClient.parse_metric_descriptor_path)"""
    monitored_resource_descriptor_path = staticmethod(
        MetricServiceClient.monitored_resource_descriptor_path
    )
    parse_monitored_resource_descriptor_path = staticmethod(
        MetricServiceClient.parse_monitored_resource_descriptor_path
    )
    time_series_path = staticmethod(MetricServiceClient.time_series_path)
    parse_time_series_path = staticmethod(MetricServiceClient.parse_time_series_path)
    common_billing_account_path = staticmethod(
        MetricServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        MetricServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(MetricServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        MetricServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        MetricServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        MetricServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(MetricServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        MetricServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(MetricServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        MetricServiceClient.parse_common_location_path
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
            MetricServiceAsyncClient: The constructed client.
        """
        return MetricServiceClient.from_service_account_info.__func__(MetricServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            MetricServiceAsyncClient: The constructed client.
        """
        return MetricServiceClient.from_service_account_file.__func__(MetricServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> MetricServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            MetricServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(MetricServiceClient).get_transport_class, type(MetricServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, MetricServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the metric service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.MetricServiceTransport]): The
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
        self._client = MetricServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_monitored_resource_descriptors(
        self,
        request: metric_service.ListMonitoredResourceDescriptorsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMonitoredResourceDescriptorsAsyncPager:
        r"""Lists monitored resource descriptors that match a
        filter. This method does not require a Workspace.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.ListMonitoredResourceDescriptorsRequest`):
                The request object. The
                `ListMonitoredResourceDescriptors` request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                on which to execute the request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.metric_service.pagers.ListMonitoredResourceDescriptorsAsyncPager:
                The ListMonitoredResourceDescriptors response.

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

        request = metric_service.ListMonitoredResourceDescriptorsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_monitored_resource_descriptors,
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
        response = pagers.ListMonitoredResourceDescriptorsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_monitored_resource_descriptor(
        self,
        request: metric_service.GetMonitoredResourceDescriptorRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> monitored_resource_pb2.MonitoredResourceDescriptor:
        r"""Gets a single monitored resource descriptor. This
        method does not require a Workspace.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.GetMonitoredResourceDescriptorRequest`):
                The request object. The `GetMonitoredResourceDescriptor`
                request.
            name (:class:`str`):
                Required. The monitored resource descriptor to get. The
                format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/monitoredResourceDescriptors/[RESOURCE_TYPE]

                The ``[RESOURCE_TYPE]`` is a predefined type, such as
                ``cloudsql_database``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.monitored_resource_pb2.MonitoredResourceDescriptor:
                An object that describes the schema of a [MonitoredResource][google.api.MonitoredResource] object using a
                   type name and a set of labels. For example, the
                   monitored resource descriptor for Google Compute
                   Engine VM instances has a type of "gce_instance" and
                   specifies the use of the labels "instance_id" and
                   "zone" to identify particular VM instances.

                   Different APIs can support different monitored
                   resource types. APIs generally provide a list method
                   that returns the monitored resource descriptors used
                   by the API.

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

        request = metric_service.GetMonitoredResourceDescriptorRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_monitored_resource_descriptor,
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

    async def list_metric_descriptors(
        self,
        request: metric_service.ListMetricDescriptorsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMetricDescriptorsAsyncPager:
        r"""Lists metric descriptors that match a filter. This
        method does not require a Workspace.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.ListMetricDescriptorsRequest`):
                The request object. The `ListMetricDescriptors` request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                on which to execute the request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.metric_service.pagers.ListMetricDescriptorsAsyncPager:
                The ListMetricDescriptors response.

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

        request = metric_service.ListMetricDescriptorsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_metric_descriptors,
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
        response = pagers.ListMetricDescriptorsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_metric_descriptor(
        self,
        request: metric_service.GetMetricDescriptorRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metric_pb2.MetricDescriptor:
        r"""Gets a single metric descriptor. This method does not
        require a Workspace.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.GetMetricDescriptorRequest`):
                The request object. The `GetMetricDescriptor` request.
            name (:class:`str`):
                Required. The metric descriptor on which to execute the
                request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/metricDescriptors/[METRIC_ID]

                An example value of ``[METRIC_ID]`` is
                ``"compute.googleapis.com/instance/disk/read_bytes_count"``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.metric_pb2.MetricDescriptor:
                Defines a metric type and its schema.
                Once a metric descriptor is created,
                deleting or altering it stops data
                collection and makes the metric type's
                existing data unusable.

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

        request = metric_service.GetMetricDescriptorRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_metric_descriptor,
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

    async def create_metric_descriptor(
        self,
        request: metric_service.CreateMetricDescriptorRequest = None,
        *,
        name: str = None,
        metric_descriptor: metric_pb2.MetricDescriptor = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metric_pb2.MetricDescriptor:
        r"""Creates a new metric descriptor. User-created metric descriptors
        define `custom
        metrics <https://cloud.google.com/monitoring/custom-metrics>`__.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.CreateMetricDescriptorRequest`):
                The request object. The `CreateMetricDescriptor`
                request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                on which to execute the request. The format is: 4
                projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metric_descriptor (:class:`google.api.metric_pb2.MetricDescriptor`):
                Required. The new `custom
                metric <https://cloud.google.com/monitoring/custom-metrics>`__
                descriptor.

                This corresponds to the ``metric_descriptor`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.metric_pb2.MetricDescriptor:
                Defines a metric type and its schema.
                Once a metric descriptor is created,
                deleting or altering it stops data
                collection and makes the metric type's
                existing data unusable.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, metric_descriptor])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metric_service.CreateMetricDescriptorRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if metric_descriptor is not None:
            request.metric_descriptor = metric_descriptor

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_metric_descriptor,
            default_timeout=12.0,
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

    async def delete_metric_descriptor(
        self,
        request: metric_service.DeleteMetricDescriptorRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a metric descriptor. Only user-created `custom
        metrics <https://cloud.google.com/monitoring/custom-metrics>`__
        can be deleted.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.DeleteMetricDescriptorRequest`):
                The request object. The `DeleteMetricDescriptor`
                request.
            name (:class:`str`):
                Required. The metric descriptor on which to execute the
                request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/metricDescriptors/[METRIC_ID]

                An example of ``[METRIC_ID]`` is:
                ``"custom.googleapis.com/my_test_metric"``.

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

        request = metric_service.DeleteMetricDescriptorRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_metric_descriptor,
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

    async def list_time_series(
        self,
        request: metric_service.ListTimeSeriesRequest = None,
        *,
        name: str = None,
        filter: str = None,
        interval: common.TimeInterval = None,
        view: metric_service.ListTimeSeriesRequest.TimeSeriesView = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTimeSeriesAsyncPager:
        r"""Lists time series that match a filter. This method
        does not require a Workspace.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.ListTimeSeriesRequest`):
                The request object. The `ListTimeSeries` request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__,
                organization or folder on which to execute the request.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]
                    organizations/[ORGANIZATION_ID]
                    folders/[FOLDER_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
                Required. A `monitoring
                filter <https://cloud.google.com/monitoring/api/v3/filters>`__
                that specifies which time series should be returned. The
                filter must specify a single metric type, and can
                additionally specify metric labels and other
                information. For example:

                ::

                    metric.type = "compute.googleapis.com/instance/cpu/usage_time" AND
                        metric.labels.instance_name = "my-instance-name"

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            interval (:class:`google.cloud.monitoring_v3.types.TimeInterval`):
                Required. The time interval for which
                results should be returned. Only time
                series that contain data points in the
                specified interval are included in the
                response.

                This corresponds to the ``interval`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            view (:class:`google.cloud.monitoring_v3.types.ListTimeSeriesRequest.TimeSeriesView`):
                Required. Specifies which information
                is returned about the time series.

                This corresponds to the ``view`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.metric_service.pagers.ListTimeSeriesAsyncPager:
                The ListTimeSeries response.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, filter, interval, view])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metric_service.ListTimeSeriesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if filter is not None:
            request.filter = filter
        if interval is not None:
            request.interval = interval
        if view is not None:
            request.view = view

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_time_series,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=90.0,
            ),
            default_timeout=90.0,
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
        response = pagers.ListTimeSeriesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_time_series(
        self,
        request: metric_service.CreateTimeSeriesRequest = None,
        *,
        name: str = None,
        time_series: Sequence[gm_metric.TimeSeries] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Creates or adds data to one or more time series.
        The response is empty if all time series in the request
        were written. If any time series could not be written, a
        corresponding failure message is included in the error
        response.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.CreateTimeSeriesRequest`):
                The request object. The `CreateTimeSeries` request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                on which to execute the request. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            time_series (:class:`Sequence[google.cloud.monitoring_v3.types.TimeSeries]`):
                Required. The new data to be added to a list of time
                series. Adds at most one data point to each of several
                time series. The new data point must be more recent than
                any other point in its time series. Each ``TimeSeries``
                value must fully specify a unique time series by
                supplying all label values for the metric and the
                monitored resource.

                The maximum number of ``TimeSeries`` objects per
                ``Create`` request is 200.

                This corresponds to the ``time_series`` field
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
        has_flattened_params = any([name, time_series])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metric_service.CreateTimeSeriesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if time_series:
            request.time_series.extend(time_series)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_time_series,
            default_timeout=12.0,
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-monitoring",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("MetricServiceAsyncClient",)
