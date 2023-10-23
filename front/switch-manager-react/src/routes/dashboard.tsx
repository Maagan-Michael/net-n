import { Outlet } from "react-router-dom";
import { ReactComponent as Search } from "../components/icons/search.svg";

export default function Dashboard() {
  return (
    <div className="p-12">
      <section>
        <h1 className="font-thin text-3xl">SwitchManager</h1>
        <section>
          <div className="rounded-md bg-neutral-100 w-[440px] mt-4 flex">
            <Search className="w-12 h-12" />
            <input
              type="search"
              placeholder="search..."
              className="bg-transparent outline-none"
            />
          </div>
        </section>
      </section>
      <Outlet />
    </div>
  );
}
