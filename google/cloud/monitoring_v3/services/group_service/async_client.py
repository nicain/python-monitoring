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
from google.cloud.monitoring_v3.services.group_service import pagers
from google.cloud.monitoring_v3.types import group
from google.cloud.monitoring_v3.types import group as gm_group
from google.cloud.monitoring_v3.types import group_service
from .transports.base import GroupServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import GroupServiceGrpcAsyncIOTransport
from .client import GroupServiceClient


class GroupServiceAsyncClient:
    """The Group API lets you inspect and manage your
    `groups <#google.monitoring.v3.Group>`__.

    A group is a named filter that is used to identify a collection of
    monitored resources. Groups are typically used to mirror the
    physical and/or logical topology of the environment. Because group
    membership is computed dynamically, monitored resources that are
    started in the future are automatically placed in matching groups.
    By using a group to name monitored resources in, for example, an
    alert policy, the target of that alert policy is updated
    automatically as monitored resources are added and removed from the
    infrastructure.
    """

    _client: GroupServiceClient

    DEFAULT_ENDPOINT = GroupServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = GroupServiceClient.DEFAULT_MTLS_ENDPOINT

    group_path = staticmethod(GroupServiceClient.group_path)
    parse_group_path = staticmethod(GroupServiceClient.parse_group_path)
    common_billing_account_path = staticmethod(
        GroupServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        GroupServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(GroupServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(GroupServiceClient.parse_common_folder_path)
    common_organization_path = staticmethod(GroupServiceClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        GroupServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(GroupServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        GroupServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(GroupServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        GroupServiceClient.parse_common_location_path
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
            GroupServiceAsyncClient: The constructed client.
        """
        return GroupServiceClient.from_service_account_info.__func__(GroupServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            GroupServiceAsyncClient: The constructed client.
        """
        return GroupServiceClient.from_service_account_file.__func__(GroupServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> GroupServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            GroupServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(GroupServiceClient).get_transport_class, type(GroupServiceClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, GroupServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the group service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.GroupServiceTransport]): The
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
        self._client = GroupServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_groups(
        self,
        request: group_service.ListGroupsRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGroupsAsyncPager:
        r"""Lists the existing groups.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.ListGroupsRequest`):
                The request object. The `ListGroup` request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                whose groups are to be listed. The format is:

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
            google.cloud.monitoring_v3.services.group_service.pagers.ListGroupsAsyncPager:
                The ListGroups response.

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

        request = group_service.ListGroupsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_groups,
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
        response = pagers.ListGroupsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_group(
        self,
        request: group_service.GetGroupRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> group.Group:
        r"""Gets a single group.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.GetGroupRequest`):
                The request object. The `GetGroup` request.
            name (:class:`str`):
                Required. The group to retrieve. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/groups/[GROUP_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.Group:
                The description of a dynamic collection of monitored resources. Each group
                   has a filter that is matched against monitored
                   resources and their associated metadata. If a group's
                   filter matches an available monitored resource, then
                   that resource is a member of that group. Groups can
                   contain any number of monitored resources, and each
                   monitored resource can be a member of any number of
                   groups.

                   Groups can be nested in parent-child hierarchies. The
                   parentName field identifies an optional parent for
                   each group. If a group has a parent, then the only
                   monitored resources available to be matched by the
                   group's filter are the resources contained in the
                   parent group. In other words, a group contains the
                   monitored resources that match its filter and the
                   filters of all the group's ancestors. A group without
                   a parent can contain any monitored resource.

                   For example, consider an infrastructure running a set
                   of instances with two user-defined tags:
                   "environment" and "role". A parent group has a
                   filter, environment="production". A child of that
                   parent group has a filter, role="transcoder". The
                   parent group contains all instances in the production
                   environment, regardless of their roles. The child
                   group contains instances that have the transcoder
                   role *and* are in the production environment.

                   The monitored resources contained in a group can
                   change at any moment, depending on what resources
                   exist and what filters are associated with the group
                   and its ancestors.

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

        request = group_service.GetGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_group,
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

    async def create_group(
        self,
        request: group_service.CreateGroupRequest = None,
        *,
        name: str = None,
        group: gm_group.Group = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gm_group.Group:
        r"""Creates a new group.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.CreateGroupRequest`):
                The request object. The `CreateGroup` request.
            name (:class:`str`):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                in which to create the group. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            group (:class:`google.cloud.monitoring_v3.types.Group`):
                Required. A group definition. It is an error to define
                the ``name`` field because the system assigns the name.

                This corresponds to the ``group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.Group:
                The description of a dynamic collection of monitored resources. Each group
                   has a filter that is matched against monitored
                   resources and their associated metadata. If a group's
                   filter matches an available monitored resource, then
                   that resource is a member of that group. Groups can
                   contain any number of monitored resources, and each
                   monitored resource can be a member of any number of
                   groups.

                   Groups can be nested in parent-child hierarchies. The
                   parentName field identifies an optional parent for
                   each group. If a group has a parent, then the only
                   monitored resources available to be matched by the
                   group's filter are the resources contained in the
                   parent group. In other words, a group contains the
                   monitored resources that match its filter and the
                   filters of all the group's ancestors. A group without
                   a parent can contain any monitored resource.

                   For example, consider an infrastructure running a set
                   of instances with two user-defined tags:
                   "environment" and "role". A parent group has a
                   filter, environment="production". A child of that
                   parent group has a filter, role="transcoder". The
                   parent group contains all instances in the production
                   environment, regardless of their roles. The child
                   group contains instances that have the transcoder
                   role *and* are in the production environment.

                   The monitored resources contained in a group can
                   change at any moment, depending on what resources
                   exist and what filters are associated with the group
                   and its ancestors.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = group_service.CreateGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if group is not None:
            request.group = group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_group,
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

    async def update_group(
        self,
        request: group_service.UpdateGroupRequest = None,
        *,
        group: gm_group.Group = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gm_group.Group:
        r"""Updates an existing group. You can change any group attributes
        except ``name``.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.UpdateGroupRequest`):
                The request object. The `UpdateGroup` request.
            group (:class:`google.cloud.monitoring_v3.types.Group`):
                Required. The new definition of the group. All fields of
                the existing group, excepting ``name``, are replaced
                with the corresponding fields of this group.

                This corresponds to the ``group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.Group:
                The description of a dynamic collection of monitored resources. Each group
                   has a filter that is matched against monitored
                   resources and their associated metadata. If a group's
                   filter matches an available monitored resource, then
                   that resource is a member of that group. Groups can
                   contain any number of monitored resources, and each
                   monitored resource can be a member of any number of
                   groups.

                   Groups can be nested in parent-child hierarchies. The
                   parentName field identifies an optional parent for
                   each group. If a group has a parent, then the only
                   monitored resources available to be matched by the
                   group's filter are the resources contained in the
                   parent group. In other words, a group contains the
                   monitored resources that match its filter and the
                   filters of all the group's ancestors. A group without
                   a parent can contain any monitored resource.

                   For example, consider an infrastructure running a set
                   of instances with two user-defined tags:
                   "environment" and "role". A parent group has a
                   filter, environment="production". A child of that
                   parent group has a filter, role="transcoder". The
                   parent group contains all instances in the production
                   environment, regardless of their roles. The child
                   group contains instances that have the transcoder
                   role *and* are in the production environment.

                   The monitored resources contained in a group can
                   change at any moment, depending on what resources
                   exist and what filters are associated with the group
                   and its ancestors.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([group])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = group_service.UpdateGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if group is not None:
            request.group = group

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_group,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=180.0,
            ),
            default_timeout=180.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("group.name", request.group.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_group(
        self,
        request: group_service.DeleteGroupRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an existing group.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.DeleteGroupRequest`):
                The request object. The `DeleteGroup` request. The
                default behavior is to be able to delete a single group
                without any descendants.
            name (:class:`str`):
                Required. The group to delete. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/groups/[GROUP_ID]

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

        request = group_service.DeleteGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_group,
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

    async def list_group_members(
        self,
        request: group_service.ListGroupMembersRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListGroupMembersAsyncPager:
        r"""Lists the monitored resources that are members of a
        group.

        Args:
            request (:class:`google.cloud.monitoring_v3.types.ListGroupMembersRequest`):
                The request object. The `ListGroupMembers` request.
            name (:class:`str`):
                Required. The group whose members are listed. The format
                is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/groups/[GROUP_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.group_service.pagers.ListGroupMembersAsyncPager:
                The ListGroupMembers response.

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

        request = group_service.ListGroupMembersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_group_members,
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
        response = pagers.ListGroupMembersAsyncPager(
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


__all__ = ("GroupServiceAsyncClient",)
