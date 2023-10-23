import { Outlet } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="p-12">
      <section>
        <h1 className="font-thin text-3xl">SwitchManager</h1>
      </section>
      <Outlet />
    </div>
  );
}
