import { useState, useCallback, MouseEventHandler } from "react";
import clsx from "clsx";
import { SearchBar } from "./SearchBar";

export function MobileNav() {
  const [open, setOpen] = useState(false);
  const onSearch: MouseEventHandler<HTMLButtonElement> = useCallback(
    (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!open) {
        setOpen(true);
      } else {
        setOpen(false);
      }
    },
    [open]
  );
  return (
    <nav className="lg:hidden fixed bottom-0 left-0 w-full h-14 drop-shadow-md">
      <div className="z-10 flex items-center justify-between p-4 w-full h-full bg-white">
        <h1 className="text-md font-thin">SM</h1>
        <button
          className="w-8 h-8 rounded-full bg-blue-400 flex items-center justify-center"
          onMouseDown={onSearch}
        />
      </div>

      <div
        className={clsx(
          "absolute w-full left-0 transition-all -z-[1] p-4",
          open ? "bottom-full visible" : "bottom-0 invisible"
        )}
      >
        <SearchBar shouldFocus={open} />
      </div>
    </nav>
  );
}
export function DesktopNav() {
  return (
    <nav className="hidden lg:block items-center gap-x-4 mt-4 md:mt-0">
      <h1 className="font-thin text-xl md:text-3xl">SwitchManager</h1>
      <section className="grow md:w-[440px] md:mt-4 lg:mt-6">
        <SearchBar />
      </section>
    </nav>
  );
}
