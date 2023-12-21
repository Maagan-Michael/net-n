import { Outlet, useLocation } from "react-router-dom";
import Navigation from "./navigation";
import { useTranslation } from "react-i18next";
import clsx from "clsx";

export default function Dashboard() {
  const { i18n } = useTranslation();
  const location = useLocation();
  const isPopup = location.pathname.startsWith("/connections/");
  return (
    <div
      className={clsx(
        "p-1 md:p-2 lg:p-8",
        isPopup &&
          "overflow-hidden max-h-screen md:max-h-none md:overflow-scroll"
      )}
      dir={i18n.dir()}
    >
      <Navigation />
      <Outlet />
    </div>
  );
}
