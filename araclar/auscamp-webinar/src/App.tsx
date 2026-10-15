import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import WebinarDetail from "./pages/WebinarDetail";
import PixelTracker from "./components/PixelTracker";

export default function App() {
  return (
    <>
      <PixelTracker />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/webinar/:slug" element={<WebinarDetail />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
