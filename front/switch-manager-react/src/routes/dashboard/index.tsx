import { Outlet } from "react-router-dom";
import { DesktopNav, MobileNav } from "./navigation";

export default function Dashboard() {
  return (
    <div className="p-1 md:p-2 lg:p-8">
      <DesktopNav />
      <Outlet />
      <MobileNav />
    </div>
  );
}
