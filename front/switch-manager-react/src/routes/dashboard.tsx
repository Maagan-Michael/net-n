import clsx from "clsx";
import { Outlet } from "react-router-dom";
import { ReactComponent as Search } from "../components/icons/search.svg";

export default function Dashboard() {
  return (
    <div className="p-12">
      <section>
        <h1 className="font-thin text-3xl">SwitchManager</h1>
        <section>
          <div className="rounded-md bg-neutral-100 w-[440px] mt-6 flex px-1 shadow">
            <Search className={clsx("w-12 h-12", "text-red-400")} />
            <input
              type="search"
              placeholder="search..."
              className="bg-transparent outline-none text-sm grow"
            />
          </div>
        </section>
      </section>
      <Outlet />
    </div>
  );
}
