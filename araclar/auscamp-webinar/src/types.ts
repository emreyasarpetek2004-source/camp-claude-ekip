import { webinars } from "./config/webinars";

export type Webinar = (typeof webinars)[number];

// Meta Pixel global
declare global {
  interface Window {
    fbq?: (...args: unknown[]) => void;
  }
}

export {};
