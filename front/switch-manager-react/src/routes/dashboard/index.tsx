import { Outlet } from "react-router-dom";
import Navigation from "./navigation";
import { useTranslation } from "react-i18next";
import clsx from "clsx";

export default function Dashboard() {
  const { i18n } = useTranslation();
  return (
    <div className={clsx("p-1 md:p-2 lg:p-8", i18n.dir())}>
      <Navigation />
      <Outlet />
    </div>
  );
}
