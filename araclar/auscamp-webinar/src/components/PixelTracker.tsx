import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import "../types";

/**
 * Fires a Meta Pixel PageView on client-side route changes. index.html already
 * fires the initial PageView on first load, so we skip the first render to
 * avoid double-counting the landing hit.
 */
export default function PixelTracker() {
  const location = useLocation();
  const first = useRef(true);

  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    if (typeof window.fbq === "function") {
      window.fbq("track", "PageView");
    }
    window.scrollTo(0, 0);
  }, [location.pathname]);

  return null;
}
