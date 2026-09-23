from domain.devices.entity import Device
from application.devices.dto import DeviceDto
from infrastructure.persistence.models import DeviceRow


def device_to_dto(device: Device) -> DeviceDto:
    if device.id is None:
        raise ValueError("Cannot convert unpersisted Device (id is None) to DeviceDto")
    return DeviceDto(
        id=device.id,
        device_type=device.device_type,
        role=device.role,
        device_family=device.device_family,
        display_name=device.display_name,
        default_config=device.default_config,
    )


def row_to_device(row: DeviceRow) -> Device:
    return Device(
        id=row.id,
        device_type=row.device_type,
        role=row.role,
        device_family=row.device_family,
        display_name=row.display_name or "",
        default_config=row.default_config or {},
    )


def device_to_row(device: Device) -> DeviceRow:
    return DeviceRow(
        id=device.id,
        device_type=device.device_type,
        role=device.role,
        device_family=device.device_family,
        display_name=device.display_name,
        default_config=device.default_config,
    )