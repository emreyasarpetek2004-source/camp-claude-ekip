import { useState } from "react";

function initials(speaker: string): string {
  // Strip common Turkish titles, then take the first letter of the first two
  // meaningful name parts. Handles two-speaker strings ("A & B") gracefully.
  const cleaned = speaker
    .replace(/Doç\.|Prof\.|Dr\.|Uzm\.|Op\.|&/gi, " ")
    .replace(/\s+/g, " ")
    .trim();
  const parts = cleaned.split(" ").filter(Boolean);
  const letters = parts.slice(0, 2).map((p) => p[0]?.toLocaleUpperCase("tr-TR") ?? "");
  return letters.join("") || "AC";
}

interface Props {
  speaker: string;
  photo?: string;
  objectPosition?: string;
  grayed?: boolean;
  size?: "md" | "lg" | "xl";
}

const SIZES = { md: "h-16 w-16 text-lg", lg: "h-20 w-20 text-xl", xl: "h-28 w-28 text-3xl" };

export default function SpeakerAvatar({
  speaker,
  photo,
  objectPosition,
  grayed = false,
  size = "md",
}: Props) {
  const [failed, setFailed] = useState(false);
  const ring = grayed ? "ring-white/20" : "ring-brand-green-mid";
  const showPhoto = photo && !failed;

  return (
    <div
      className={`${SIZES[size]} shrink-0 overflow-hidden rounded-full bg-brand-green-dark ring-4 ${ring} ${
        grayed ? "opacity-60 grayscale" : ""
      }`}
    >
      {showPhoto ? (
        <img
          src={photo}
          alt={speaker}
          loading="lazy"
          decoding="async"
          className="h-full w-full object-cover"
          style={{ objectPosition: objectPosition ?? "50% 50%" }}
          onError={() => setFailed(true)}
        />
      ) : (
        <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-brand-green-mid to-brand-green-deep font-extrabold text-white">
          {initials(speaker)}
        </div>
      )}
    </div>
  );
}
