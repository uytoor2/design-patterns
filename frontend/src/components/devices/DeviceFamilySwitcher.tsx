import React from "react";
import { DeviceFamily } from "../../services/api";

type Props = {
  selectedFamily: DeviceFamily;
  onSelectFamily: (family: DeviceFamily) => void;
  onProvision: (family: DeviceFamily) => void;
  isProvisioning: boolean;
};

export const DeviceFamilySwitcher: React.FC<Props> = ({
  selectedFamily,
  onSelectFamily,
  onProvision,
  isProvisioning,
}) => {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 p-4 bg-white rounded-lg border border-slate-200 shadow-sm mb-6">
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-slate-700">Family Filter:</span>
        <button
          onClick={() => onSelectFamily("simulation")}
          className={`px-3 py-1.5 text-sm font-semibold rounded-md transition-colors ${
            selectedFamily === "simulation"
              ? "bg-emerald-600 text-white"
              : "bg-slate-100 text-slate-700 hover:bg-slate-200"
          }`}
        >
          Simulation
        </button>
        <button
          onClick={() => onSelectFamily("edge")}
          className={`px-3 py-1.5 text-sm font-semibold rounded-md transition-colors ${
            selectedFamily === "edge"
              ? "bg-emerald-600 text-white"
              : "bg-slate-100 text-slate-700 hover:bg-slate-200"
          }`}
        >
          Edge Hardware
        </button>
      </div>

      <button
        onClick={() => onProvision(selectedFamily)}
        disabled={isProvisioning}
        className="px-4 py-1.5 text-sm font-semibold bg-emerald-600 hover:bg-emerald-700 text-white rounded-md shadow-sm disabled:opacity-50 transition-colors"
      >
        {isProvisioning ? "Provisioning..." : `Provision Kit (${selectedFamily})`}
      </button>
    </div>
  );
};