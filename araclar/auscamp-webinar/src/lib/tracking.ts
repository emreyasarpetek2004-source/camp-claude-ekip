import "../types";

/**
 * Fires a Meta Pixel "Lead" event enriched with the ad UTM params, then sends
 * the user on to targetUrl. The redirect always happens — a missing/blocked
 * pixel must never trap the visitor.
 *
 * @param contentName identifies which CTA fired (webinar slug or "duyuru-toplulugu")
 * @param targetUrl   the WhatsApp / community link to open
 */
export function trackAndRedirect(contentName: string, targetUrl: string): void {
  const params = new URLSearchParams(window.location.search);
  const utm_source = params.get("utm_source") ?? undefined;
  const utm_campaign = params.get("utm_campaign") ?? undefined;
  const utm_content = params.get("utm_content") ?? undefined;

  const go = () => {
    // Same-tab navigation: reliable on mobile (a deferred window.open is killed
    // by popup blockers). The Lead event above fires via sendBeacon, so it
    // survives the navigation.
    window.location.href = targetUrl;
  };

  if (typeof window.fbq === "function") {
    window.fbq("track", "Lead", {
      content_name: contentName,
      utm_source,
      utm_campaign,
      utm_content,
    });
    // Give the pixel a beat to fire before navigating, but never block the user.
    window.setTimeout(go, 300);
  } else {
    // No pixel available — redirect immediately, don't trap the user.
    go();
  }
}
