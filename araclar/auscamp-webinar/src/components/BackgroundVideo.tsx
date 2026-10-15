import { useEffect, useState } from "react";

// Landscape hero footage (desktop/tablet) vs. a portrait-framed aerial (mobile)
// so the Opera House stays centered on both aspect ratios. Both stream from the
// Pexels CDN (free commercial) → out of the deploy bundle, full source quality.
const LANDSCAPE_SRC =
  "https://videos.pexels.com/video-files/31965509/13620858_1280_720_24fps.mp4";
const PORTRAIT_SRC =
  "https://videos.pexels.com/video-files/37217165/15766230_720_1280_30fps.mp4";

/**
 * Full-bleed background video for hero sections (Sydney Opera House / Harbour
 * Bridge). Muted + autoplay + loop + playsInline so it plays inline on mobile.
 * Picks a portrait clip on small screens so vertical crops still look good.
 * A green gradient overlay keeps headline text legible and on-brand.
 */
export default function BackgroundVideo() {
  const [src, setSrc] = useState(LANDSCAPE_SRC);

  useEffect(() => {
    const mq = window.matchMedia("(max-width: 767px)");
    const update = () => setSrc(mq.matches ? PORTRAIT_SRC : LANDSCAPE_SRC);
    update();
    mq.addEventListener("change", update);
    return () => mq.removeEventListener("change", update);
  }, []);

  return (
    <div aria-hidden className="pointer-events-none absolute inset-0 -z-10 overflow-hidden">
      <video
        key={src}
        className="h-full w-full object-cover"
        autoPlay
        muted
        loop
        playsInline
        preload="metadata"
      >
        <source src={src} type="video/mp4" />
      </video>
      {/* Brand-green wash: keeps AUSCAMP identity + text contrast over any footage.
          Lighter at the very top (more Sydney visible), heavier lower down where
          headline/CTA text sits so contrast stays safe. */}
      <div className="absolute inset-0 bg-gradient-to-b from-brand-green-deep/45 via-brand-green-deep/62 to-brand-green-dark/90" />
      {/* Readability scrims: a soft top band behind the header/eyebrow and a
          stronger bottom band under the CTA — keeps the Opera House + Harbour
          Bridge scenery visible while text stays crisp. */}
      <div
        className="absolute inset-0"
        style={{
          background:
            "linear-gradient(to bottom, rgba(4,40,20,0.35) 0%, rgba(4,40,20,0) 30%, rgba(4,40,20,0) 60%, rgba(4,40,20,0.55) 100%)",
        }}
      />
      {/* subtle dot texture on top, matching the poster language */}
      <div
        className="absolute inset-0 opacity-[0.06]"
        style={{
          backgroundImage: "radial-gradient(#fff 1.1px, transparent 1.1px)",
          backgroundSize: "22px 22px",
        }}
      />
    </div>
  );
}
