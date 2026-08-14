import { useEffect, useState } from "react";
import * as api from "../../services/api";
import type { Airport } from "../../types/radar";

export function useAirports() {
  const [airports, setAirports] = useState<Airport[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .listAirports()
      .then(setAirports)
      .finally(() => setLoading(false));
  }, []);

  return { airports, loading };
}
