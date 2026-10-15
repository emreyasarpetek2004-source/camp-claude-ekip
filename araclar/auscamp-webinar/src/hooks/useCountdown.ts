import { useEffect, useState } from "react";

export interface TimeLeft {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
  done: boolean;
}

function compute(target: number): TimeLeft {
  const diff = target - Date.now();
  if (diff <= 0) {
    return { days: 0, hours: 0, minutes: 0, seconds: 0, done: true };
  }
  const totalSeconds = Math.floor(diff / 1000);
  return {
    days: Math.floor(totalSeconds / 86400),
    hours: Math.floor((totalSeconds % 86400) / 3600),
    minutes: Math.floor((totalSeconds % 3600) / 60),
    seconds: totalSeconds % 60,
    done: false,
  };
}

/**
 * Countdown to a target timestamp (ms). The initial state is computed
 * synchronously via lazy initialization, so the first paint already shows the
 * correct value — no 00:00:00 flash. This is a client-only Vite app, so there
 * is no SSR hydration mismatch to worry about.
 */
export function useCountdown(target: number | null): TimeLeft | null {
  const [timeLeft, setTimeLeft] = useState<TimeLeft | null>(() =>
    target === null ? null : compute(target)
  );

  useEffect(() => {
    if (target === null) {
      setTimeLeft(null);
      return;
    }
    setTimeLeft(compute(target));
    const id = window.setInterval(() => setTimeLeft(compute(target)), 1000);
    return () => window.clearInterval(id);
  }, [target]);

  return timeLeft;
}
