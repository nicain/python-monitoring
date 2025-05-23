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
from distutils import util
import os
import re
from typing import Callable, Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.monitoring_v3.services.alert_policy_service import pagers
from google.cloud.monitoring_v3.types import alert
from google.cloud.monitoring_v3.types import alert_service
from google.cloud.monitoring_v3.types import mutation_record
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import AlertPolicyServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import AlertPolicyServiceGrpcTransport
from .transports.grpc_asyncio import AlertPolicyServiceGrpcAsyncIOTransport


class AlertPolicyServiceClientMeta(type):
    """Metaclass for the AlertPolicyService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[AlertPolicyServiceTransport]]
    _transport_registry["grpc"] = AlertPolicyServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = AlertPolicyServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[AlertPolicyServiceTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class AlertPolicyServiceClient(metaclass=AlertPolicyServiceClientMeta):
    """The AlertPolicyService API is used to manage (list, create, delete,
    edit) alert policies in Stackdriver Monitoring. An alerting policy
    is a description of the conditions under which some aspect of your
    system is considered to be "unhealthy" and the ways to notify people
    or services about this state. In addition to using this API, alert
    policies can also be managed through `Stackdriver
    Monitoring <https://cloud.google.com/monitoring/docs/>`__, which can
    be reached by clicking the "Monitoring" tab in `Cloud
    Console <https://console.cloud.google.com/>`__.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "monitoring.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
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
            AlertPolicyServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            AlertPolicyServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> AlertPolicyServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            AlertPolicyServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def alert_policy_path(project: str, alert_policy: str,) -> str:
        """Returns a fully-qualified alert_policy string."""
        return "projects/{project}/alertPolicies/{alert_policy}".format(
            project=project, alert_policy=alert_policy,
        )

    @staticmethod
    def parse_alert_policy_path(path: str) -> Dict[str, str]:
        """Parses a alert_policy path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/alertPolicies/(?P<alert_policy>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def alert_policy_condition_path(
        project: str, alert_policy: str, condition: str,
    ) -> str:
        """Returns a fully-qualified alert_policy_condition string."""
        return "projects/{project}/alertPolicies/{alert_policy}/conditions/{condition}".format(
            project=project, alert_policy=alert_policy, condition=condition,
        )

    @staticmethod
    def parse_alert_policy_condition_path(path: str) -> Dict[str, str]:
        """Parses a alert_policy_condition path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/alertPolicies/(?P<alert_policy>.+?)/conditions/(?P<condition>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, AlertPolicyServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the alert policy service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, AlertPolicyServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                if is_mtls:
                    api_endpoint = self.DEFAULT_MTLS_ENDPOINT
                else:
                    api_endpoint = self.DEFAULT_ENDPOINT
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, AlertPolicyServiceTransport):
            # transport is a AlertPolicyServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=(
                    Transport == type(self).get_transport_class("grpc")
                    or Transport == type(self).get_transport_class("grpc_asyncio")
                ),
            )

    def list_alert_policies(
        self,
        request: alert_service.ListAlertPoliciesRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAlertPoliciesPager:
        r"""Lists the existing alerting policies for the
        workspace.

        Args:
            request (google.cloud.monitoring_v3.types.ListAlertPoliciesRequest):
                The request object. The protocol for the
                `ListAlertPolicies` request.
            name (str):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                whose alert policies are to be listed. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                Note that this field names the parent container in which
                the alerting policies to be listed are stored. To
                retrieve a single alerting policy by name, use the
                [GetAlertPolicy][google.monitoring.v3.AlertPolicyService.GetAlertPolicy]
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
            google.cloud.monitoring_v3.services.alert_policy_service.pagers.ListAlertPoliciesPager:
                The protocol for the ListAlertPolicies response.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a alert_service.ListAlertPoliciesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, alert_service.ListAlertPoliciesRequest):
            request = alert_service.ListAlertPoliciesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_alert_policies]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListAlertPoliciesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_alert_policy(
        self,
        request: alert_service.GetAlertPolicyRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> alert.AlertPolicy:
        r"""Gets a single alerting policy.

        Args:
            request (google.cloud.monitoring_v3.types.GetAlertPolicyRequest):
                The request object. The protocol for the
                `GetAlertPolicy` request.
            name (str):
                Required. The alerting policy to retrieve. The format
                is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/alertPolicies/[ALERT_POLICY_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.AlertPolicy:
                A description of the conditions under which some aspect of your system is
                   considered to be "unhealthy" and the ways to notify
                   people or services about this state. For an overview
                   of alert policies, see [Introduction to
                   Alerting](\ https://cloud.google.com/monitoring/alerts/).

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

        # Minor optimization to avoid making a copy if the user passes
        # in a alert_service.GetAlertPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, alert_service.GetAlertPolicyRequest):
            request = alert_service.GetAlertPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_alert_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_alert_policy(
        self,
        request: alert_service.CreateAlertPolicyRequest = None,
        *,
        name: str = None,
        alert_policy: alert.AlertPolicy = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> alert.AlertPolicy:
        r"""Creates a new alerting policy.

        Args:
            request (google.cloud.monitoring_v3.types.CreateAlertPolicyRequest):
                The request object. The protocol for the
                `CreateAlertPolicy` request.
            name (str):
                Required. The
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                in which to create the alerting policy. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                Note that this field names the parent container in which
                the alerting policy will be written, not the name of the
                created policy. \|name\| must be a host project of a
                workspace, otherwise INVALID_ARGUMENT error will return.
                The alerting policy that is returned will have a name
                that contains a normalized representation of this name
                as a prefix but adds a suffix of the form
                ``/alertPolicies/[ALERT_POLICY_ID]``, identifying the
                policy in the container.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            alert_policy (google.cloud.monitoring_v3.types.AlertPolicy):
                Required. The requested alerting policy. You should omit
                the ``name`` field in this policy. The name will be
                returned in the new policy, including a new
                ``[ALERT_POLICY_ID]`` value.

                This corresponds to the ``alert_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.AlertPolicy:
                A description of the conditions under which some aspect of your system is
                   considered to be "unhealthy" and the ways to notify
                   people or services about this state. For an overview
                   of alert policies, see [Introduction to
                   Alerting](\ https://cloud.google.com/monitoring/alerts/).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, alert_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a alert_service.CreateAlertPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, alert_service.CreateAlertPolicyRequest):
            request = alert_service.CreateAlertPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if alert_policy is not None:
                request.alert_policy = alert_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_alert_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_alert_policy(
        self,
        request: alert_service.DeleteAlertPolicyRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an alerting policy.

        Args:
            request (google.cloud.monitoring_v3.types.DeleteAlertPolicyRequest):
                The request object. The protocol for the
                `DeleteAlertPolicy` request.
            name (str):
                Required. The alerting policy to delete. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/alertPolicies/[ALERT_POLICY_ID]

                For more information, see
                [AlertPolicy][google.monitoring.v3.AlertPolicy].

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

        # Minor optimization to avoid making a copy if the user passes
        # in a alert_service.DeleteAlertPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, alert_service.DeleteAlertPolicyRequest):
            request = alert_service.DeleteAlertPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_alert_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def update_alert_policy(
        self,
        request: alert_service.UpdateAlertPolicyRequest = None,
        *,
        update_mask: field_mask_pb2.FieldMask = None,
        alert_policy: alert.AlertPolicy = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> alert.AlertPolicy:
        r"""Updates an alerting policy. You can either replace the entire
        policy with a new one or replace only certain fields in the
        current alerting policy by specifying the fields to be updated
        via ``updateMask``. Returns the updated alerting policy.

        Args:
            request (google.cloud.monitoring_v3.types.UpdateAlertPolicyRequest):
                The request object. The protocol for the
                `UpdateAlertPolicy` request.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Optional. A list of alerting policy field names. If this
                field is not empty, each listed field in the existing
                alerting policy is set to the value of the corresponding
                field in the supplied policy (``alert_policy``), or to
                the field's default value if the field is not in the
                supplied alerting policy. Fields not listed retain their
                previous value.

                Examples of valid field masks include ``display_name``,
                ``documentation``, ``documentation.content``,
                ``documentation.mime_type``, ``user_labels``,
                ``user_label.nameofkey``, ``enabled``, ``conditions``,
                ``combiner``, etc.

                If this field is empty, then the supplied alerting
                policy replaces the existing policy. It is the same as
                deleting the existing policy and adding the supplied
                policy, except for the following:

                -  The new policy will have the same
                   ``[ALERT_POLICY_ID]`` as the former policy. This
                   gives you continuity with the former policy in your
                   notifications and incidents.
                -  Conditions in the new policy will keep their former
                   ``[CONDITION_ID]`` if the supplied condition includes
                   the ``name`` field with that ``[CONDITION_ID]``. If
                   the supplied condition omits the ``name`` field, then
                   a new ``[CONDITION_ID]`` is created.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            alert_policy (google.cloud.monitoring_v3.types.AlertPolicy):
                Required. The updated alerting policy or the updated
                values for the fields listed in ``update_mask``. If
                ``update_mask`` is not empty, any fields in this policy
                that are not in ``update_mask`` are ignored.

                This corresponds to the ``alert_policy`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.AlertPolicy:
                A description of the conditions under which some aspect of your system is
                   considered to be "unhealthy" and the ways to notify
                   people or services about this state. For an overview
                   of alert policies, see [Introduction to
                   Alerting](\ https://cloud.google.com/monitoring/alerts/).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([update_mask, alert_policy])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a alert_service.UpdateAlertPolicyRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, alert_service.UpdateAlertPolicyRequest):
            request = alert_service.UpdateAlertPolicyRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if update_mask is not None:
                request.update_mask = update_mask
            if alert_policy is not None:
                request.alert_policy = alert_policy

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_alert_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("alert_policy.name", request.alert_policy.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

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


__all__ = ("AlertPolicyServiceClient",)
