import { Outlet } from "react-router-dom";
import Navigation from "./navigation";
import { useTranslation } from "react-i18next";

export default function Dashboard() {
  const { i18n } = useTranslation();
  return (
    <div className="p-1 md:p-2 lg:p-8" dir={i18n.dir()}>
      <Navigation />
      <Outlet />
    </div>
  );
}
