import { useEffect } from "react";

/**
 * Client-side title + meta-description updater for SPA route changes.
 * Note: social crawlers read the static tags in index.html; per-route OG
 * would need prerendering. For Meta ad traffic the ad creative carries the
 * preview, so tab title + description here is enough.
 */
export function useDocumentMeta(title: string, description?: string): void {
  useEffect(() => {
    const prevTitle = document.title;
    document.title = title;

    const metaEl = document.querySelector('meta[name="description"]');
    const prevDesc = metaEl?.getAttribute("content") ?? null;
    if (description && metaEl) metaEl.setAttribute("content", description);

    return () => {
      document.title = prevTitle;
      if (description && metaEl && prevDesc !== null) {
        metaEl.setAttribute("content", prevDesc);
      }
    };
  }, [title, description]);
}
