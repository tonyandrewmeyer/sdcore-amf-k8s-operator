# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

output "app_name" {
  description = "Name of the deployed application."
  value       = juju_application.amf.name
}

# Required integration endpoints

output "fiveg_nrf_endpoint" {
  description = "Name of the endpoint used to integrate with the NRF."
  value       = "fiveg_nrf"
}

output "sdcore_config_endpoint" {
  description = "Name of the endpoint used to integrate with the NMS."
  value       = "sdcore_config"
}

output "certificates_endpoint" {
  description = "Name of the endpoint used to integrate with the TLS certificates provider."
  value       = "certificates"
}

output "logging_endpoint" {
  description = "Name of the endpoint used to integrate with the Logging provider."
  value       = "logging"
}

# Provided integration endpoints

output "metrics_endpoint" {
  description = "Exposes the Prometheus metrics endpoint providing telemetry about the AMF instance."
  value       = "metrics-endpoint"
}

output "fiveg_n2_endpoint" {
  description = "Name of the endpoint used to provide information on connectivity to the N2 plane."
  value       = "fiveg-n2"
}
