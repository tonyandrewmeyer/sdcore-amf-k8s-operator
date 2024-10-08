# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.


import scenario
from ops.pebble import Layer, ServiceStatus

from tests.unit.fixtures import AMFUnitTestFixtures


class TestCharmFiveGN2RelationJoined(AMFUnitTestFixtures):
    def test_given_service_not_running_when_fiveg_n2_relation_joined_then_n2_information_is_not_in_relation_databag(  # noqa: E501
        self,
    ):
        fiveg_n2_relation = scenario.Relation(endpoint="fiveg-n2", interface="fiveg-n2")
        container = scenario.Container(name="amf", can_connect=True)
        state_in = scenario.State(
            leader=True,
            containers=[container],
            relations=[fiveg_n2_relation],
        )
        self.mock_check_output.return_value = b"1.1.1.1"
        self.mock_k8s_service.get_hostname.return_value = "amf.pizza.com"
        self.mock_k8s_service.get_ip.return_value = "1.1.1.1"

        state_out = self.ctx.run(fiveg_n2_relation.joined_event, state_in)

        assert state_out.relations[0].local_app_data == {}

    def test_given_n2_information_and_service_is_running_when_fiveg_n2_relation_joined_then_n2_information_is_in_relation_databag(  # noqa: E501
        self,
    ):
        fiveg_n2_relation = scenario.Relation(endpoint="fiveg-n2", interface="fiveg-n2")
        container = scenario.Container(
            name="amf",
            can_connect=True,
            layers={
                "amf": Layer(
                    {
                        "services": {
                            "amf": {
                                "startup": "enabled",
                                "override": "replace",
                                "command": "/bin/amf --amfcfg /free5gc/config/amfcfg.conf",
                                "environment": {
                                    "GOTRACEBACK": "crash",
                                    "GRPC_GO_LOG_VERBOSITY_LEVEL": "99",
                                    "GRPC_GO_LOG_SEVERITY_LEVEL": "info",
                                    "GRPC_TRACE": "all",
                                    "GRPC_VERBOSITY": "DEBUG",
                                    "POD_IP": "1.1.1.1",
                                    "MANAGED_BY_CONFIG_POD": "true",
                                },
                            }
                        }
                    }
                )
            },
            service_status={"amf": ServiceStatus.ACTIVE},
        )
        state_in = scenario.State(
            leader=True,
            containers=[container],
            relations=[
                fiveg_n2_relation,
            ],
        )
        self.mock_k8s_service.get_hostname.return_value = "amf.pizza.com"
        self.mock_k8s_service.get_ip.return_value = "1.1.1.1"

        state_out = self.ctx.run(fiveg_n2_relation.joined_event, state_in)

        assert state_out.relations[0].local_app_data == {
            "amf_ip_address": "1.1.1.1",
            "amf_hostname": "amf.pizza.com",
            "amf_port": "38412",
        }

    def test_given_n2_information_and_service_is_running_and_n2_config_is_overriden_when_fiveg_n2_relation_joined_then_custom_n2_information_is_in_relation_databag(  # noqa: E501
        self,
    ):
        fiveg_n2_relation = scenario.Relation(endpoint="fiveg-n2", interface="fiveg-n2")
        container = scenario.Container(
            name="amf",
            can_connect=True,
            layers={
                "amf": Layer(
                    {
                        "services": {
                            "amf": {
                                "startup": "enabled",
                                "override": "replace",
                                "command": "/bin/amf --amfcfg /free5gc/config/amfcfg.conf",
                                "environment": {
                                    "GOTRACEBACK": "crash",
                                    "GRPC_GO_LOG_VERBOSITY_LEVEL": "99",
                                    "GRPC_GO_LOG_SEVERITY_LEVEL": "info",
                                    "GRPC_TRACE": "all",
                                    "GRPC_VERBOSITY": "DEBUG",
                                    "POD_IP": "1.1.1.1",
                                    "MANAGED_BY_CONFIG_POD": "true",
                                },
                            }
                        }
                    }
                )
            },
            service_status={"amf": ServiceStatus.ACTIVE},
        )
        state_in = scenario.State(
            config={"external-amf-ip": "2.2.2.2", "external-amf-hostname": "amf.burger.com"},
            leader=True,
            containers=[container],
            relations=[
                fiveg_n2_relation,
            ],
        )
        self.mock_k8s_service.get_hostname.return_value = "amf.pizza.com"
        self.mock_k8s_service.get_ip.return_value = "1.1.1.1"

        state_out = self.ctx.run(fiveg_n2_relation.joined_event, state_in)

        assert state_out.relations[0].local_app_data == {
            "amf_ip_address": "2.2.2.2",
            "amf_hostname": "amf.burger.com",
            "amf_port": "38412",
        }

    def test_given_n2_information_and_service_is_running_and_lb_service_has_no_hostname_when_fiveg_n2_relation_joined_then_internal_service_hostname_is_used(  # noqa: E501
        self,
    ):
        model_name = "whatever"
        fiveg_n2_relation = scenario.Relation(endpoint="fiveg-n2", interface="fiveg-n2")
        container = scenario.Container(
            name="amf",
            can_connect=True,
            layers={
                "amf": Layer(
                    {
                        "services": {
                            "amf": {
                                "startup": "enabled",
                                "override": "replace",
                                "command": "/bin/amf --amfcfg /free5gc/config/amfcfg.conf",
                                "environment": {
                                    "GOTRACEBACK": "crash",
                                    "GRPC_GO_LOG_VERBOSITY_LEVEL": "99",
                                    "GRPC_GO_LOG_SEVERITY_LEVEL": "info",
                                    "GRPC_TRACE": "all",
                                    "GRPC_VERBOSITY": "DEBUG",
                                    "POD_IP": "1.1.1.1",
                                    "MANAGED_BY_CONFIG_POD": "true",
                                },
                            }
                        }
                    }
                )
            },
            service_status={"amf": ServiceStatus.ACTIVE},
        )
        state_in = scenario.State(
            model=scenario.Model(
                name=model_name,
            ),
            config={"external-amf-ip": "2.2.2.2"},
            leader=True,
            containers=[container],
            relations=[
                fiveg_n2_relation,
            ],
        )
        self.mock_check_output.return_value = b"1.1.1.1"
        self.mock_k8s_service.get_hostname.return_value = None
        self.mock_k8s_service.get_ip.return_value = "1.1.1.1"
        self.mock_nrf_url.return_value = "http://nrf:8081"

        state_out = self.ctx.run(fiveg_n2_relation.joined_event, state_in)

        assert state_out.relations[0].local_app_data == {
            "amf_ip_address": "2.2.2.2",
            "amf_hostname": f"sdcore-amf-k8s-external.{model_name}.svc.cluster.local",
            "amf_port": "38412",
        }
