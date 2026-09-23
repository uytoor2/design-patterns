import React, { useEffect, useState } from "react";
import { DeviceDto, DeviceFamily, fetchDevices, provisionDeviceFamily } from "../../services/api";
import { DeviceFamilySwitcher } from "./DeviceFamilySwitcher";

export const DeviceList: React.FC = () => {
  const [devices, setDevices] = useState<DeviceDto[]>([]);
  const [selectedFamily, setSelectedFamily] = useState<DeviceFamily>("simulation");
  const [isLoading, setIsLoading] = useState(false);
  const [isProvisioning, setIsProvisioning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadDevices = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchDevices({ family: selectedFamily });
      setDevices(data);
    } catch (err: any) {
      setError(err.message || "Failed to load devices");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadDevices();
  }, [selectedFamily]);

  const handleProvision = async (family: DeviceFamily) => {
    setIsProvisioning(true);
    setError(null);
    try {
      await provisionDeviceFamily(family);
      await loadDevices();
    } catch (err: any) {
      setError(err.message || "Provisioning failed");
    } finally {
      setIsProvisioning(false);
    }
  };

  return (
    <div className="space-y-4">
      <DeviceFamilySwitcher
        selectedFamily={selectedFamily}
        onSelectFamily={setSelectedFamily}
        onProvision={handleProvision}
        isProvisioning={isProvisioning}
      />

      {error && (
        <div className="p-3 bg-red-50 text-red-700 rounded-md text-sm border border-red-200">
          {error}
        </div>
      )}

      {isLoading ? (
        <div className="text-slate-500 text-center py-8">Loading devices...</div>
      ) : devices.length === 0 ? (
        <div className="text-slate-500 text-center py-8 bg-slate-50 rounded-lg border border-dashed border-slate-300">
          No {selectedFamily} devices found. Click "Provision Kit" to generate a set.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {devices.map((device) => (
            <div key={device.id} className="p-4 bg-white rounded-lg border border-slate-200 shadow-sm space-y-2">
              <div className="flex justify-between items-start">
                <h3 className="font-semibold text-slate-800">{device.display_name}</h3>
                <div className="flex gap-1.5">
                  <span
                    className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                      device.role === "sensor"
                        ? "bg-blue-100 text-blue-700"
                        : "bg-purple-100 text-purple-700"
                    }`}
                  >
                    {device.role}
                  </span>
                  <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-100 text-slate-600">
                    {device.device_family}
                  </span>
                </div>
              </div>
              <p className="text-xs font-mono text-slate-500">Type: {device.device_type}</p>
              <div className="bg-slate-50 p-2 rounded text-xs font-mono overflow-x-auto border border-slate-100">
                {JSON.stringify(device.default_config, null, 2)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};