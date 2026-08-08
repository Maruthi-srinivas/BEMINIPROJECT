import { Navigate, Route, Routes } from "react-router-dom";
import { HomePage } from "./pages/HomePage";
import { UrlShortenerPage } from "./pages/services/UrlShortenerPage";
import { AuthPage } from "./pages/services/AuthPage";
import { RateLimiterPage } from "./pages/services/RateLimiterPage";
import { FileStoragePage } from "./pages/services/FileStoragePage";
import { NotificationsPage } from "./pages/services/NotificationsPage";
import { JobQueuePage } from "./pages/services/JobQueuePage";
import { ApiGatewayPage } from "./pages/services/ApiGatewayPage";
import { LogAggregatorPage } from "./pages/services/LogAggregatorPage";
import { FeatureFlagsPage } from "./pages/services/FeatureFlagsPage";
import { MiniRedisPage } from "./pages/services/MiniRedisPage";

export default function App() {
  return (
    <div className="app-root">
      <div className="ambient-bg" aria-hidden="true">
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />
        <div className="noise-overlay" />
      </div>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/services/url-shortener" element={<UrlShortenerPage />} />
        <Route path="/services/auth-service" element={<AuthPage />} />
        <Route path="/services/rate-limiter" element={<RateLimiterPage />} />
        <Route path="/services/file-storage" element={<FileStoragePage />} />
        <Route path="/services/notifications" element={<NotificationsPage />} />
        <Route path="/services/job-queue" element={<JobQueuePage />} />
        <Route path="/services/api-gateway" element={<ApiGatewayPage />} />
        <Route path="/services/log-aggregator" element={<LogAggregatorPage />} />
        <Route path="/services/feature-flags" element={<FeatureFlagsPage />} />
        <Route path="/services/mini-redis" element={<MiniRedisPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
