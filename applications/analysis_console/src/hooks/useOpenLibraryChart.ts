import { useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useLibrary } from "../state/library";
import { useSession } from "../state/session";

/** Open a library chart into the active analysis session. */
export function useOpenLibraryChart() {
  const navigate = useNavigate();
  const { openChart } = useLibrary();
  const { setChart, resetDownstreamFromChart } = useSession();

  return useCallback(
    (libraryId: string, path = "/chart") => {
      const entry = openChart(libraryId);
      if (!entry) return;
      if (entry.remote) {
        setChart(entry.remote);
        resetDownstreamFromChart();
      }
      navigate(path);
    },
    [navigate, openChart, resetDownstreamFromChart, setChart],
  );
}
